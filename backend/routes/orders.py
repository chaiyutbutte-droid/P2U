from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from datetime import datetime

from models import User, Order, CartItem, Product, Notification

orders = Blueprint('orders', __name__)

# ----------------------------------------------------------
# 1. ดูประวัติการสั่งซื้อ (สำหรับลูกค้า) 
# ----------------------------------------------------------
@orders.route('/orders/my-orders', methods=['GET'])
@jwt_required()
def get_my_orders():
    user_id = get_jwt_identity()
    try:
        user = User.objects.get(id=ObjectId(user_id))
        user_orders = Order.objects(user=user).order_by('-created_at')
        
        result = []
        for order in user_orders:
            items_list = []
            for item_ref in order.items:
                try:
                    if item_ref and item_ref.product:
                        items_list.append({
                            "id": str(item_ref.product.id),
                            "quantity": int(item_ref.quantity),
                            "price": float(item_ref.product.price),
                            "product": {
                                "name": item_ref.product.name,
                                "image_url": item_ref.product.image_url,
                                "price": float(item_ref.product.price)
                            }
                        })
                except Exception:
                    continue
            
            result.append({
                "_id": str(order.id),
                "items": items_list,
                "total_price": float(order.total_price),
                "status": order.status,
                "created_at": order.created_at.isoformat() if order.created_at else None
            })
        
        return jsonify(result), 200
    except DoesNotExist:
        return jsonify({"msg": "ไม่พบข้อมูลผู้ใช้"}), 404
    except Exception as e:
        return jsonify({"msg": f"เกิดข้อผิดพลาด: {str(e)}"}), 500

# -----------------------------
# 2. สร้างคำสั่งซื้อ (Checkout)
# -----------------------------
@orders.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    item_ids = data.get('cart_items', [])
    
    if not item_ids:
        return jsonify({"msg": "ไม่มีสินค้าที่เลือกชำระเงินเพคะ"}), 400
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        final_cart_items = []
        total_price = 0
        
        for item_id in item_ids:
            if not ObjectId.is_valid(item_id): continue
            oid = ObjectId(item_id)
            
            # ค้นหาจาก CartItem (ตะกร้า)
            cart_item = CartItem.objects.filter(id=oid, user=user).first()
            if not cart_item:
                cart_item = CartItem.objects.filter(product=oid, user=user).first()
            
            # ถ้าไม่เจอในตะกร้า แต่เป็น ID สินค้า ให้สร้างเป็นไอเท็มชั่วคราว
            if not cart_item:
                product = Product.objects.filter(id=oid).first()
                if product:
                    cart_item = CartItem(user=user, product=product, quantity=1)
                    # ยังไม่ save ลง CartItem table แต่จะเก็บไว้ใน List ออเดอร์
            
            if cart_item and cart_item.product:
                final_cart_items.append(cart_item)
                total_price += float(cart_item.product.price) * int(cart_item.quantity)

        if not final_cart_items:
            return jsonify({"msg": "ไม่พบข้อมูลสินค้าที่ต้องการสั่งซื้อในระบบเพคะ"}), 400
        
        new_order = Order(
            user=user,
            items=final_cart_items,
            total_price=total_price,
            status='pending',
            created_at=datetime.utcnow()
        )
        new_order.save()
        
        # แจ้งเตือนผู้ขายว่ามีออเดอร์ใหม่ (สถานะยังเป็น pending)
        seller_notified = set()
        for item in final_cart_items:
            seller = item.product.seller
            if seller:
                seller_id_str = str(seller.id)
                if seller_id_str not in seller_notified:
                    Notification(
                        user=seller,
                        title="ยอดขายใหม่ ✨",
                        message=f"คุณได้รับออเดอร์ใหม่จากคุณ {user.username} แล้วเพคะ",
                        type="order",
                        link="/seller-dashboard"
                    ).save()
                    seller_notified.add(seller_id_str)
        
        return jsonify({
            "msg": "สร้างคำสั่งซื้อสำเร็จแล้วเพคะ! ✨",
            "order_id": str(new_order.id),
            "total_price": total_price
        }), 201
    except Exception as e:
        return jsonify({"msg": f"เกิดข้อผิดพลาดที่ระบบ: {str(e)}"}), 500

# ----------------------------------------------------------
# 3. บันทึกการชำระเงิน (อัปเดตสถานะเป็น paid) ✅
# ----------------------------------------------------------
@orders.route('/orders/<order_id>/pay', methods=['PUT'])
@jwt_required()
def pay_order(order_id):
    user_id = get_jwt_identity()
    try:
        order = Order.objects.get(id=ObjectId(order_id), user=ObjectId(user_id))
        
        if order.status == 'pending':
            order.status = 'paid'
            order.save()
            
            # แจ้งเตือนผู้ขายและอัปเดตยอดขายรวม
            seller_notified = set()
            for item in order.items:
                seller = item.product.seller
                if seller:
                    seller_id_str = str(seller.id)
                    if seller_id_str not in seller_notified:
                        Notification(
                            user=seller,
                            title="ได้รับการชำระเงินแล้ว 💰",
                            message=f"ออเดอร์ #{str(order.id)[-6:]} ชำระเงินเรียบร้อยแล้ว เตรียมจัดส่งนะเพคะ",
                            type="payment_received",
                            link="/seller-dashboard"
                        ).save()
                        
                        # อัปเดตยอดขายรวมของผู้ขาย
                        current_sales = getattr(seller, 'total_sales', 0) or 0
                        seller.total_sales = current_sales + (float(item.product.price) * int(item.quantity))
                        seller.save()
                        seller_notified.add(seller_id_str)

            return jsonify({"msg": "ชำระเงินสำเร็จและอัปเดตสถานะแล้วเพคะ ✨"}), 200
        else:
            return jsonify({"msg": "ออเดอร์นี้ไม่ได้อยู่ในสถานะรอชำระเงินเพคะ"}), 400

    except DoesNotExist:
        return jsonify({"msg": "ไม่พบข้อมูลคำสั่งซื้อเพคะ"}), 404
    except Exception as e:
        return jsonify({"msg": f"Backend Error: {str(e)}"}), 500

