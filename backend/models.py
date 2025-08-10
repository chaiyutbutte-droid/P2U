from mongoengine import (
    Document, StringField, EmailField, BooleanField, DateTimeField,
    ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField, CASCADE
)
from datetime import datetime

class Address(EmbeddedDocument):
    name = StringField(required=True)
    phone = StringField(required=True)
    address_line = StringField(required=True)
    district = StringField(required=True)
    province = StringField(required=True)
    postal_code = StringField(required=True)
    is_default = BooleanField(default=False)

class Product(Document):
    name = StringField(required=True)
    description = StringField()
    price = StringField(required=True)
    image_url = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'products'}

class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_image_url = StringField(default=None)

    full_name = StringField(required=True)
    phone_number = StringField()
    addresses = ListField(EmbeddedDocumentField(Address))

    is_seller = BooleanField(default=False)
    # ✅ เพิ่มฟิลด์ shop_name เพื่อเก็บชื่อร้านของผู้ขาย
    shop_name = StringField() 
    
    is_active = BooleanField(default=True)
    is_verified = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    # ลบ reverse_delete_rule ใน ListField เหล่านี้
    wishlist = ListField(ReferenceField('Product'))
    cart_items = ListField(ReferenceField('CartItem'))
    orders = ListField(ReferenceField('Order'))

    meta = {'collection': 'users'}

class CartItem(Document):
    product = ReferenceField('Product', required=True, reverse_delete_rule=CASCADE)
    quantity = StringField(required=True)
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    added_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'cart_items'}

class Order(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    items = ListField(ReferenceField('CartItem', reverse_delete_rule=CASCADE))
    total_price = StringField(required=True)
    status = StringField(default='pending')
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'orders'}

class Note(Document):
    title = StringField(required=True)
    content = StringField(default='')
    image_url = StringField(default=None)
    created_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField('User', reverse_delete_rule=CASCADE, required=True)
    meta = {'collection': 'notes'}