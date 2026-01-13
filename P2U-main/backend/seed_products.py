"""
Product Seed Script - UNIQUE IMAGES ONLY
Each product has a unique image, no duplicates
"""
import sys
sys.path.insert(0, '.')

from models import User, Product
from werkzeug.security import generate_password_hash
from mongoengine import connect
from config import Config

# Connect to MongoDB
connect(db=Config.MONGODB_SETTINGS["db"], host=Config.MONGODB_SETTINGS["host"])

# Get or create demo seller
demo_seller = User.objects(username="P2UKAISER_Shop").first()
if not demo_seller:
    demo_seller = User(
        username="P2UKAISER_Shop",
        email="shop@p2ukaiser.com",
        password=generate_password_hash("shop123"),
        full_name="P2UKAISER Official Shop",
        is_seller=True,
        shop_name="P2UKAISER Official",
        is_email_verified=True
    )
    demo_seller.save()

# Delete existing products
Product.objects.delete()
print("Deleted existing products")

# Each product has ONE UNIQUE IMAGE - no duplicates!
products_with_unique_images = [
    # Electronics (4 unique images)
    {"name": "iPhone 16 Pro Max 256GB", "price": 49900, "category": "electronics", 
     "description": "สมาร์ทโฟนรุ่นล่าสุด จอ 6.7 นิ้ว กล้อง 48MP ชิป A18 Pro",
     "image_url": "/static/products/product_iphone_1766769641862.png"},
    
    {"name": "Sony WH-1000XM5", "price": 12990, "category": "electronics", 
     "description": "หูฟังไร้สาย Noise Cancelling คุณภาพระดับพรีเมียม",
     "image_url": "/static/products/product_headphones_1766769657879.png"},
    
    {"name": "Apple Watch Ultra 2", "price": 31900, "category": "electronics", 
     "description": "สมาร์ทวอทช์สำหรับนักผจญภัย GPS + LTE แบตอึด",
     "image_url": "/static/products/product_watch_1766769694809.png"},
    
    {"name": "MacBook Pro M3 14 นิ้ว", "price": 89900, "category": "electronics", 
     "description": "โน้ตบุ๊คประสิทธิภาพสูง ชิป M3 Pro RAM 18GB",
     "image_url": "/static/products/product_macbook_1766770139240.png"},

    # Fashion (4 unique images)
    {"name": "Nike Air Max Pink", "price": 4590, "category": "fashion", 
     "description": "รองเท้าวิ่งสุดเท่ น้ำหนักเบา ดีไซน์สวย",
     "image_url": "/static/products/product_sneakers_1766769676542.png"},
    
    {"name": "Minimalist Backpack", "price": 1990, "category": "fashion", 
     "description": "กระเป๋าเป้สไตล์มินิมอล กันน้ำ ใส่โน๊ตบุ๊คได้",
     "image_url": "/static/products/product_backpack_1766769712117.png"},
    
    {"name": "เสื้อยืด Oversized Premium", "price": 590, "category": "fashion", 
     "description": "เสื้อยืดผ้าคอตตอน 100% สวมสบาย มีหลายสี",
     "image_url": "/static/products/product_tshirt_1766770253429.png"},
    
    {"name": "ชุดเดรสดอกไม้ Summer", "price": 1290, "category": "fashion", 
     "description": "เดรสลายดอกไม้ ใส่สบาย เหมาะกับหน้าร้อน",
     "image_url": "/static/products/product_dress_1766771324315.png"},

    # Gaming (3 unique images)
    {"name": "Razer DeathAdder V3 Pro", "price": 4990, "category": "gaming", 
     "description": "เมาส์เกมมิ่งไร้สาย เซนเซอร์ 30K DPI RGB",
     "image_url": "/static/products/product_gaming_mouse_1766769731233.png"},
    
    {"name": "PlayStation 5 Slim Bundle", "price": 18990, "category": "gaming", 
     "description": "เครื่องเล่นเกมรุ่นใหม่ พร้อมคอนโทรลเลอร์ DualSense",
     "image_url": "/static/products/product_ps5_1766770153698.png"},
    
    {"name": "Razer BlackWidow V4 RGB", "price": 5990, "category": "gaming", 
     "description": "คีย์บอร์ด Mechanical RGB Full-size สวิตช์เขียว",
     "image_url": "/static/products/product_gaming_keyboard_1766771305375.png"},

    # Beauty (2 unique images)
    {"name": "ลิปสติก MAC Ruby Woo", "price": 890, "category": "beauty", 
     "description": "ลิปสติกสีแดงคลาสสิค เนื้อแมท ติดทน",
     "image_url": "/static/products/product_lipstick_1766770192997.png"},
    
    {"name": "Luxury Skincare Set", "price": 2990, "category": "beauty", 
     "description": "เซ็ตบำรุงผิวพรีเมียม เซรั่มและครีมบำรุง",
     "image_url": "/static/products/product_skincare_1766771344171.png"},

    # Home (2 unique images)
    {"name": "กระทะไฟฟ้า Premium", "price": 1290, "category": "home", 
     "description": "กระทะไฟฟ้าเคลือบเซรามิก ทำอาหารง่าย",
     "image_url": "/static/products/product_pan_1766770209597.png"},
    
    {"name": "โซฟา Modern 3 ที่นั่ง", "price": 12990, "category": "home", 
     "description": "โซฟาผ้านั่งสบาย สไตล์โมเดิร์น",
     "image_url": "/static/products/product_sofa_1766771370494.png"},

    # Sports (2 unique images)
    {"name": "ลูกฟุตบอล Adidas Pro", "price": 990, "category": "sports", 
     "description": "ลูกฟุตบอลหนัง PU คุณภาพสูง เบอร์ 5",
     "image_url": "/static/products/product_football_1766770226683.png"},
    
    {"name": "เสื่อโยคะ Premium TPE", "price": 890, "category": "sports", 
     "description": "เสื่อโยคะ TPE หนา 8 มม. กันลื่น พร้อมสาย",
     "image_url": "/static/products/product_yoga_mat_1766771386990.png"},

    # Pets (1 unique image)
    {"name": "อาหารสุนัข Royal Canin Premium", "price": 1290, "category": "pets", 
     "description": "อาหารสุนัขพรีเมียม สูตรบำรุงขน 5 กก.",
     "image_url": "/static/products/product_dog_food_1766771404479.png"},
]

# Create products
created = 0
for p in products_with_unique_images:
    product = Product(
        name=p["name"],
        description=p["description"],
        price=p["price"],
        category=p["category"],
        image_url=p["image_url"],
        seller=demo_seller
    )
    product.save()
    created += 1

print(f"Created {created} products with UNIQUE images!")
print("Categories:")
from collections import Counter
cats = Counter([p["category"] for p in products_with_unique_images])
for cat, count in cats.items():
    print(f"  - {cat}: {count} products")
