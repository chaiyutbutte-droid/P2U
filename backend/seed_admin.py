
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import User
from werkzeug.security import generate_password_hash
from mongoengine import connect
from config import Config

# Connect to MongoDB
connect(db=Config.MONGODB_SETTINGS["db"], host=Config.MONGODB_SETTINGS["host"])

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def seed_admin():
    # Check if admin exists
    admin_user = User.objects(username=ADMIN_USERNAME).first()
    
    if admin_user:
        print(f"Updating existing admin user '{ADMIN_USERNAME}'...")
        admin_user.password = generate_password_hash(ADMIN_PASSWORD)
        admin_user.is_admin = True
        admin_user.is_seller = False # Admin shouldn't necessarily be a seller, but can be
        admin_user.save()
        print("Admin user updated successfully.")
    else:
        print(f"Creating new admin user '{ADMIN_USERNAME}'...")
        admin_user = User(
            username=ADMIN_USERNAME,
            email="admin@p2ukaiser.com",
            password=generate_password_hash(ADMIN_PASSWORD),
            full_name="Administrator",
            is_admin=True,
            is_email_verified=True,
            is_seller=False
        )
        admin_user.save()
        print("Admin user created successfully.")

if __name__ == "__main__":
    seed_admin()
