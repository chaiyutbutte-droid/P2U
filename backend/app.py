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
from routes.seller_rank import seller_rank
from routes.coin import coin_bp
from routes.admin import admin
from routes.reviews import reviews
from routes.notifications import notifications
from routes.orders import orders
from routes.chat import chat
from routes.gamification import gamification
from routes.recommendations import recommendations
from routes.auction import auction
from routes.price_analysis import price_analysis
from routes.token import token_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Setup Extensions ---
    
    # ✅ แก้ไขการตั้งค่า CORS ให้ถูกต้องเพียงจุดเดียว
    # รองรับทั้ง GET, POST, PUT, DELETE และ OPTIONS (Preflight)
    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000"]}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )
    
    JWTManager(app)

    # --- MongoDB Connection ---
    connect(
        db=app.config["MONGODB_SETTINGS"]["db"],
        host=app.config["MONGODB_SETTINGS"]["host"]
    )

    # --- Register Blueprints ---
    # หมายเหตุ: ทุกเส้นทางจะเริ่มต้นด้วย /api เช่น /api/orders/...
    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(seller, url_prefix="/api")
    app.register_blueprint(product, url_prefix="/api")
    app.register_blueprint(seller_rank, url_prefix="/api")
    app.register_blueprint(coin_bp, url_prefix="/api")
    app.register_blueprint(admin, url_prefix="/api")
    app.register_blueprint(reviews, url_prefix="/api")
    app.register_blueprint(notifications, url_prefix="/api")
    app.register_blueprint(orders, url_prefix="/api")
    app.register_blueprint(chat, url_prefix="/api")
    app.register_blueprint(gamification, url_prefix="/api")
    app.register_blueprint(recommendations, url_prefix="/api")
    app.register_blueprint(auction, url_prefix="/api")
    app.register_blueprint(price_analysis, url_prefix="/api")
    app.register_blueprint(token_bp, url_prefix="/api")

    # --- Static File Routes ---
    @app.route('/static/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        return send_from_directory('static/uploads', filename)

    @app.route('/uploads/products/<path:filename>')
    def serve_product_image(filename):
        return send_from_directory('uploads/products', filename)

    # Route สำหรับ serve รูปสลิป
    @app.route('/uploads/slips/<path:filename>')
    def serve_slip_image(filename):
        return send_from_directory('uploads/slips', filename)

    return app

if __name__ == "__main__":
    app = create_app()
    # เปิด debug=True เพื่อให้โค้ดอัปเดตอัตโนมัติขณะพัฒนา
    app.run(debug=True, port=5000)