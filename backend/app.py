from flask import Flask, send_from_directory ,jsonify , send_file
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config
import cv2
import numpy as np
from io import BytesIO

# Import models
from models import User, Product, CartItem, Order, Address, TopupTransaction

# Import Blueprints
from routes.auth import auth
from routes.seller import seller
from routes.product import product
from routes.seller_rank import seller_rank  # <-- AI Ranking
from routes.coin import coin_bp  # <-- Coin / Topup



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup Extensions
    # ✅ อนุญาต CORS สำหรับทุก API route / origin และ preflight requests
    CORS(
        app,
        resources={r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ]
        }},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        expose_headers=["Content-Type", "Authorization"]
    )
    JWTManager(app)

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
