from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
from models import User, SellerRankingHistory
import numpy as np

seller_rank = Blueprint('seller_rank', __name__)


# ========= Enhanced Scoring Algorithm =========
def calculate_advanced_seller_score(seller):
    """
    Advanced scoring with weighted factors:
    - Sales performance (25%)
    - Customer rating (25%)
    - Delivery speed (15%)
    - Response rate (15%)
    - Cancel rate penalty (10%)
    - Verification bonus (10%)
    """
    weights = {
        'sales': 0.25,
        'rating': 0.25,
        'delivery': 0.15,
        'response': 0.15,
        'cancel': 0.10,
        'verification': 0.10
    }
    
    # Normalize values (0-100 scale)
    sales_score = min(100, (seller.total_sales / 100000) * 100) if seller.total_sales else 0
    rating_score = (seller.rating_avg / 5) * 100 if seller.rating_avg else 0
    delivery_score = max(0, 100 - (seller.delivery_speed * 10)) if seller.delivery_speed else 50
    response_score = seller.response_rate * 100 if seller.response_rate else 0
    cancel_penalty = max(0, 100 - (seller.cancel_rate * 200)) if seller.cancel_rate else 100
    
    # Verification bonus
    verification_score = 0
    if seller.is_email_verified:
        verification_score += 30
    if seller.is_phone_verified:
        verification_score += 30
    if seller.is_id_verified:
        verification_score += 40
    
    # Calculate weighted score
    final_score = (
        sales_score * weights['sales'] +
        rating_score * weights['rating'] +
        delivery_score * weights['delivery'] +
        response_score * weights['response'] +
        cancel_penalty * weights['cancel'] +
        verification_score * weights['verification']
    )
    
    return round(final_score, 2)


def assign_level(score):
    """Assign tier level based on score"""
    if score >= 90:
        return "S"
    elif score >= 75:
        return "A"
    elif score >= 60:
        return "B"
    else:
        return "C"


def get_level_badge(level):
    """Get badge info for level"""
    badges = {
        'S': {'icon': '🥇', 'name': 'Top Seller', 'color': '#FFD700'},
        'A': {'icon': '⭐', 'name': 'Star Seller', 'color': '#C0C0C0'},
        'B': {'icon': '✓', 'name': 'Verified Seller', 'color': '#CD7F32'},
        'C': {'icon': '📦', 'name': 'Basic Seller', 'color': '#808080'}
    }
    return badges.get(level, badges['C'])


# ========= Update Seller Rank =========
@seller_rank.route('/seller/rank/update', methods=['POST'])
@jwt_required()
def update_seller_rank():
    """Update current seller's ranking score"""
    user_id = get_jwt_identity()
    seller = User.objects(id=ObjectId(user_id), is_seller=True).first()
    if not seller:
        return jsonify({"msg": "ไม่พบข้อมูลผู้ขาย"}), 404

    score = calculate_advanced_seller_score(seller)
    level = assign_level(score)
    badge = get_level_badge(level)

    # Update seller
    old_level = seller.ai_level
    seller.ai_score = score
    seller.ai_level = level
    seller.save()

    # Record history
    all_sellers = User.objects(is_seller=True).order_by('-ai_score')
    rank_position = 1
    for i, s in enumerate(all_sellers):
        if str(s.id) == user_id:
            rank_position = i + 1
            break
    
    SellerRankingHistory(
        seller=seller,
        score=score,
        level=level,
        rank_position=rank_position,
        total_sales=seller.total_sales,
        rating_avg=seller.rating_avg
    ).save()

    return jsonify({
        "msg": "อัปเดตอันดับสำเร็จ",
        "seller": {
            "shop_name": seller.shop_name,
            "ai_score": seller.ai_score,
            "ai_level": seller.ai_level,
            "badge": badge,
            "rank_position": rank_position,
            "level_changed": old_level != level
        }
    }), 200


