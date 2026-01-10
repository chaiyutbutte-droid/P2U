from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from mongoengine.errors import ValidationError
from bson import ObjectId
import os
import uuid
import random
from datetime import datetime, timedelta

# ✅ เพิ่ม import ที่จำเป็นสำหรับส่งอีเมล
import smtplib
import ssl
from email.message import EmailMessage

# ✅ เพิ่ม import ที่จำเป็นสำหรับ JWT
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from models import User, Address

auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'static/uploads'
"print"


# Function to send email
def send_verification_email(recipient_email, verification_code):
    try:
        sender_email = current_app.config['MAIL_USERNAME']
        sender_password = current_app.config['MAIL_PASSWORD']
        
        # Email message setup
        msg = EmailMessage()
        msg['Subject'] = "Your Verification Code"
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.set_content(f"Hi there,\n\nYour verification code is: {verification_code}\n\nThis code is valid for 15 minutes.")
        
        # Connect to SMTP Server and send the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'], context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


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

    verification_code = ''.join(random.choices('0123456789', k=6))
    expiration_time = datetime.utcnow() + timedelta(minutes=15)
    
    hashed_pw = generate_password_hash(password)
    try:
        user = User(
            username=username,
            email=email,
            password=hashed_pw,
            full_name=full_name,
            phone_number=phone_number,
            is_seller=False,
            profile_image_url=profile_image_url,
            is_email_verified=False,
            email_verification_token=verification_code,
            email_verification_token_expiration=expiration_time
        )
        user.save()
    except ValidationError as e:
        return jsonify({"msg": str(e)}), 400

    send_verification_email(user.email, verification_code)
    
    return jsonify({"msg": "User registered successfully. Please check your email for the verification code."}), 201

# -----------------------------
# ✅ Verify Code
# -----------------------------
@auth.route('/verify-code', methods=['POST'])
def verify_email_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if not email or not code:
        return jsonify({"msg": "Email and code are required"}), 400

    user = User.objects(email=email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.is_email_verified:
        return jsonify({"msg": "Email is already verified"}), 200
    
    if user.email_verification_token == code and datetime.utcnow() < user.email_verification_token_expiration:
        user.is_email_verified = True
        user.email_verification_token = None
        user.email_verification_token_expiration = None
        user.save()
        return jsonify({"msg": "Email verified successfully"}), 200
    else:
        return jsonify({"msg": "Invalid or expired verification code"}), 400

# -----------------------------
# ✅ Resend Code
# -----------------------------
@auth.route('/resend-verification-code', methods=['POST'])
def resend_verification_code():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"msg": "Email is required"}), 400

    user = User.objects(email=email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.is_email_verified:
        return jsonify({"msg": "Email is already verified"}), 200

    new_code = ''.join(random.choices('0123456789', k=6))
    new_expiration = datetime.utcnow() + timedelta(minutes=15)
    
    user.email_verification_token = new_code
    user.email_verification_token_expiration = new_expiration
    user.save()
    
    send_verification_email(user.email, new_code)

    return jsonify({"msg": "A new verification code has been sent to your email."}), 200

# -----------------------------
# ✅ Login
# -----------------------------
@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"msg": "Invalid JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = User.objects(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401
    
    # ✅ ส่วนที่แก้ไข: เพิ่มการตรวจสอบสถานะการยืนยันอีเมลกลับมา
    if not user.is_email_verified:
        return jsonify({"msg": "Please verify your email before logging in"}), 403

    if not user.is_active:
        return jsonify({"msg": "Account is inactive"}), 403
    
    # ต้องมีการกำหนดค่า JWT_SECRET_KEY ใน config.py
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
            "is_email_verified": user.is_email_verified, # ✅ เพิ่ม field นี้เข้าไปใน response
            "shop_name": user.shop_name if user.is_seller else None
        }
    }), 200

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

    # Check if the email is verified before allowing seller registration
    if not user.is_email_verified:
        return jsonify({"msg": "Please verify your email before registering as a seller"}), 403

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
        "is_email_verified": user.is_email_verified,
        "coin_balance": user.coin_balance,
        "token_balance": user.token_balance,
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

    user.profile_image_url = f"/{UPLOAD_FOLDER}/{new_filename}"
    user.save()

    return jsonify({"profile_image_url": user.profile_image_url}), 200


