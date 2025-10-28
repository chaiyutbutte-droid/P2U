from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, TopupTransaction
from utils.omise_client import OmiseClient
from datetime import datetime
import hmac
import hashlib
import base64
import os

coin_bp = Blueprint('coin', __name__)

# -----------------------------
# ✅ สร้างคำขอเติม Coin (สร้าง Charge)
# -----------------------------
@coin_bp.route('/coin/topup', methods=['POST'])
@jwt_required()
def create_coin_charge():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    data = request.get_json()
    amount = data.get("amount")
    payment_method = data.get("payment_method", "promptpay")  # 'promptpay' หรือ 'credit'
    card_token = data.get("card_token")  # สำหรับ credit

    if not amount or amount <= 0:
        return jsonify({"status": "error", "message": "Invalid amount"}), 400

    try:
        if payment_method == "promptpay":
            result = OmiseClient.create_charge_promptpay(amount)
        elif payment_method == "credit":
            if not card_token:
                return jsonify({"status": "error", "message": "Card token required"}), 400
            result = OmiseClient.create_charge_credit(amount, card_token)
        else:
            return jsonify({"status": "error", "message": "Invalid payment method"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    if result.get("status") == "error":
        return jsonify(result), 500

    charge_data = result["data"]

    # ✅ บันทึกลงฐานข้อมูล
    transaction = TopupTransaction(
        user=user,
        amount=amount,
        charge_id=charge_data.id,
        payment_method=payment_method,
        status=charge_data.status,
        created_at=datetime.utcnow()
    ).save()

    return jsonify({
        "status": "success",
        "charge_id": charge_data.id,
        "payment_method": payment_method,
        "amount": amount,
        "charge_data": charge_data
    }), 200

# -----------------------------
# ✅ Webhook จาก Omise พร้อม Signature Verification
# -----------------------------
@coin_bp.route('/coin/webhook/omise', methods=['POST'])
def omise_webhook():
    payload = request.get_data()
    signature = request.headers.get("Omise-Signature")

    webhook_secret = os.getenv("OMISE_WEBHOOK_SECRET")
    if not webhook_secret:
        return jsonify({"status": "error", "message": "Webhook secret not configured"}), 500

    # ✅ ตรวจสอบ Signature
    computed_signature = hmac.new(
        webhook_secret.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_signature, signature):
        return jsonify({"status": "error", "message": "Signature verification failed"}), 400

    # แปลง payload เป็น JSON
    try:
        event = request.get_json()
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    if not event or 'data' not in event:
        return jsonify({"status": "error", "message": "Invalid webhook format"}), 400

    charge = event['data']
    charge_id = charge['id']
    status = charge['status']

    # ✅ หา Transaction
    transaction = TopupTransaction.objects(charge_id=charge_id).first()
    if not transaction:
        return jsonify({"status": "error", "message": "Transaction not found"}), 404

    # ✅ อัปเดตสถานะ
    transaction.status = status
    transaction.save()

    # ✅ ถ้าจ่ายสำเร็จ เพิ่ม Coin ให้ User
    if status == "successful":
        user = transaction.user
        user.coin_balance += transaction.amount
        user.save()

    return jsonify({"status": "success", "message": "Webhook processed"}), 200

# -----------------------------
# ✅ ดูยอด Coin ของผู้ใช้
# -----------------------------
@coin_bp.route('/coin/balance', methods=['GET'])
@jwt_required()
def coin_balance():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    return jsonify({"status": "success", "coin_balance": user.coin_balance}), 200

# -----------------------------
# ✅ ดูประวัติการเติมเงิน
# -----------------------------
@coin_bp.route('/coin/history', methods=['GET'])
@jwt_required()
def coin_history():
    user_id = get_jwt_identity()
    transactions = TopupTransaction.objects(user=user_id).order_by('-created_at')

    data = [{
        "amount": t.amount,
        "status": t.status,
        "payment_method": t.payment_method,
        "created_at": t.created_at
    } for t in transactions]

    return jsonify({"status": "success", "history": data}), 200