# ========= Get Seller Leaderboard =========
@seller_rank.route('/seller/rank/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get seller leaderboard with pagination and filters"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    level_filter = request.args.get('level', None)
    
    query = User.objects(is_seller=True)
    
    if level_filter:
        query = query.filter(ai_level=level_filter.upper())
    
    total = query.count()
    sellers = query.order_by('-ai_score').skip((page - 1) * per_page).limit(per_page)
    
    leaderboard = []
    for i, s in enumerate(sellers):
        rank = (page - 1) * per_page + i + 1
        badge = get_level_badge(s.ai_level)
        
        leaderboard.append({
            "rank": rank,
            "id": str(s.id),
            "shop_name": s.shop_name or s.username,
            "profile_image": s.profile_image_url,
            "ai_score": s.ai_score,
            "ai_level": s.ai_level,
            "badge": badge,
            "rating_avg": s.rating_avg,
            "total_sales": s.total_sales,
            "is_verified": s.is_id_verified,
            "is_phone_verified": s.is_phone_verified
        })
    
    return jsonify({
        "leaderboard": leaderboard,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page
        }
    }), 200


# ========= Get All Seller Rankings (Legacy) =========
@seller_rank.route('/seller/rank/all', methods=['GET'])
def get_all_seller_rankings():
    """Legacy endpoint for all seller rankings"""
    sellers = User.objects(is_seller=True).order_by('-ai_score')
    return jsonify([
        {
            "id": str(s.id),
            "shop_name": s.shop_name or s.username,
            "ai_score": s.ai_score,
            "ai_level": s.ai_level,
            "badge": get_level_badge(s.ai_level),
            "rating_avg": s.rating_avg,
            "total_sales": s.total_sales
        } for s in sellers
    ])


# ========= Get Seller Rank History =========
@seller_rank.route('/seller/rank/history/<seller_id>', methods=['GET'])
def get_seller_history(seller_id):
    """Get ranking history for a seller"""
    try:
        history = SellerRankingHistory.objects(
            seller=ObjectId(seller_id)
        ).order_by('-recorded_at').limit(30)
        
        return jsonify({
            "seller_id": seller_id,
            "history": [{
                "score": h.score,
                "level": h.level,
                "rank_position": h.rank_position,
                "total_sales": h.total_sales,
                "rating_avg": h.rating_avg,
                "recorded_at": h.recorded_at.isoformat()
            } for h in history]
        }), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


# ========= Get Single Seller Details =========
@seller_rank.route('/seller/rank/<seller_id>', methods=['GET'])
def get_seller_rank_details(seller_id):
    """Get detailed ranking info for a seller"""
    try:
        seller = User.objects(id=ObjectId(seller_id), is_seller=True).first()
        if not seller:
            return jsonify({"msg": "ไม่พบผู้ขาย"}), 404
        
        # Get rank position
        all_sellers = User.objects(is_seller=True).order_by('-ai_score')
        rank_position = 1
        for i, s in enumerate(all_sellers):
            if str(s.id) == seller_id:
                rank_position = i + 1
                break
        
        badge = get_level_badge(seller.ai_level)
        
        # Score breakdown
        score_breakdown = {
            "sales": min(100, (seller.total_sales / 100000) * 100) if seller.total_sales else 0,
            "rating": (seller.rating_avg / 5) * 100 if seller.rating_avg else 0,
            "delivery": max(0, 100 - (seller.delivery_speed * 10)) if seller.delivery_speed else 50,
            "response": seller.response_rate * 100 if seller.response_rate else 0,
            "cancel": max(0, 100 - (seller.cancel_rate * 200)) if seller.cancel_rate else 100,
            "verification": (30 if seller.is_email_verified else 0) + 
                          (30 if seller.is_phone_verified else 0) +
                          (40 if seller.is_id_verified else 0)
        }
        
        return jsonify({
            "id": str(seller.id),
            "shop_name": seller.shop_name or seller.username,
            "profile_image": seller.profile_image_url,
            "ai_score": seller.ai_score,
            "ai_level": seller.ai_level,
            "badge": badge,
            "rank_position": rank_position,
            "total_sellers": all_sellers.count(),
            "rating_avg": seller.rating_avg,
            "total_sales": seller.total_sales,
            "score_breakdown": score_breakdown,
            "verification": {
                "email": seller.is_email_verified,
                "phone": seller.is_phone_verified,
                "id_card": seller.is_id_verified
            }
        }), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

