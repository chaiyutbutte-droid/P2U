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
    is_admin = BooleanField(default=False)
    shop_name = StringField()
    
    is_active = BooleanField(default=True)
    is_email_verified = BooleanField(default=False)
    email_verification_token = StringField()
    email_verification_token_expiration = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)

    wishlist = ListField(ReferenceField('Product'))

    # ===== ระบบ Coin =====
    coin_balance = IntField(default=0)
    token_balance = IntField(default=0)  # เพิ่ม field นี้เพื่อให้ตรงกับ DB
    topup_transactions = ListField(EmbeddedDocumentField(TopupTransaction))

    # ===== ฟิลด์สำหรับ AI Ranking =====
    total_sales = FloatField(default=0.0)
    rating_avg = FloatField(default=0.0)
    delivery_speed = FloatField(default=0.0)
    response_rate = FloatField(default=0.0)
    cancel_rate = FloatField(default=0.0)
    ai_score = FloatField(default=0.0)
    ai_level = StringField(default="C")

    # ===== Gamification =====
    member_level = StringField(default="Bronze", choices=["Bronze", "Silver", "Gold", "Diamond"])
    xp = IntField(default=0)
    check_in_streak = IntField(default=0)
    last_check_in = DateTimeField()
    total_spent = FloatField(default=0.0)

    # ===== Identity Verification =====
    is_phone_verified = BooleanField(default=False)
    phone_verification_code = StringField()
    phone_verification_expiry = DateTimeField()
    is_id_verified = BooleanField(default=False)
    id_card_front_url = StringField()
    id_card_back_url = StringField()
    verification_date = DateTimeField()

    meta = {'collection': 'users'}

# -------- Product Model --------
class Product(Document):
    name = StringField(required=True, max_length=100)
    description = StringField()
    price = DecimalField(required=True, min_value=0)
    image_url = StringField()
    images = ListField(StringField())
    video_url = StringField()
    view_360_images = ListField(StringField())
    category = StringField(default='all')
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
    # ✅ เพิ่ม choices เพื่อป้องกันการเก็บค่าสถานะที่ผิดพลาด
    status = StringField(default='pending', choices=['pending', 'paid', 'processing', 'completed', 'cancelled'])
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'orders'}

# -------- Review Model --------
class Review(Document):
    product = ReferenceField('Product', required=True, reverse_delete_rule=CASCADE)
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    rating = IntField(required=True, min_value=1, max_value=5)
    comment = StringField(max_length=500)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'reviews'}

# -------- Notification Model --------
class Notification(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    title = StringField(required=True)
    message = StringField(required=True)
    # ✅ แก้ไข: เพิ่ม 'order_update' เข้าไปใน choices เพื่อแก้ปัญหา ValidationError
    type = StringField(default='info', choices=['info', 'order', 'order_update', 'review', 'promo', 'system'])
    is_read = BooleanField(default=False)
    link = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'notifications'}

# -------- Conversation Model (Chat) --------
class Conversation(Document):
    participants = ListField(ReferenceField('User'), required=True)
    last_message = StringField()
    last_message_at = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'conversations'}

# -------- Message Model (Chat) --------
class Message(Document):
    conversation = ReferenceField('Conversation', required=True, reverse_delete_rule=CASCADE)
    sender = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    content = StringField(required=True, max_length=1000)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'messages'}

# -------- Mission Model --------
class Mission(Document):
    title = StringField(required=True)
    description = StringField()
    type = StringField(required=True, choices=['daily', 'weekly', 'achievement'])
    requirement_type = StringField(required=True, choices=['check_in', 'purchase', 'spend', 'review', 'order_count'])
    requirement_value = IntField(required=True)
    xp_reward = IntField(default=0)
    coin_reward = IntField(default=0)
    is_active = BooleanField(default=True)
    meta = {'collection': 'missions'}

# -------- UserMission Model --------
class UserMission(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    mission = ReferenceField('Mission', required=True, reverse_delete_rule=CASCADE)
    progress = IntField(default=0)
    is_completed = BooleanField(default=False)
    is_claimed = BooleanField(default=False)
    completed_at = DateTimeField()
    claimed_at = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'user_missions'}

# -------- Auction Model --------
class Auction(Document):
    title = StringField(required=True, max_length=200)
    description = StringField()
    image_url = StringField()
    category = StringField(default='all')
    starting_price = DecimalField(required=True, min_value=0)
    current_price = DecimalField(required=True, min_value=0)
    min_bid_increment = DecimalField(default=10)
    seller = ReferenceField('User', required=True)
    winner = ReferenceField('User')
    start_time = DateTimeField(default=datetime.utcnow)
    end_time = DateTimeField(required=True)
    is_active = BooleanField(default=True)
    is_ended = BooleanField(default=False)
    total_bids = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'auctions'}

# -------- AuctionBid Model --------
class AuctionBid(Document):
    auction = ReferenceField('Auction', required=True, reverse_delete_rule=CASCADE)
    bidder = ReferenceField('User', required=True)
    amount = DecimalField(required=True, min_value=0)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'auction_bids', 'ordering': ['-created_at']}

# -------- AutoBid Model (Auction Enhancement) --------
class AutoBid(Document):
    auction = ReferenceField('Auction', required=True, reverse_delete_rule=CASCADE)
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    max_amount = DecimalField(required=True, min_value=0)
    current_bid = DecimalField(default=0)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'auto_bids'}

# -------- Seller Ranking History --------
class SellerRankingHistory(Document):
    seller = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    score = FloatField(required=True)
    level = StringField(required=True)
    rank_position = IntField()
    total_sales = FloatField(default=0.0)
    rating_avg = FloatField(default=0.0)
    recorded_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'seller_ranking_history', 'ordering': ['-recorded_at']}

# -------- Price Statistics (for Price Recommendation) --------
class PriceStatistics(Document):
    category = StringField(required=True, unique=True)
    avg_price = FloatField(default=0.0)
    min_price = FloatField(default=0.0)
    max_price = FloatField(default=0.0)
    median_price = FloatField(default=0.0)
    total_products = IntField(default=0)
    updated_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'price_statistics'}

# -------- Token Request Model (Admin Approval) --------
class TokenRequest(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    amount = IntField(required=True)  # จำนวน Token ที่ต้องการ
    payment_proof_url = StringField()  # หลักฐานการชำระเงิน (optional)
    status = StringField(default='pending', choices=['pending', 'approved', 'rejected'])
    admin_note = StringField()  # หมายเหตุจาก admin
    approved_by = ReferenceField('User')  # Admin ที่อนุมัติ
    created_at = DateTimeField(default=datetime.utcnow)
    processed_at = DateTimeField()
    meta = {'collection': 'token_requests', 'ordering': ['-created_at']}