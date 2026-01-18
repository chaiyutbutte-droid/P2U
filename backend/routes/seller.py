import os
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from models import Product, User

# Create a new Blueprint for seller routes
seller = Blueprint('seller', __name__)

# --- Constants for file upload ---
UPLOAD_FOLDER = 'uploads/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Save uploaded image with unique filename
def save_image(image_file):
    if image_file and allowed_file(image_file.filename):
        ext = image_file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        image_file.save(file_path)
        # ✅ เก็บเป็น relative path สำหรับ client
        return f"/uploads/products/{unique_filename}"
    return None

# 🔸 Get all products for the current seller
@seller.route('/seller/products', methods=['GET'])
@jwt_required()
def get_seller_products():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    if not user or not user.is_seller:
        return jsonify({"msg": "Unauthorized. This action requires seller privileges."}), 403

    products = Product.objects(seller=user).order_by('-created_at')
    return jsonify([
        {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "image_url": product.image_url,
            "category": product.category or 'all',
            "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for product in products
    ]), 200

# 🔸 Add a new product
@seller.route('/seller/products', methods=['POST'])
@jwt_required()
def add_product():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    if not user or not user.is_seller:
        return jsonify({"msg": "Unauthorized. This action requires seller privileges."}), 403

    data = request.form
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    category = data.get('category', 'all')  # รับหมวดหมู่จาก form
    if not name or not price:
        return jsonify({"msg": "Product name and price are required."}), 400

    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        image_url = save_image(file)
        if not image_url:
            return jsonify({"msg": "Invalid image file provided."}), 400

    try:
        product = Product(
            name=name,
            description=description,
            price=float(price),
            image_url=image_url,
            category=category,  # บันทึกหมวดหมู่
            seller=user
        )
        product.save()
        return jsonify({
            "msg": "Product added successfully!",
            "product": {
                "id": str(product.id),
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "image_url": product.image_url,
                "category": product.category or 'all',
                "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 201
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

# 🔸 Get a single product by ID
@seller.route('/seller/products/<product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    try:
        product = Product.objects.get(id=ObjectId(product_id), seller=user)
    except Product.DoesNotExist:
        return jsonify({"msg": "Product not found or unauthorized access."}), 404
    except Exception:
        return jsonify({"msg": "Invalid product ID."}), 400

    return jsonify({
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "price": float(product.price),
        "image_url": product.image_url,
        "category": product.category or 'all',
        "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })

# 🔸 Update a product by ID
@seller.route('/seller/products/<product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    try:
        product = Product.objects.get(id=ObjectId(product_id), seller=user)
    except Product.DoesNotExist:
        return jsonify({"msg": "Product not found or unauthorized access."}), 404
    except Exception:
        return jsonify({"msg": "Invalid product ID."}), 400

    data = request.get_json()
    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'description' in data:
        update_fields['description'] = data['description']
    if 'price' in data:
        update_fields['price'] = float(data['price'])
    if 'category' in data:
        update_fields['category'] = data['category']

    product.update(**update_fields)
    return jsonify({"msg": "Product updated successfully!"}), 200

# 🔸 Delete a product by ID
@seller.route('/seller/products/<product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    try:
        product = Product.objects.get(id=ObjectId(product_id), seller=user)
        # ✅ ลบไฟล์จริงจากโฟลเดอร์
        if product.image_url:
            file_path = product.image_url.lstrip('/')
            if os.path.exists(file_path):
                os.remove(file_path)
        product.delete()
        return jsonify({"msg": "Product deleted successfully!"}), 200
    except Product.DoesNotExist:
        return jsonify({"msg": "Product not found or unauthorized access."}), 404
    except Exception as e:
        return jsonify({"msg": f"Invalid product ID: {str(e)}"}), 400

# 🔸 Update product image
@seller.route('/seller/products/<product_id>/image', methods=['PUT'])
@jwt_required()
def update_product_image(product_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    try:
        product = Product.objects.get(id=ObjectId(product_id), seller=user)
    except Product.DoesNotExist:
        return jsonify({"msg": "Product not found or unauthorized access."}), 404
    except Exception:
        return jsonify({"msg": "Invalid product ID."}), 400

    if 'image' not in request.files:
        return jsonify({"msg": "No image file provided."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"msg": "No selected file."}), 400

    # ✅ ลบไฟล์เก่า
    if product.image_url:
        file_path = product.image_url.lstrip('/')
        if os.path.exists(file_path):
            os.remove(file_path)

    new_image_url = save_image(file)
    if new_image_url:
        product.update(image_url=new_image_url)
        return jsonify({"msg": "Image updated successfully.", "image_url": new_image_url}), 200
    else:
        return jsonify({"msg": "Invalid file type."}), 400

# 🔸 Get all available categories
@seller.route('/categories', methods=['GET'])
def get_categories():
    """Return all available product categories"""
    categories = [
        {"id": "all", "name": "ทั้งหมด", "icon": "🛍️"},
        {"id": "electronics", "name": "อิเล็กทรอนิกส์", "icon": "📱"},
        {"id": "fashion", "name": "แฟชั่น", "icon": "👗"},
        {"id": "gaming", "name": "เกมมิ่ง", "icon": "🎮"},
        {"id": "beauty", "name": "ความงาม", "icon": "💄"},
        {"id": "home", "name": "บ้าน & สวน", "icon": "🏠"},
        {"id": "sports", "name": "กีฬา", "icon": "⚽"},
        {"id": "food", "name": "อาหาร", "icon": "🍔"},
        {"id": "books", "name": "หนังสือ", "icon": "📚"},
        {"id": "toys", "name": "ของเล่น", "icon": "🧸"},
        {"id": "pets", "name": "สัตว์เลี้ยง", "icon": "🐶"},
        {"id": "automotive", "name": "ยานยนต์", "icon": "🚗"},
    ]
    return jsonify(categories), 200