# -----------------------------
# 4. ดูออเดอร์ของผู้ขาย (Seller Orders)
# -----------------------------
@orders.route('/orders/seller/<seller_id>', methods=['GET'])
@jwt_required()
def get_seller_orders(seller_id):
    user_id = get_jwt_identity()
    current_user = User.objects(id=ObjectId(user_id), is_seller=True).first()
    
    if not current_user or str(current_user.id) != seller_id:
        return jsonify({"msg": "Unauthorized"}), 403

    try:
        seller_oid = ObjectId(seller_id)
        all_orders = Order.objects().order_by('-created_at')

        result = []
        for order in all_orders:
            seller_items = []
            for item in order.items:
                try:
                    if item and item.product:
                        product_seller = item.product.seller
                        if product_seller and str(product_seller.id) == str(seller_oid):
                            seller_items.append({
                                "product_id": str(item.product.id),
                                "product_name": item.product.name,
                                "quantity": int(item.quantity),
                                "price": float(item.product.price),
                                "image": item.product.image_url
                            })
                except Exception:
                    continue

            if seller_items:
                result.append({
                    "id": str(order.id),
                    "buyer": {
                        "id": str(order.user.id) if order.user else "Unknown",
                        "username": order.user.username if order.user else "Unknown User"
                    },
                    "items": seller_items,
                    "items_count": len(seller_items),
                    "total_price": sum(i["price"] * i["quantity"] for i in seller_items),
                    "status": order.status,
                    "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else "N/A"
                })

        return jsonify({"orders": result, "total": len(result)}), 200
    except Exception as e:
        return jsonify({"msg": f"Backend Error: {str(e)}"}), 500

# ----------------------------------------------------------
# 5. อัปเดตสถานะคำสั่งซื้อ (โดยผู้ขาย)
# ----------------------------------------------------------
@orders.route('/orders/<order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({"msg": "กรุณาระบุสถานะเพคะ"}), 400

    try:
        current_user = User.objects(id=ObjectId(user_id), is_seller=True).first()
        if not current_user:
            return jsonify({"msg": "เฉพาะผู้ขายเท่านั้นที่เปลี่ยนสถานะได้"}), 403

        order = Order.objects.get(id=ObjectId(order_id))
        
        has_product = False
        for item in order.items:
            if item.product and str(item.product.seller.id) == str(current_user.id):
                has_product = True
                break
        
        if not has_product:
            return jsonify({"msg": "คุณไม่มีสิทธิ์จัดการออเดอร์นี้"}), 403

        old_status = order.status
        order.status = new_status
        order.save()

        if order.user:
            status_map = {
                "processing": "กำลังจัดส่ง 🚚", 
                "completed": "สำเร็จแล้ว ✅",
                "cancelled": "ถูกยกเลิก ❌"
            }
            display_status = status_map.get(new_status, new_status)
            
            Notification(
                user=order.user,
                title="อัปเดตสถานะคำสั่งซื้อ ✨",
                message=f"ออเดอร์ #{str(order.id)[-6:]} เปลี่ยนสถานะเป็น: {display_status}",
                type="order_update",
                link="/profile"
            ).save()

        return jsonify({
            "msg": f"อัปเดตสำเร็จจาก {old_status} เป็น {new_status} แล้วเพคะ",
            "new_status": new_status
        }), 200

    except DoesNotExist:
        return jsonify({"msg": "ไม่พบออเดอร์นี้"}), 404
    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500

# ----------------------------------------------------------
# 6. ยกเลิกคำสั่งซื้อ (โดยลูกค้า) ❌
# ----------------------------------------------------------
@orders.route('/orders/<order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()
    try:
        order = Order.objects.get(id=ObjectId(order_id), user=ObjectId(user_id))
        
        if order.status not in ['pending', 'paid']:
            return jsonify({"msg": "ไม่สามารถยกเลิกได้ เนื่องจากสินค้าอยู่ระหว่างจัดส่งหรือสำเร็จแล้วเพคะ"}), 400
        
        order.status = 'cancelled'
        order.save()

        # แจ้งเตือนผู้ขาย
        seller_notified = set()
        for item in order.items:
            if item.product and item.product.seller:
                s_id = str(item.product.seller.id)
                if s_id not in seller_notified:
                    Notification(
                        user=item.product.seller,
                        title="คำสั่งซื้อถูกยกเลิก 💔",
                        message=f"ออเดอร์ #{str(order.id)[-6:]} ถูกยกเลิกโดยลูกค้าเพคะ",
                        type="order_cancelled",
                        link="/seller-dashboard"
                    ).save()
                    seller_notified.add(s_id)

        return jsonify({"msg": "ยกเลิกคำสั่งซื้อเรียบร้อยแล้วเพคะ ✨"}), 200

    except DoesNotExist:
        return jsonify({"msg": "ไม่พบข้อมูลคำสั่งซื้อเพคะ"}), 404
    except Exception as e:
        return jsonify({"msg": f"Backend Error: {str(e)}"}), 500