# -----------------------------
# ✅ Get Wishlist
# -----------------------------
@auth.route('/wishlist', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = get_jwt_identity()
    try:
        user = User.objects(id=ObjectId(user_id)).first()
    except (ValidationError, TypeError):
        return jsonify({"msg": "Invalid user ID"}), 400

    if not user:
        return jsonify({"msg": "User not found"}), 404

    from models import Product
    wishlist_items = []
    for product_ref in user.wishlist:
        try:
            if product_ref:
                wishlist_items.append({
                    "id": str(product_ref.id),
                    "name": product_ref.name,
                    "description": product_ref.description,
                    "price": float(product_ref.price),
                    "image_url": product_ref.image_url,
                    "seller": {
                        "id": str(product_ref.seller.id),
                        "username": product_ref.seller.username,
                        "shop_name": product_ref.seller.shop_name
                    } if product_ref.seller else None
                })
        except:
            continue

    return jsonify({
        "wishlist": wishlist_items,
        "total": len(wishlist_items)
    }), 200


# -----------------------------
# ✅ Add to Wishlist
# -----------------------------
@auth.route('/wishlist/<product_id>', methods=['POST'])
@jwt_required()
def add_to_wishlist(product_id):
    user_id = get_jwt_identity()
    try:
        user = User.objects(id=ObjectId(user_id)).first()
    except (ValidationError, TypeError):
        return jsonify({"msg": "Invalid user ID"}), 400

    if not user:
        return jsonify({"msg": "User not found"}), 404

    from models import Product
    try:
        product = Product.objects.get(id=ObjectId(product_id))
    except:
        return jsonify({"msg": "Product not found"}), 404

    # Check if already in wishlist
    if product in user.wishlist:
        return jsonify({"msg": "Product already in wishlist"}), 400

    user.wishlist.append(product)
    user.save()

    return jsonify({"msg": "Added to wishlist"}), 201


# -----------------------------
# ✅ Remove from Wishlist
# -----------------------------
@auth.route('/wishlist/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(product_id):
    user_id = get_jwt_identity()
    try:
        user = User.objects(id=ObjectId(user_id)).first()
    except (ValidationError, TypeError):
        return jsonify({"msg": "Invalid user ID"}), 400

    if not user:
        return jsonify({"msg": "User not found"}), 404

    from models import Product
    try:
        product = Product.objects.get(id=ObjectId(product_id))
    except:
        return jsonify({"msg": "Product not found"}), 404

    if product not in user.wishlist:
        return jsonify({"msg": "Product not in wishlist"}), 400

    user.wishlist.remove(product)
    user.save()

    return jsonify({"msg": "Removed from wishlist"}), 200


# -----------------------------
# ✅ Check if in Wishlist
# -----------------------------
@auth.route('/wishlist/<product_id>/check', methods=['GET'])
@jwt_required()
def check_wishlist(product_id):
    user_id = get_jwt_identity()
    try:
        user = User.objects(id=ObjectId(user_id)).first()
    except (ValidationError, TypeError):
        return jsonify({"msg": "Invalid user ID"}), 400

    if not user:
        return jsonify({"msg": "User not found"}), 404

    from models import Product
    try:
        product = Product.objects.get(id=ObjectId(product_id))
        in_wishlist = product in user.wishlist
    except:
        in_wishlist = False

    return jsonify({"in_wishlist": in_wishlist}), 200

# -----------------------------
# ✅ Get Cart (ดึงตะกร้าของฉัน)
# -----------------------------
@auth.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    # ดึง CartItem ทั้งหมดที่เป็นของ User คนนี้
    # ใช้ .select_related() เพื่อดึงข้อมูลสินค้า (Product) มาทีเดียวเลย
    cart_items = CartItem.objects(user=ObjectId(user_id)).select_related()
    
    result = []
    for item in cart_items:
        p = item.product
        if p: # เช็คเผื่อสินค้าโดนลบไปแล้ว
            result.append({
                "cart_item_id": str(item.id),
                "id": str(p.id),
                "name": p.name,
                "price": float(p.price),
                "description": p.description,
                "image_url": p.image_url,
                "quantity": int(item.quantity),
                "seller": {
                    "shop_name": p.seller.shop_name if p.seller else "ร้านค้าทั่วไป"
                }
            })
            
    return jsonify({"cart": result}), 200

# -----------------------------
# ✅ Add to Cart (เพิ่ม/อัปเดตจำนวน)
# -----------------------------
@auth.route('/cart/add/<product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    user_id = get_jwt_identity()
    
    # ตรวจสอบว่ามีสินค้านี้ในตะกร้าของ User คนนี้หรือยัง
    cart_item = CartItem.objects(user=ObjectId(user_id), product=ObjectId(product_id)).first()
    
    if cart_item:
        # ถ้ามีแล้ว ให้บวกจำนวนเพิ่มไป 1
        cart_item.quantity = float(cart_item.quantity) + 1
        cart_item.save()
    else:
        # ถ้ายังไม่มี ให้สร้างใหม่
        new_item = CartItem(
            user=ObjectId(user_id),
            product=ObjectId(product_id),
            quantity=1
        )
        new_item.save()
        
    return jsonify({"msg": "เพิ่มสินค้าลงตะกร้าแล้ว ✨"}), 200