from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

# Import models ที่ใช้ ReferenceField เพื่อป้องกัน NotRegistered
from models import User, Product, CartItem, Order, Note

#  Import Blueprints
from routes.auth import auth
from routes.notes import notes  # notes.py ของคุณ

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
    app.register_blueprint(notes, url_prefix="/api")  # ใช้ notes blueprint

    #  เสิร์ฟไฟล์โปรไฟล์จาก static/uploads/
    @app.route('/static/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        return send_from_directory('static/uploads', filename)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
