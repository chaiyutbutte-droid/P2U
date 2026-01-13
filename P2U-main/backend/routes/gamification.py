from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime, timedelta

from models import User, Mission, UserMission, Notification

gamification = Blueprint('gamification', __name__)


# -----------------------------
# Daily Check-in
# -----------------------------
@gamification.route('/check-in', methods=['POST'])
@jwt_required()
def daily_check_in():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    today = datetime.utcnow().date()
    
    # Check if already checked in today
    if user.last_check_in:
        last_check_in_date = user.last_check_in.date()
        if last_check_in_date == today:
            return jsonify({"msg": "Already checked in today"}), 400
        
        # Check streak
        yesterday = today - timedelta(days=1)
        if last_check_in_date == yesterday:
            user.check_in_streak += 1
        else:
            user.check_in_streak = 1
    else:
        user.check_in_streak = 1
    
    # Calculate coin reward based on streak
    base_coins = 5
    streak_bonus = min(user.check_in_streak, 7) * 2  # Max 14 extra coins
    total_coins = base_coins + streak_bonus
    
    # Streak milestones
    milestone_bonus = 0
    if user.check_in_streak == 7:
        milestone_bonus = 50
    elif user.check_in_streak == 30:
        milestone_bonus = 200
    
    total_coins += milestone_bonus
    
    # Update user
    user.last_check_in = datetime.utcnow()
    user.coin_balance += total_coins
    user.save()
    
    # Update missions progress
    update_mission_progress(user, 'check_in', 1)
    
    return jsonify({
        "msg": "Check-in successful!",
        "coins_earned": total_coins,
        "streak": user.check_in_streak,
        "milestone_bonus": milestone_bonus,
        "total_coins": user.coin_balance
    }), 200


# -----------------------------
# Get Check-in Status
# -----------------------------
@gamification.route('/check-in/status', methods=['GET'])
@jwt_required()
def check_in_status():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    today = datetime.utcnow().date()
    can_check_in = True
    
    if user.last_check_in:
        last_check_in_date = user.last_check_in.date()
        can_check_in = last_check_in_date != today
    
    return jsonify({
        "can_check_in": can_check_in,
        "streak": user.check_in_streak,
        "last_check_in": user.last_check_in.strftime("%Y-%m-%d") if user.last_check_in else None,
        "coin_balance": user.coin_balance
    }), 200


# -----------------------------
# Get Available Missions
# -----------------------------
@gamification.route('/missions', methods=['GET'])
@jwt_required()
def get_missions():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    # Get active missions
    missions = Mission.objects(is_active=True)
    
    result = []
    for mission in missions:
        # Get or create user mission
        user_mission = UserMission.objects(user=user, mission=mission).first()
        if not user_mission:
            user_mission = UserMission(user=user, mission=mission, progress=0)
            user_mission.save()
        
        result.append({
            "id": str(mission.id),
            "title": mission.title,
            "description": mission.description,
            "type": mission.type,
            "requirement_type": mission.requirement_type,
            "requirement_value": mission.requirement_value,
            "coin_reward": mission.coin_reward,
            "progress": user_mission.progress,
            "is_completed": user_mission.is_completed,
            "is_claimed": user_mission.is_claimed
        })
    
    return jsonify({"missions": result}), 200


# -----------------------------
# Claim Mission Reward
# -----------------------------
@gamification.route('/missions/<mission_id>/claim', methods=['POST'])
@jwt_required()
def claim_mission(mission_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    try:
        mission = Mission.objects.get(id=ObjectId(mission_id))
    except:
        return jsonify({"msg": "Mission not found"}), 404
    
    user_mission = UserMission.objects(user=user, mission=mission).first()
    
    if not user_mission or not user_mission.is_completed:
        return jsonify({"msg": "Mission not completed"}), 400
    
    if user_mission.is_claimed:
        return jsonify({"msg": "Reward already claimed"}), 400
    
    # Award coins only
    user.coin_balance += mission.coin_reward
    user.save()
    
    # Mark as claimed
    user_mission.is_claimed = True
    user_mission.claimed_at = datetime.utcnow()
    user_mission.save()
    
    return jsonify({
        "msg": "Reward claimed!",
        "coins_earned": mission.coin_reward,
        "total_coins": user.coin_balance
    }), 200


# -----------------------------
# Helper: Update Mission Progress
# -----------------------------
def update_mission_progress(user, requirement_type, value):
    """Update all relevant missions for a user"""
    missions = Mission.objects(requirement_type=requirement_type, is_active=True)
    
    for mission in missions:
        user_mission = UserMission.objects(user=user, mission=mission).first()
        if not user_mission:
            user_mission = UserMission(user=user, mission=mission, progress=0)
        
        if not user_mission.is_completed:
            user_mission.progress += value
            if user_mission.progress >= mission.requirement_value:
                user_mission.is_completed = True
                user_mission.completed_at = datetime.utcnow()
                
                # Notify user
                Notification(
                    user=user,
                    title="🎯 ภารกิจสำเร็จ!",
                    message=f"คุณทำภารกิจ '{mission.title}' สำเร็จแล้ว! รับ {mission.coin_reward} Coins",
                    type="promo",
                    link="/missions"
                ).save()
            
            user_mission.save()


# -----------------------------
# Seed Default Missions (Coins only)
# -----------------------------
@gamification.route('/missions/seed', methods=['POST'])
def seed_missions():
    """Create default missions if none exist"""
    # Delete old missions to recreate
    Mission.objects.delete()
    
    default_missions = [
        # Daily
        {"title": "📅 เช็คอินประจำวัน", "description": "เช็คอินรับ Coins", "type": "daily", "requirement_type": "check_in", "requirement_value": 1, "xp_reward": 0, "coin_reward": 10},
        {"title": "🛒 ซื้อสินค้า 1 ชิ้น", "description": "สั่งซื้อสินค้าใดก็ได้ 1 ชิ้น", "type": "daily", "requirement_type": "order_count", "requirement_value": 1, "xp_reward": 0, "coin_reward": 25},
        {"title": "⭐ เขียนรีวิว", "description": "เขียนรีวิวสินค้าที่ซื้อ", "type": "daily", "requirement_type": "review", "requirement_value": 1, "xp_reward": 0, "coin_reward": 15},
        # Weekly
        {"title": "💰 ใช้จ่าย 500 บาท", "description": "ซื้อสินค้ารวม 500 บาท", "type": "weekly", "requirement_type": "spend", "requirement_value": 500, "xp_reward": 0, "coin_reward": 75},
        {"title": "📦 สั่งซื้อ 3 ครั้ง", "description": "สั่งซื้อสินค้า 3 ครั้ง", "type": "weekly", "requirement_type": "order_count", "requirement_value": 3, "xp_reward": 0, "coin_reward": 100},
        # Achievement
        {"title": "🎖️ นักช้อปมือใหม่", "description": "ซื้อสินค้าครั้งแรก", "type": "achievement", "requirement_type": "purchase", "requirement_value": 1, "xp_reward": 0, "coin_reward": 50},
        {"title": "💎 ใช้จ่าย 5,000 บาท", "description": "ใช้จ่ายสะสม 5,000 บาท", "type": "achievement", "requirement_type": "spend", "requirement_value": 5000, "xp_reward": 0, "coin_reward": 300},
    ]
    
    for m in default_missions:
        Mission(**m).save()
    
    return jsonify({"msg": f"Created {len(default_missions)} missions (Coins only)"}), 201
