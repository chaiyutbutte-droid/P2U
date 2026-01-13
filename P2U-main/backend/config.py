import os

class Config:
    # -------------------------------
    #  🔐 Flask Security
    # -------------------------------
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-jwt-secret')

    # -------------------------------
    #  📦 MongoDB
    # -------------------------------
    MONGODB_SETTINGS = {
        'db': 'P2Ukaiser',
        'host': 'mongodb://loeitech_admin_2:G7#u4sK!8zWb@202.29.231.188:27019/?authSource=admin'
    }

    # -------------------------------
    #  ✉ Email (Gmail SMTP + App Password)
    # -------------------------------
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'p2ukaiser.official@gmail.com'
    MAIL_PASSWORD = 'aitr khdo ffkn ngqd'  # ใช้ App Password เท่านั้น!

    # -------------------------------
    #  💰 Coin System
    # -------------------------------
    TOPUP_COIN_RATE = 100  # 1 บาท = 100 Coin

    # -------------------------------
    #  📲 PromptPay QR Payment
    # -------------------------------
    PROMPTPAY_ID = "0655747752"  # ✅ เบอร์โทร/เลข PromptPay ที่ใช้รับเงินจริง
    PROMPTPAY_REF_CODE = "P2U"   # ✅ Reference Code ใน QR (เพื่อดูว่าใครเติม)

    # -------------------------------
    #  🧧 TrueMoney Wallet API
    # -------------------------------
    TRUEMONEY_PARTNER_ID = "YOUR_PARTNER_ID"
    TRUEMONEY_PARTNER_SECRET = "YOUR_PARTNER_SECRET"
    TRUEMONEY_CALLBACK_URL = "https://yourdomain.com/api/truemoney/callback"

    # -------------------------------
    #  💳 Omise Payment Gateway
    # -------------------------------
    OMISE_PUBLIC_KEY = os.getenv("OMISE_PUBLIC_KEY", "pkey_test_xxxx")
    OMISE_SECRET_KEY = os.getenv("OMISE_SECRET_KEY", "skey_test_xxxx")
    OMISE_API_VERSION = "2020-05-29"
    OMISE_CURRENCY = "thb"
    OMISE_RETURN_URL = os.getenv("OMISE_RETURN_URL", "https://yourdomain.com/payment/success")
    OMISE_WEBHOOK_SECRET = os.getenv("OMISE_WEBHOOK_SECRET", "whsec_xxxx")  # สำหรับเช็ค Signature

    # -------------------------------
    # 🔔 Frontend URL (ใช้ Redirect / Email Verification / Payment Success)
    # -------------------------------
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://your-frontend-domain.com")
