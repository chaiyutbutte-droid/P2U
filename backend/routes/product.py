import os
import uuid
from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError

from models import User, Product

product = Blueprint('product', __name__)
UPLOAD_FOLDER = os.path.join('static', 'products')  # เก็บไฟล์ไว้ใน static/products

# -----------------------------
# ตรวจสอบไฟล์ที่อนุญาตให้อัปโหลด
# -----------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# -----------------------------
# สร้างสินค้าใหม่ (เฉพาะ seller)
# -----------------------------
@product.route('/products', methods=['POST'])
@jwt_required()
def create_product():
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
            # คืนค่าเป็น full URL เลย
            image_url = url_for('static', filename=f'products/{new_filename}', _external=True)
        except Exception as e:
            return jsonify({"msg": f"Failed to upload image: {str(e)}"}), 500

    try:
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            image_url=image_url,
            seller=user
        )
        new_product.save()

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

# -----------------------------
# ดึงสินค้าทั้งหมด
# -----------------------------
@product.route('/products', methods=['GET'])
def get_all_products():
    products = Product.objects.order_by('-created_at')
    product_list = []

    for p in products:
        product_list.append({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "image_url": p.image_url,  # ตอน save ลง DB เราเก็บ full URL แล้ว
            "seller": {
                "id": str(p.seller.id),
                "username": p.seller.username,
                "shop_name": p.seller.shop_name
            },
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(product_list), 200

# -----------------------------
# ดึงสินค้าเดี่ยว
# -----------------------------
@product.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
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

# -----------------------------
# ลบสินค้า (เฉพาะ seller เจ้าของ)
# -----------------------------
@product.route('/products/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()

    try:
        product_item = Product.objects.get(id=ObjectId(product_id))
    except (DoesNotExist, ValidationError):
        return jsonify({"msg": "Product not found."}), 404

    if str(product_item.seller.id) != user_id:
        return jsonify({"msg": "Unauthorized. You can only delete your own products."}), 403

    try:
        # ลบไฟล์รูปจาก server (ถ้ามี)
        if product_item.image_url:
            filename = os.path.basename(product_item.image_url)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        product_item.delete()
        return jsonify({"msg": "Product deleted successfully."}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
