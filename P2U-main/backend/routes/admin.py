from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from bson import ObjectId
from functools import wraps

from models import User, Product, Order, TokenRequest, Notification

admin = Blueprint('admin', __name__)

# ===== Hardcoded Admin Credentials =====
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def admin_required(fn):
    """Decorator to check if user is admin"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.objects(id=ObjectId(user_id)).first()
        if not user or not user.is_admin:
            return jsonify({"msg": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


# -----------------------------
# Admin Login
# -----------------------------
@admin.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # Find or create admin user
        admin_user = User.objects(username=ADMIN_USERNAME, is_admin=True).first()
        
        if not admin_user:
            # Create admin user if not exists
            from werkzeug.security import generate_password_hash
            admin_user = User(
                username=ADMIN_USERNAME,
                email="admin@p2ukaiser.com",
                password=generate_password_hash(ADMIN_PASSWORD),
                full_name="Administrator",
                is_admin=True,
                is_email_verified=True
            )
            admin_user.save()
        
        access_token = create_access_token(identity=str(admin_user.id))
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": str(admin_user.id),
                "username": admin_user.username,
                "is_admin": True
            }
        }), 200
    
    return jsonify({"msg": "Invalid admin credentials"}), 401


# -----------------------------
# Get Dashboard Statistics
# -----------------------------
@admin.route('/admin/stats', methods=['GET'])
@admin_required
def get_stats():
    total_users = User.objects(is_admin__ne=True).count()
    total_sellers = User.objects(is_seller=True).count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    
    # Calculate total revenue
    orders = Order.objects(status='completed')
    total_revenue = sum(float(order.total_price) for order in orders)
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at').limit(10)
    recent_orders_list = []
    for order in recent_orders:
        recent_orders_list.append({
            "id": str(order.id),
            "user": order.user.username if order.user else "Unknown",
            "total": float(order.total_price),
            "status": order.status,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return jsonify({
        "total_users": total_users,
        "total_sellers": total_sellers,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders_list
    }), 200


# -----------------------------
# Get All Users
# -----------------------------
@admin.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.objects(is_admin__ne=True)
    users_list = []
    for user in users:
        users_list.append({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_seller": user.is_seller,
            "is_active": user.is_active,
            "coin_balance": user.coin_balance,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(users_list), 200


# -----------------------------
# Ban/Unban User
# -----------------------------
@admin.route('/admin/users/<user_id>/toggle-ban', methods=['PUT'])
@admin_required
def toggle_ban_user(user_id):
    try:
        user = User.objects.get(id=ObjectId(user_id))
        user.is_active = not user.is_active
        user.save()
        return jsonify({
            "msg": f"User {'unbanned' if user.is_active else 'banned'} successfully",
            "is_active": user.is_active
        }), 200
    except:
        return jsonify({"msg": "User not found"}), 404


# -----------------------------
# Delete User
# -----------------------------
@admin.route('/admin/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        user = User.objects.get(id=ObjectId(user_id))
        # Delete user's products
        Product.objects(seller=user).delete()
        user.delete()
        return jsonify({"msg": "User deleted successfully"}), 200
    except:
        return jsonify({"msg": "User not found"}), 404


# -----------------------------
# Get All Products (Admin)
# -----------------------------
@admin.route('/admin/products', methods=['GET'])
@admin_required
def get_all_products_admin():
    products = Product.objects.order_by('-created_at')
    products_list = []
    for p in products:
        products_list.append({
            "id": str(p.id),
            "name": p.name,
            "price": float(p.price),
            "image_url": p.image_url,
            "seller": {
                "id": str(p.seller.id),
                "username": p.seller.username
            } if p.seller else None,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(products_list), 200


# -----------------------------
# Delete Product (Admin)
# -----------------------------
@admin.route('/admin/products/<product_id>', methods=['DELETE'])
@admin_required
def delete_product_admin(product_id):
    try:
        product = Product.objects.get(id=ObjectId(product_id))
        product.delete()
        return jsonify({"msg": "Product deleted successfully"}), 200
    except:
        return jsonify({"msg": "Product not found"}), 404


# -----------------------------
# Get All Orders (Admin)
# -----------------------------
@admin.route('/admin/orders', methods=['GET'])
@admin_required
def get_all_orders():
    orders = Order.objects.order_by('-created_at')
    orders_list = []
    for order in orders:
        orders_list.append({
            "id": str(order.id),
            "user": {
                "id": str(order.user.id),
                "username": order.user.username
            } if order.user else None,
            "total_price": float(order.total_price),
            "status": order.status,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(orders_list), 200


# -----------------------------
# Update Order Status (Admin)
# -----------------------------
@admin.route('/admin/orders/<order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['pending', 'processing', 'completed', 'cancelled']:
        return jsonify({"msg": "Invalid status"}), 400
    
    try:
        order = Order.objects.get(id=ObjectId(order_id))
        order.status = new_status
        order.save()
        return jsonify({"msg": "Order status updated", "status": new_status}), 200
    except:
        return jsonify({"msg": "Order not found"}), 404


# -----------------------------
# Get All Token Requests (Admin)
# -----------------------------
@admin.route('/admin/token-requests', methods=['GET'])
@admin_required
def get_token_requests():
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        requests = TokenRequest.objects.order_by('-created_at')
    else:
        requests = TokenRequest.objects(status=status_filter).order_by('-created_at')
    
    result = []
    for r in requests:
        result.append({
            "id": str(r.id),
            "user": {
                "id": str(r.user.id),
                "username": r.user.username,
                "email": r.user.email
            } if r.user else None,
            "amount": r.amount,
            "status": r.status,
            "payment_proof_url": r.payment_proof_url,
            "admin_note": r.admin_note,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "processed_at": r.processed_at.strftime("%Y-%m-%d %H:%M:%S") if r.processed_at else None
        })
    
    return jsonify({"requests": result}), 200


# -----------------------------
# Approve Token Request (Admin)
# -----------------------------
@admin.route('/admin/token-requests/<request_id>/approve', methods=['PUT'])
@admin_required
def approve_token_request(request_id):
    from datetime import datetime
    
    admin_id = get_jwt_identity()
    admin_user = User.objects(id=ObjectId(admin_id)).first()
    
    data = request.get_json() or {}
    admin_note = data.get('admin_note', '')
    
    try:
        token_request = TokenRequest.objects.get(id=ObjectId(request_id))
    except:
        return jsonify({"msg": "Token request not found"}), 404
    
    if token_request.status != 'pending':
        return jsonify({"msg": "คำขอนี้ได้รับการดำเนินการแล้ว"}), 400
    
    # อัปเดตคำขอ
    token_request.status = 'approved'
    token_request.admin_note = admin_note
    token_request.approved_by = admin_user
    token_request.processed_at = datetime.utcnow()
    token_request.save()
    
    # เพิ่ม Token ให้ผู้ใช้
    user = token_request.user
    user.token_balance = (user.token_balance or 0) + token_request.amount
    user.save()
    
    # แจ้งเตือนผู้ใช้
    Notification(
        user=user,
        title="✅ คำขอเติม Token ได้รับการอนุมัติ",
        message=f"คุณได้รับ {token_request.amount} Token แล้ว! ใช้สำหรับประมูลสินค้าได้เลย",
        type="system",
        link="/token-topup"
    ).save()
    
    return jsonify({
        "msg": f"อนุมัติ Token {token_request.amount} ให้ {user.username} สำเร็จ",
        "new_balance": user.token_balance
    }), 200


# -----------------------------
# Reject Token Request (Admin)
# -----------------------------
@admin.route('/admin/token-requests/<request_id>/reject', methods=['PUT'])
@admin_required
def reject_token_request(request_id):
    from datetime import datetime
    
    admin_id = get_jwt_identity()
    admin_user = User.objects(id=ObjectId(admin_id)).first()
    
    data = request.get_json() or {}
    admin_note = data.get('admin_note', 'ไม่ผ่านการตรวจสอบ')
    
    try:
        token_request = TokenRequest.objects.get(id=ObjectId(request_id))
    except:
        return jsonify({"msg": "Token request not found"}), 404
    
    if token_request.status != 'pending':
        return jsonify({"msg": "คำขอนี้ได้รับการดำเนินการแล้ว"}), 400
    
    # อัปเดตคำขอ
    token_request.status = 'rejected'
    token_request.admin_note = admin_note
    token_request.approved_by = admin_user
    token_request.processed_at = datetime.utcnow()
    token_request.save()
    
    # แจ้งเตือนผู้ใช้
    user = token_request.user
    Notification(
        user=user,
        title="❌ คำขอเติม Token ถูกปฏิเสธ",
        message=f"คำขอ {token_request.amount} Token ถูกปฏิเสธ: {admin_note}",
        type="system",
        link="/token-topup"
    ).save()
    
    return jsonify({
        "msg": f"ปฏิเสธคำขอของ {user.username} สำเร็จ"
    }), 200


# -----------------------------
# Get Token Stats (Admin)
# -----------------------------
@admin.route('/admin/token-stats', methods=['GET'])
@admin_required
def get_token_stats():
    pending_count = TokenRequest.objects(status='pending').count()
    approved_count = TokenRequest.objects(status='approved').count()
    rejected_count = TokenRequest.objects(status='rejected').count()
    
    # คำนวณยอด Token ที่อนุมัติทั้งหมด
    approved_requests = TokenRequest.objects(status='approved')
    total_approved_tokens = sum(r.amount for r in approved_requests)
    
    return jsonify({
        "pending": pending_count,
        "approved": approved_count,
        "rejected": rejected_count,
        "total_approved_tokens": total_approved_tokens
    }), 200
