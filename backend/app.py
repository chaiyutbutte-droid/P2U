from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config


# ✅ Import models that use ReferenceField to prevent NotRegistered

from models import User, Product, CartItem, Order, Note

#  Import Blueprints
from routes.auth import auth
from routes.seller import seller # <-- Imported the seller blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #  Setup Extensions
    CORS(app)
    JWTManager(app)

    #  MongoDB Connection
    connect(
        db=app.config["MONGODB_SETTINGS"]["db"],
        host=app.config["MONGODB_SETTINGS"]["host"]
    )

    #  Register Blueprints
    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(seller, url_prefix="/api") # <-- Registered the seller blueprint

    # ✅ Serve profile files from static/uploads/
    @app.route('/static/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        return send_from_directory('static/uploads', filename)

    # ✅ Serve product images from uploads/products/
    @app.route('/uploads/products/<path:filename>')
    def serve_product_image(filename):
        return send_from_directory('uploads/products', filename)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)