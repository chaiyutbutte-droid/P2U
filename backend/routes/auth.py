from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from mongoengine.errors import ValidationError
from bson import ObjectId
import os
import uuid

from models import User, Address

auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'static/uploads'

# -----------------------------
# ✅ Register
# -----------------------------
@auth.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    phone_number = request.form.get('phone_number')

    # ลบ is_seller ออกจาก form data ที่นี่
    # is_seller = request.form.get('is_seller', 'false').lower() == 'true'

    address_name = request.form.get('address_name')
    address_phone = request.form.get('address_phone')
    address_line = request.form.get('address_line')
    district = request.form.get('district')
    province = request.form.get('province')
    postal_code = request.form.get('postal_code')

    profile_image = request.files.get('profile_image')
    profile_image_url = ""

    if not all([username, email, password, full_name]):
        return jsonify({"msg": "Required fields are missing"}), 400

    if User.objects(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    if User.objects(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    if profile_image:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        filename = secure_filename(profile_image.filename)
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if ext not in ALLOWED_EXTENSIONS:
            return jsonify({"msg": "Invalid image file type"}), 400

        new_filename = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(UPLOAD_FOLDER, new_filename)
        profile_image.save(save_path)
        profile_image_url = f"/{UPLOAD_FOLDER}/{new_filename}"

    addresses = []
    if address_line and district and province and postal_code:
        addresses.append(Address(
            name=address_name or full_name,
            phone=address_phone or phone_number,
            address_line=address_line,
            district=district,
            province=province,
            postal_code=postal_code,
            is_default=True
        ))

    hashed_pw = generate_password_hash(password)
    try:
        user = User(
            username=username,
            email=email,
            password=hashed_pw,
            full_name=full_name,
            phone_number=phone_number,
            is_seller=False, # ตั้งค่า is_seller เป็น False เสมอ
            profile_image_url=profile_image_url,
            addresses=addresses
        )
        user.save()
    except ValidationError as e:
        return jsonify({"msg": str(e)}), 400

    return jsonify({"msg": "User registered successfully"}), 201

# -----------------------------
# ✅ Register as Seller
# -----------------------------
@auth.route('/register-seller', methods=['POST'])
@jwt_required()
def register_seller():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.is_seller:
        return jsonify({"msg": "User is already a seller"}), 400

    data = request.get_json()
    shop_name = data.get('shop_name')
    full_name = data.get('full_name')
    phone_number = data.get('phone_number')

    address_name = data.get('address_name')
    address_phone = data.get('address_phone')
    address_line = data.get('address_line')
    district = data.get('district')
    province = data.get('province')
    postal_code = data.get('postal_code')
    
    if not all([shop_name, full_name, address_line, district, province, postal_code]):
        return jsonify({"msg": "Required seller information is missing"}), 400

    new_address = Address(
        name=address_name or full_name,
        phone=address_phone or phone_number,
        address_line=address_line,
        district=district,
        province=province,
        postal_code=postal_code,
        is_default=True
    )
    
    try:
        user.is_seller = True
        user.shop_name = shop_name
        user.full_name = full_name
        user.phone_number = phone_number
        user.addresses.append(new_address)
        user.save()
        
        return jsonify({"msg": "Seller registration successful"}), 200
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500


# -----------------------------
# ✅ Login
# -----------------------------
@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"msg": "Invalid JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = User.objects(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"msg": "Account is inactive"}), 403

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "access_token": token,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "profile_image_url": user.profile_image_url or "",
            "is_seller": user.is_seller,
            "shop_name": user.shop_name if user.is_seller else None
        }
    }), 200

# -----------------------------
# ✅ Profile
# -----------------------------
@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    try:
        user = User.objects(id=ObjectId(user_id)).first()
    except (ValidationError, TypeError):
        return jsonify({"msg": "Invalid user ID"}), 400

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "phone_number": user.phone_number,
        "profile_image_url": user.profile_image_url or "",
        "is_seller": user.is_seller,
        "shop_name": user.shop_name if user.is_seller else None,
        "addresses": [
            {
                "name": addr.name,
                "phone": addr.phone,
                "address_line": addr.address_line,
                "district": addr.district,
                "province": addr.province,
                "postal_code": addr.postal_code,
                "is_default": addr.is_default
            } for addr in user.addresses
        ]
    }), 200

# -----------------------------
# ✅ Update Profile Image
# -----------------------------
@auth.route('/profile/image', methods=['PUT'])
@jwt_required()
def update_profile_image():
    user_id = get_jwt_identity()
    try:
        user = User.objects(id=ObjectId(user_id)).first()
    except (ValidationError, TypeError):
        return jsonify({"msg": "Invalid user ID"}), 400

    if not user:
        return jsonify({"msg": "User not found"}), 404

    profile_image = request.files.get('profile_image')
    if not profile_image:
        return jsonify({"msg": "No image file provided"}), 400

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    filename = secure_filename(profile_image.filename)
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"msg": "Invalid image file type"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(UPLOAD_FOLDER, new_filename)
    profile_image.save(save_path)

    # Optionally, delete old image here if needed

    user.profile_image_url = f"/{UPLOAD_FOLDER}/{new_filename}"
    user.save()

    return jsonify({"profile_image_url": user.profile_image_url}), 200