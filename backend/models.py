# models.py
from mongoengine import (
    Document, StringField, EmailField, BooleanField, DateTimeField,
    ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField,
    DecimalField, CASCADE
)
from datetime import datetime

# -------- Address Model --------
# โมเดลสำหรับที่อยู่ ซึ่งจะถูกฝังอยู่ในโมเดล User
class Address(EmbeddedDocument):
    name = StringField(required=True)
    phone = StringField(required=True)
    address_line = StringField(required=True)
    district = StringField(required=True)
    province = StringField(required=True)
    postal_code = StringField(required=True)
    is_default = BooleanField(default=False)

# -------- User Model --------
# โมเดลหลักสำหรับผู้ใช้, ผู้ซื้อ, และผู้ขาย
class User(Document):
    username = StringField(required=True, unique=True, min_length=4, max_length=20)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_image_url = StringField()

    full_name = StringField(required=True)
    phone_number = StringField()
    addresses = ListField(EmbeddedDocumentField(Address))

    is_seller = BooleanField(default=False)
    shop_name = StringField()
    
    is_active = BooleanField(default=True)
    is_email_verified = BooleanField(default=False)
    email_verification_token = StringField()
    email_verification_token_expiration = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)

    # เก็บรายการสินค้าที่ผู้ใช้สนใจ (wishlist)
    wishlist = ListField(ReferenceField('Product'))
    
    # cart_items และ orders จะใช้การ query จาก collection ของตัวเอง
    # ไม่ต้องเก็บเป็น ListField ใน User model เพื่อลดความซ้ำซ้อนและเพิ่มประสิทธิภาพ
    meta = {'collection': 'users'}


# -------- Product Model --------
# โมเดลสำหรับสินค้า
class Product(Document):
    name = StringField(required=True, max_length=100)
    description = StringField()
    # ✅ เปลี่ยนเป็น DecimalField สำหรับการคำนวณราคาที่ถูกต้อง
    price = DecimalField(required=True, min_value=0)
    image_url = StringField()
    # ✅ เพิ่ม ReferenceField เพื่อเชื่อมโยงสินค้ากับผู้ขาย (User)
    seller = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'products'}

# -------- CartItem Model --------
# โมเดลสำหรับรายการสินค้าในตะกร้า
class CartItem(Document):
    product = ReferenceField('Product', required=True)
    # ✅ เปลี่ยนเป็น DecimalField สำหรับการคำนวณจำนวนสินค้าที่ถูกต้อง
    quantity = DecimalField(required=True, min_value=1)
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    added_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'cart_items'}


# -------- Order Model --------
# โมเดลสำหรับคำสั่งซื้อ
class Order(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    # items เก็บรายการสินค้าในตะกร้า (CartItem) ที่อ้างอิงถึง
    items = ListField(ReferenceField('CartItem'))
    # ✅ เปลี่ยนเป็น DecimalField สำหรับการคำนวณราคารวมที่ถูกต้อง
    total_price = DecimalField(required=True, min_value=0)
    status = StringField(default='pending')
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'orders'}