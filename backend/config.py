import os

class Config:
    # Flask app configuration
    SECRET_KEY = 'your-secret-key'

    # Database configuration (using MongoEngine)
    MONGODB_SETTINGS = {
        'db': 'P2Ukaiser',
        'host': 'mongodb://loeitech_admin_2:G7#u4sK!8zWb@202.29.231.188:27019/?authSource=admin'
    }

    # JWT configuration
    JWT_SECRET_KEY = 'your-jwt-secret'

    # Mail configuration for sending verification emails
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    
    # ✅ ใช้ App Password ที่สร้างจาก Google
    MAIL_USERNAME = 'chanidaphalanon2005@gmail.com'  # ✅ ใส่ email ของคุณ
    MAIL_PASSWORD = 'time smjt wzja ufnl'  # ✅ นำ App Password มาใส่ที่นี่
