from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from datetime import datetime

from models import User, Order, CartItem, Product, Notification

orders = Blueprint('orders', __name__)

# -----------------------------
# 1. ดูประวัติการสั่งซื้อ (Order History)
# -----------------------------
@orders.route('/orders', methods=['GET'])
@jwt_required()
def get_order_history():
    user_id = get_jwt_identity()
    try:
        user = User.objects.get(id=ObjectId(user_id))
        # ดึงออเดอร์ของ User เรียงตามใหม่ไปเก่า
        user_orders = Order.objects(user=user).order_by('-created_at')
        
        result = []
        for order in user_orders:
            items_list = []
            for item_ref in order.items:
                try:
                    # ป้องกันกรณีสินค้าถูกลบออกจากระบบไปแล้ว
                    if item_ref and item_ref.product:
                        items_list.append({
                            "product_id": str(item_ref.product.id),
                            "product_name": item_ref.product.name,
                            "product_image": item_ref.product.image_url,
                            "quantity": int(item_ref.quantity),
                            "price": float(item_ref.product.price)
                        })
                except: continue
            
            result.append({
                "id": str(order.id),
                "items": items_list,
                "total_price": float(order.total_price),
                "status": order.status,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return jsonify({
            "orders": result,
            "total": len(result)
        }), 200
        
    except DoesNotExist:
        return jsonify({"msg": "ไม่พบข้อมูลผู้ใช้"}), 404
    except Exception as e:
        return jsonify({"msg": f"เกิดข้อผิดพลาด: {str(e)}"}), 500


# -----------------------------
# 2. สร้างคำสั่งซื้อ (Checkout) - ระบบชำระเงินตรง
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
            
            # 🔍 ขั้นตอนค้นหาสินค้า (รองรับทั้ง CartItem ID และ Product ID)
            # พยายามหาในตะกร้าก่อน
            cart_item = CartItem.objects.filter(id=oid, user=user).first()
            if not cart_item:
                cart_item = CartItem.objects.filter(product=oid, user=user).first()
            
            # ถ้าหาในตะกร้าไม่เจอเลย (เช่น ซื้อทันที) ให้สร้าง CartItem ชั่วคราว
            if not cart_item:
                product = Product.objects.filter(id=oid).first()
                if product:
                    cart_item = CartItem(user=user, product=product, quantity=1)
                    cart_item.save()
            
            if cart_item and cart_item.product:
                final_cart_items.append(cart_item)
                total_price += float(cart_item.product.price) * int(cart_item.quantity)

        if not final_cart_items:
            return jsonify({"msg": "ไม่พบข้อมูลสินค้าที่ต้องการสั่งซื้อในระบบเพคะ"}), 400
        
        # 🧾 สร้าง Order (กำหนดสถานะเป็น paid ทันทีเพราะไม่ได้ใช้ระบบเหรียญ)
        new_order = Order(
            user=user,
            items=final_cart_items,
            total_price=total_price,
            status='paid',
            created_at=datetime.utcnow()
        )
        new_order.save()
        
        # 🔔 แจ้งเตือนผู้ขายและอัปเดตยอดขาย
        seller_notified = set()
        for item in final_cart_items:
            seller = item.product.seller
            if seller:
                # ส่งแจ้งเตือน (ส่ง 1 ครั้งต่อ 1 ออเดอร์สำหรับผู้ขายคนนั้นๆ)
                if str(seller.id) not in seller_notified:
                    Notification(
                        user=seller,
                        title="ยอดขายใหม่ ✨",
                        message=f"คุณได้รับออเดอร์ใหม่มูลค่า ฿{total_price} จากคุณ {user.username} แล้วเพคะ",
                        type="order",
                        link="/seller-dashboard"
                    ).save()
                    seller_notified.add(str(seller.id))
                
                # เพิ่มยอดขายสะสมให้ผู้ขาย
                current_sales = getattr(seller, 'total_sales', 0) or 0
                seller.total_sales = current_sales + (float(item.product.price) * int(item.quantity))
                seller.save()
        
        # 🗑️ ลบสินค้าออกจากตะกร้าหลังจากซื้อสำเร็จ
        for item in final_cart_items:
            item.delete()
        
        return jsonify({
            "msg": "สั่งซื้อสำเร็จแล้วเพคะ! ✨",
            "order_id": str(new_order.id),
            "total_price": total_price
        }), 201
        
    except DoesNotExist:
        return jsonify({"msg": "ไม่พบข้อมูลผู้ใช้ในระบบ"}), 404
    except Exception as e:
        return jsonify({"msg": f"เกิดข้อผิดพลาดที่ระบบ: {str(e)}"}), 500


# -----------------------------
# 3. ยกเลิกคำสั่งซื้อ (Cancel Order)
# -----------------------------
@orders.route('/orders/<order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()
    try:
        order = Order.objects.get(id=ObjectId(order_id))
        
        # ตรวจสอบสิทธิ์ว่าเป็นเจ้าของออเดอร์หรือไม่
        if str(order.user.id) != user_id:
            return jsonify({"msg": "ไม่มีสิทธิ์ดำเนินการเพคะ"}), 403
        
        # อัปเดตสถานะเป็น cancelled (ไม่ต้องคืนเหรียญเพราะไม่ได้ใช้ระบบเหรียญ)
        order.status = 'cancelled'
        order.save()
        
        return jsonify({"msg": "ยกเลิกออเดอร์เรียบร้อยเพคะ"}), 200
        
    except DoesNotExist:
        return jsonify({"msg": "ไม่พบข้อมูลออเดอร์"}), 404
    except Exception as e:
        return jsonify({"msg": f"เกิดข้อผิดพลาด: {str(e)}"}), 500