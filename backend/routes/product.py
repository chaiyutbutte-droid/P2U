import os
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError

from models import User, Product

product = Blueprint('product', __name__)
UPLOAD_FOLDER = 'uploads/products'

# ฟังก์ชันตรวจสอบไฟล์ที่อัปโหลด
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# ✅ Create Product
@product.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    """
    สร้างสินค้าใหม่ โดยรับข้อมูลจาก form data และไฟล์รูปภาพ
    ต้องเป็น seller เท่านั้นถึงจะสร้างสินค้าได้
    """
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not user or not user.is_seller:
        return jsonify({"msg": "Unauthorized. Only sellers can create products."}), 403

    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    image = request.files.get('image')

    if not all([name, price]):
        return jsonify({"msg": "Product name and price are required."}), 400

    image_url = None
    if image and allowed_file(image.filename):
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(image.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, new_filename)
            image.save(save_path)
            image_url = f"/{UPLOAD_FOLDER}/{new_filename}"
        except Exception as e:
            return jsonify({"msg": f"Failed to upload image: {str(e)}"}), 500

    try:
        # เก็บ seller เป็น ObjectId ของ user
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            image_url=image_url,
            seller=user  # <-- เปลี่ยนจาก user.id เป็น user object
        )
        new_product.save()

        # ส่งข้อมูลพร้อม seller info
        return jsonify({
            "id": str(new_product.id),
            "name": new_product.name,
            "description": new_product.description,
            "price": float(new_product.price),
            "image_url": new_product.image_url,
            "seller": {
                "id": str(user.id),
                "username": user.username,
                "shop_name": user.shop_name
            },
            "created_at": new_product.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }), 201

    except ValidationError as e:
        return jsonify({"msg": str(e)}), 400
    except ValueError:
        return jsonify({"msg": "Price must be a valid number."}), 400

# ✅ Get all products
@product.route('/products', methods=['GET'])
def get_all_products():
    """
    ดึงข้อมูลสินค้าทั้งหมดพร้อม seller info
    """
    products = Product.objects.order_by('-created_at')  # ล่าสุดก่อน
    product_list = []
    for p in products:
        product_list.append({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "image_url": p.image_url,
            "seller": {
                "id": str(p.seller.id),
                "username": p.seller.username,
                "shop_name": p.seller.shop_name
            },
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(product_list), 200

# ✅ Get a single product
@product.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    """
    ดึงข้อมูลสินค้าเฉพาะรายการ พร้อม seller info
    """
    try:
        p = Product.objects.get(id=ObjectId(product_id))
        return jsonify({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "image_url": p.image_url,
            "seller": {
                "id": str(p.seller.id),
                "username": p.seller.username,
                "shop_name": p.seller.shop_name
            },
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except (DoesNotExist, ValidationError):
        return jsonify({"msg": "Product not found."}), 404

# ✅ Delete product
@product.route('/products/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """
    ลบสินค้า ต้องเป็น seller ที่สร้างสินค้านั้นเท่านั้น
    """
    user_id = get_jwt_identity()
    try:
        product_item = Product.objects.get(id=ObjectId(product_id))
    except (DoesNotExist, ValidationError):
        return jsonify({"msg": "Product not found."}), 404

    if str(product_item.seller.id) != user_id:
        return jsonify({"msg": "Unauthorized. You can only delete your own products."}), 403

    try:
        # ลบรูปภาพจาก server ด้วย (optional)
        if product_item.image_url and os.path.exists(product_item.image_url.lstrip('/')):
            os.remove(product_item.image_url.lstrip('/'))
        product_item.delete()
        return jsonify({"msg": "Product deleted successfully."}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
