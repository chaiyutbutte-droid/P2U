from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Product, User # Assuming you have a Product and User model
from mongoengine import Document, ReferenceField, StringField, DecimalField, IntField
from bson import ObjectId
import os
import uuid
from werkzeug.utils import secure_filename

# Create a new Blueprint for seller routes
seller = Blueprint('seller', __name__)

# --- Constants for file upload ---
UPLOAD_FOLDER = 'uploads/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# New function to save the uploaded image with a unique filename
def save_image(image_file):
    if image_file and allowed_file(image_file.filename):
        # Generate a unique filename using UUID
        ext = image_file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        image_file.save(file_path)
        return f'/{UPLOAD_FOLDER}/{unique_filename}'
    return None

# --- Seller API Routes ---

# 🔸 Get all products for the current seller
@seller.route('/seller/products', methods=['GET'])
@jwt_required()
def get_seller_products():
    """
    Retrieves all products listed by the current authenticated seller.
    """
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    # Check if the user is a seller before allowing access
    if not user or not user.is_seller:
        return jsonify({"msg": "Unauthorized. This action requires seller privileges."}), 403

    products = Product.objects(user=user).order_by('-created_at')
    
    return jsonify([
        {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "stock_quantity": product.stock_quantity,
            "image_url": product.image_url,
            "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for product in products
    ])

# 🔸 Add a new product
@seller.route('/seller/products', methods=['POST'])
@jwt_required()
def add_product():
    """
    Adds a new product for the current seller.
    Requires product details and handles image upload.
    """
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not user or not user.is_seller:
        return jsonify({"msg": "Unauthorized. This action requires seller privileges."}), 403

    data = request.form
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    stock_quantity = data.get('stock_quantity', 0)
    
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
            stock_quantity=int(stock_quantity),
            image_url=image_url,
            user=user
        )
        product.save()
        return jsonify({"msg": "Product added successfully!", "product_id": str(product.id)}), 201
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

# 🔸 Get a single product by ID
@seller.route('/seller/products/<product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """
    Retrieves a single product by its ID.
    Only allows access if the current user is the product's seller.
    """
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    try:
        product = Product.objects.get(id=ObjectId(product_id), user=user)
    except Product.DoesNotExist:
        return jsonify({"msg": "Product not found or unauthorized access."}), 404
    except Exception:
        return jsonify({"msg": "Invalid product ID."}), 400

    return jsonify({
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "price": float(product.price),
        "stock_quantity": product.stock_quantity,
        "image_url": product.image_url
    })

# 🔸 Update a product by ID
@seller.route('/seller/products/<product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """
    Updates an existing product.
    Only the seller can update their own products.
    """
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    try:
        product = Product.objects.get(id=ObjectId(product_id), user=user)
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
    if 'stock_quantity' in data:
        update_fields['stock_quantity'] = int(data['stock_quantity'])

    product.update(**update_fields)
    return jsonify({"msg": "Product updated successfully!"})

# 🔸 Delete a product by ID
@seller.route('/seller/products/<product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """
    Deletes a product by its ID.
    Only the seller can delete their own products.
    """
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    try:
        product = Product.objects.get(id=ObjectId(product_id), user=user)
        # Optional: Delete the image file from the server
        if product.image_url and os.path.exists(product.image_url.lstrip('/')):
            os.remove(product.image_url.lstrip('/'))
        product.delete()
        return jsonify({"msg": "Product deleted successfully!"}), 200
    except Product.DoesNotExist:
        return jsonify({"msg": "Product not found or unauthorized access."}), 404
    except Exception:
        return jsonify({"msg": "Invalid product ID."}), 400

# 🔸 Update product image
@seller.route('/seller/products/<product_id>/image', methods=['PUT'])
@jwt_required()
def update_product_image(product_id):
    """
    Updates the image of an existing product.
    """
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    try:
        product = Product.objects.get(id=ObjectId(product_id), user=user)
    except Product.DoesNotExist:
        return jsonify({"msg": "Product not found or unauthorized access."}), 404
    except Exception:
        return jsonify({"msg": "Invalid product ID."}), 400
    
    if 'image' not in request.files:
        return jsonify({"msg": "No image file provided."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"msg": "No selected file."}), 400

    # Delete old image if it exists
    if product.image_url and os.path.exists(product.image_url.lstrip('/')):
        os.remove(product.image_url.lstrip('/'))
        
    new_image_url = save_image(file)
    if new_image_url:
        product.update(image_url=new_image_url)
        return jsonify({"msg": "Image updated successfully.", "image_url": new_image_url}), 200
    else:
        return jsonify({"msg": "Invalid file type."}), 400