from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from models import User
from sklearn.preprocessing import MinMaxScaler
import numpy as np

seller_rank = Blueprint('seller_rank', __name__)

# ========= ฟังก์ชันคำนวณคะแนน =========
def calculate_seller_score(seller):
    data = np.array([[seller.total_sales,
                      seller.rating_avg,
                      -seller.delivery_speed,  # ยิ่งเร็วยิ่งดี
                      seller.response_rate,
                      -seller.cancel_rate]])    # ยิ่งน้อยยิ่งดี

    scaler = MinMaxScaler()
    score = scaler.fit_transform(data)
    return round(np.mean(score) * 100, 2)

def assign_level(score):
    if score >= 90:
        return "S"
    elif score >= 75:
        return "A"
    elif score >= 60:
        return "B"
    else:
        return "C"

# ========= Endpoint อัปเดตคะแนนผู้ขาย =========
@seller_rank.route('/seller/rank/update', methods=['POST'])
@jwt_required()
def update_seller_rank():
    user_id = get_jwt_identity()
    seller = User.objects(id=ObjectId(user_id), is_seller=True).first()
    if not seller:
        return jsonify({"msg": "Seller not found"}), 404

    score = calculate_seller_score(seller)
    level = assign_level(score)

    seller.ai_score = score
    seller.ai_level = level
    seller.save()

    return jsonify({
        "msg": "Seller ranking updated successfully",
        "seller": {
            "shop_name": seller.shop_name,
            "ai_score": seller.ai_score,
            "ai_level": seller.ai_level
        }
    }), 200

# ========= Endpoint ดูอันดับผู้ขายทั้งหมด =========
@seller_rank.route('/seller/rank/all', methods=['GET'])
def get_all_seller_rankings():
    sellers = User.objects(is_seller=True).order_by('-ai_score')
    return jsonify([
        {
            "shop_name": s.shop_name,
            "ai_score": s.ai_score,
            "ai_level": s.ai_level,
            "rating_avg": s.rating_avg,
            "total_sales": s.total_sales
        } for s in sellers
    ])
