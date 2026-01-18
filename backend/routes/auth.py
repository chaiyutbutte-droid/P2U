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

# ✅ Import Models
from models import User, Address, CartItem, Product

auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'static/uploads'


# -----------------------------
# 🛠 Helper Function: Save Image
# -----------------------------
def save_image(file, subfolder="misc"):
    """ฟังก์ชันช่วยบันทึกรูปภาพและคืนค่า URL"""
    if file:
        # ✅ รองรับไฟล์รูปภาพพื้นฐานและ webp
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        
        filename = secure_filename(file.filename)
        # 🔍 Debug Log
        print(f"DEBUG: Processing image upload: {filename}")

        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        
        if ext not in ALLOWED_EXTENSIONS:
            print(f"ERROR: Invalid file extension '{ext}'")
            raise ValueError(f"Invalid file type: .{ext} (Allowed: {', '.join(ALLOWED_EXTENSIONS)})")

        # สร้าง Path: static/uploads/subfolder
        folder_path = os.path.join(UPLOAD_FOLDER, subfolder)
        os.makedirs(folder_path, exist_ok=True)

        new_filename = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(folder_path, new_filename)
        file.save(save_path)
        
        return f"/{UPLOAD_FOLDER}/{subfolder}/{new_filename}"
    return None


# -----------------------------
# 📧 Function to send email
# -----------------------------
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

    # ใช้ Helper function บันทึกรูปโปรไฟล์
    if profile_image:
        try:
            profile_image_url = save_image(profile_image, subfolder="profiles") or ""
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400

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
    
    if not user.is_email_verified:
        return jsonify({"msg": "Please verify your email before logging in"}), 403

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
            "is_email_verified": user.is_email_verified,
            "shop_name": user.shop_name if user.is_seller else None
        }
    }), 200


# -----------------------------
# ✅ Register Seller Application (With eKYC Images) - FIXED 🔧
# -----------------------------
@auth.route('/register-seller-application', methods=['POST'])
@jwt_required()
def register_seller_application():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # ตรวจสอบอีเมลก่อนสมัคร
    if not user.is_email_verified:
        return jsonify({"msg": "Please verify your email before registering as a seller"}), 403
    
    # ตรวจสอบว่าเคยสมัครไปแล้วหรือยัง (เพื่อไม่ให้ส่งซ้ำ)
    if user.verification_status in ['PENDING', 'APPROVED']:
        return jsonify({"msg": "คุณได้ส่งคำขอสมัครร้านค้าไปแล้ว หรือเป็นร้านค้าอยู่แล้ว"}), 400

    # รับข้อมูล Text (FormData)
    shop_name = request.form.get('shop_name')
    phone_number = request.form.get('phone_number')
    id_card_number = request.form.get('id_card_number') # ✅ เพิ่มบรรทัดนี้: รับเลขบัตร ปชช.
    
    address_line = request.form.get('address_line')
    district = request.form.get('district')
    province = request.form.get('province')
    postal_code = request.form.get('postal_code')

    # รับไฟล์รูปภาพ
    id_front = request.files.get('id_front_image')
    id_back = request.files.get('id_back_image')
    selfie = request.files.get('selfie_image')

    # Debug: ดูข้อมูลที่รับมา
    print(f"DEBUG: Seller Reg - Shop: {shop_name}, ID: {id_card_number}, Files: Front={id_front}, Back={id_back}, Selfie={selfie}")

    # ✅ เพิ่ม id_card_number ในการตรวจสอบ
    if not all([shop_name, phone_number, id_card_number, address_line, district, province, postal_code, id_front, id_back, selfie]):
        return jsonify({"msg": "กรุณากรอกข้อมูลและอัปโหลดรูปภาพให้ครบถ้วน"}), 400

    try:
        # บันทึกรูป eKYC
        id_front_url = save_image(id_front, subfolder="ekyc")
        id_back_url = save_image(id_back, subfolder="ekyc")
        selfie_url = save_image(selfie, subfolder="ekyc")

        # อัปเดตข้อมูล User
        user.shop_name = shop_name
        user.phone_number = phone_number
        user.id_card_number = id_card_number # ✅ เพิ่มบรรทัดนี้: บันทึกลง DB
        
        # บันทึก URL รูปภาพลงฐานข้อมูล
        user.id_card_front_url = id_front_url
        user.id_card_back_url = id_back_url
        user.selfie_with_card_url = selfie_url
        
        # สร้าง Address ใหม่สำหรับร้านค้า
        new_address = Address(
            name=shop_name,
            phone=phone_number,
            address_line=address_line,
            district=district,
            province=province,
            postal_code=postal_code,
            is_default=True
        )
        user.addresses.append(new_address)

        # ----------------------------------------------------
        # 🔥 ตั้งสถานะเป็น PENDING และ is_seller=False
        # ----------------------------------------------------
        user.verification_status = 'PENDING'    # เพื่อให้ Admin เห็นใน Dashboard
        user.verification_date = datetime.utcnow() # เก็บเวลาที่ส่งเรื่อง
        user.is_seller = False                  # ยังไม่ให้เป็นผู้ขายจนกว่า Admin จะกดอนุมัติ

        user.save()

        return jsonify({"msg": "ส่งใบสมัครเรียบร้อยแล้ว กรุณารอแอดมินตรวจสอบ"}), 200

    except ValueError as e:
        # ✅ จับ Error เรื่องไฟล์โดยเฉพาะ และส่ง 400 (Bad Request)
        print(f"File Upload Error: {e}")
        return jsonify({"msg": str(e)}), 400

    except Exception as e:
        print(f"Error registering seller: {e}")
        return jsonify({"msg": f"เกิดข้อผิดพลาด: {str(e)}"}), 500


