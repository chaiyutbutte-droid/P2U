from mongoengine import (
    Document, StringField, EmailField, BooleanField, DateTimeField,
    ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField,
    DecimalField, FloatField, CASCADE, IntField
)
from datetime import datetime


# -------- Topup Transaction Model (Embedded) --------
class TopupTransaction(EmbeddedDocument):
    transaction_id = StringField(required=True)
    method = StringField(required=True, choices=["omise", "promptpay", "truemoney"])
    amount = IntField(required=True)  # จำนวนเงิน (บาท) = Coin
    status = StringField(default='pending', choices=["pending", "success", "failed"])
    created_at = DateTimeField(default=datetime.utcnow)


# -------- Address Model --------
class Address(EmbeddedDocument):
    name = StringField(required=True)
    phone = StringField(required=True)
    address_line = StringField(required=True)
    district = StringField(required=True)
    province = StringField(required=True)
    postal_code = StringField(required=True)
    is_default = BooleanField(default=False)


# -------- User Model --------
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

    # Wishlist ของผู้ใช้
    wishlist = ListField(ReferenceField('Product'))

    # ===== ระบบ Coin =====
    coin_balance = IntField(default=0)  # ยอด coin คงเหลือ
    topup_transactions = ListField(EmbeddedDocumentField(TopupTransaction))

    # ===== ฟิลด์สำหรับ AI Ranking =====
    total_sales = FloatField(default=0.0)        # ยอดขายรวม
    rating_avg = FloatField(default=0.0)         # คะแนนเฉลี่ย
    delivery_speed = FloatField(default=0.0)     # วันเฉลี่ยต่อการจัดส่ง
    response_rate = FloatField(default=0.0)      # อัตราการตอบลูกค้า
    cancel_rate = FloatField(default=0.0)        # อัตราการยกเลิก
    ai_score = FloatField(default=0.0)           # คะแนนจาก AI
    ai_level = StringField(default="C")          # ระดับ (S, A, B, C)

    meta = {'collection': 'users'}


# -------- Product Model --------
class Product(Document):
    name = StringField(required=True, max_length=100)
    description = StringField()
    price = DecimalField(required=True, min_value=0)
    image_url = StringField()
    seller = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'products'}


# -------- CartItem Model --------
class CartItem(Document):
    product = ReferenceField('Product', required=True)
    quantity = DecimalField(required=True, min_value=1)
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    added_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'cart_items'}


# -------- Order Model --------
class Order(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    items = ListField(ReferenceField('CartItem'))
    total_price = DecimalField(required=True, min_value=0)
    status = StringField(default='pending')
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'orders'}
