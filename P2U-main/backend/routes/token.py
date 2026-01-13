from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime

from models import User, TokenRequest, Notification

token_bp = Blueprint('token', __name__)


# -----------------------------
# สร้างคำขอเติม Token
# -----------------------------
@token_bp.route('/token/request', methods=['POST'])
@jwt_required()
def create_token_request():
    """User creates a token top-up request"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    data = request.get_json()
    amount = data.get('amount')
    payment_proof_url = data.get('payment_proof_url', '')
    
    if not amount or amount <= 0:
        return jsonify({"msg": "กรุณาระบุจำนวน Token ที่ถูกต้อง"}), 400
    
    # สร้างคำขอ
    token_request = TokenRequest(
        user=user,
        amount=amount,
        payment_proof_url=payment_proof_url
    )
    token_request.save()
    
    return jsonify({
        "msg": "ส่งคำขอเติม Token สำเร็จ รอการอนุมัติจาก Admin",
        "request_id": str(token_request.id),
        "amount": amount,
        "status": "pending"
    }), 201


# -----------------------------
# ดูประวัติคำขอ Token ของตัวเอง
# -----------------------------
@token_bp.route('/token/my-requests', methods=['GET'])
@jwt_required()
def get_my_token_requests():
    """Get user's token request history"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    requests = TokenRequest.objects(user=user).order_by('-created_at')
    
    result = []
    for r in requests:
        result.append({
            "id": str(r.id),
            "amount": r.amount,
            "status": r.status,
            "payment_proof_url": r.payment_proof_url,
            "admin_note": r.admin_note,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "processed_at": r.processed_at.strftime("%Y-%m-%d %H:%M:%S") if r.processed_at else None
        })
    
    return jsonify({"requests": result}), 200


# -----------------------------
# ดูยอด Token คงเหลือ
# -----------------------------
@token_bp.route('/token/balance', methods=['GET'])
@jwt_required()
def get_token_balance():
    """Get user's token balance"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    return jsonify({
        "token_balance": user.token_balance or 0,
        "username": user.username
    }), 200
