from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

# Import models
from models import User, Product, CartItem, Order, Address, TopupTransaction

# Import Blueprints
from routes.auth import auth
from routes.seller import seller
from routes.product import product
from routes.seller_rank import seller_rank  # <-- AI Ranking
from routes.coin import coin_bp  # <-- Coin / Topup
from routes.admin import admin  # <-- Admin
from routes.reviews import reviews  # <-- Reviews
from routes.notifications import notifications  # <-- Notifications
from routes.orders import orders  # <-- Orders
from routes.chat import chat  # <-- Chat
from routes.gamification import gamification  # <-- Gamification
from routes.recommendations import recommendations  # <-- AI Recommendations
from routes.auction import auction  # <-- Auction
from routes.price_analysis import price_analysis  # <-- Price Recommendation

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup Extensions
    # ✅ อนุญาต CORS สำหรับทุก API route / origin และ preflight requests
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:3000"]}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    JWTManager(app)

    # ปรับจากของเดิมเป็นแบบนี้
    CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:3000"]}}, # เปลี่ยนจาก /api/* เป็น /*
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"] # เพิ่ม headers ที่จำเป็น
    )

    # MongoDB Connection
    connect(
        db=app.config["MONGODB_SETTINGS"]["db"],
        host=app.config["MONGODB_SETTINGS"]["host"]
    )

    # Register Blueprints
    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(seller, url_prefix="/api")
    app.register_blueprint(product, url_prefix="/api")
    app.register_blueprint(seller_rank, url_prefix="/api")  # AI Ranking
    app.register_blueprint(coin_bp, url_prefix="/api")      # Coin / Topup
    app.register_blueprint(admin, url_prefix="/api")        # Admin
    app.register_blueprint(reviews, url_prefix="/api")      # Reviews
    app.register_blueprint(notifications, url_prefix="/api") # Notifications
    app.register_blueprint(orders, url_prefix="/api")       # Orders
    app.register_blueprint(chat, url_prefix="/api")         # Chat
    app.register_blueprint(gamification, url_prefix="/api")  # Gamification
    app.register_blueprint(recommendations, url_prefix="/api") # AI Recommendations
    app.register_blueprint(auction, url_prefix="/api")        # Auction
    app.register_blueprint(price_analysis, url_prefix="/api")  # Price Recommendation

    # Serve profile files
    @app.route('/static/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        return send_from_directory('static/uploads', filename)

    # Serve product images
    @app.route('/uploads/products/<path:filename>')
    def serve_product_image(filename):
        return send_from_directory('uploads/products', filename)

    return app

if __name__ == "__main__":
    app = create_app()
    # ✅ เปิด debug=True สำหรับ development และตั้ง port 5000
    app.run(debug=True, port=5000)