# -----------------------------
# ✅ Register as Seller (Old JSON Version - Optional)
# -----------------------------
@auth.route('/register-seller', methods=['POST'])
@jwt_required()
def register_seller():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not user.is_email_verified:
        return jsonify({"msg": "Please verify your email before registering as a seller"}), 403

    if user.is_seller:
        return jsonify({"msg": "User is already a seller"}), 400

    data = request.get_json()
    shop_name = data.get('shop_name')
    phone_number = data.get('phone_number')

    address_phone = data.get('address_phone')
    address_line = data.get('address_line')
    district = data.get('district')
    province = data.get('province')
    postal_code = data.get('postal_code')
    
    if not all([shop_name, address_line, district, province, postal_code]):
        return jsonify({"msg": "Required seller information is missing"}), 400

    new_address = Address(
        name=shop_name,
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
        "verification_status": user.verification_status, # ส่งสถานะกลับไปด้วยเพื่อแสดงผลที่หน้า Profile
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

    try:
        url = save_image(profile_image, subfolder="profiles")
        user.profile_image_url = url
        user.save()
        return jsonify({"profile_image_url": user.profile_image_url}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400


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

    try:
        product = Product.objects.get(id=ObjectId(product_id))
    except:
        return jsonify({"msg": "Product not found"}), 404

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

    try:
        product = Product.objects.get(id=ObjectId(product_id))
        in_wishlist = product in user.wishlist
    except:
        in_wishlist = False

    return jsonify({"in_wishlist": in_wishlist}), 200


# -----------------------------
# ✅ Get Cart
# -----------------------------
@auth.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.objects(user=ObjectId(user_id)).select_related()
    
    result = []
    for item in cart_items:
        p = item.product
        if p:
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
# ✅ Add to Cart
# -----------------------------
@auth.route('/cart/add/<product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    user_id = get_jwt_identity()
    
    cart_item = CartItem.objects(user=ObjectId(user_id), product=ObjectId(product_id)).first()
    
    if cart_item:
        cart_item.quantity = float(cart_item.quantity) + 1
        cart_item.save()
    else:
        new_item = CartItem(
            user=ObjectId(user_id),
            product=ObjectId(product_id),
            quantity=1
        )
        new_item.save()
        
    return jsonify({"msg": "เพิ่มสินค้าลงตะกร้าแล้ว ✨"}), 200