from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from mongoengine.errors import DoesNotExist

from models import User, Notification

notifications = Blueprint('notifications', __name__)


# -----------------------------
# Get User Notifications
# -----------------------------
@notifications.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        notifs = Notification.objects(user=user).order_by('-created_at')
        
        result = []
        unread_count = 0
        for n in notifs:
            if not n.is_read:
                unread_count += 1
            result.append({
                "id": str(n.id),
                "title": n.title,
                "message": n.message,
                "type": n.type,
                "is_read": n.is_read,
                "link": n.link,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return jsonify({
            "notifications": result,
            "unread_count": unread_count,
            "total": len(result)
        }), 200
        
    except DoesNotExist:
        return jsonify({"msg": "User not found"}), 404


# -----------------------------
# Mark Notification as Read
# -----------------------------
@notifications.route('/notifications/<notif_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notif_id):
    user_id = get_jwt_identity()
    
    try:
        notif = Notification.objects.get(id=ObjectId(notif_id))
        
        if str(notif.user.id) != user_id:
            return jsonify({"msg": "Unauthorized"}), 403
        
        notif.is_read = True
        notif.save()
        
        return jsonify({"msg": "Notification marked as read"}), 200
        
    except DoesNotExist:
        return jsonify({"msg": "Notification not found"}), 404


# -----------------------------
# Mark All as Read
# -----------------------------
@notifications.route('/notifications/read-all', methods=['PUT'])
@jwt_required()
def mark_all_as_read():
    user_id = get_jwt_identity()
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        Notification.objects(user=user, is_read=False).update(set__is_read=True)
        
        return jsonify({"msg": "All notifications marked as read"}), 200
        
    except DoesNotExist:
        return jsonify({"msg": "User not found"}), 404


# -----------------------------
# Delete Notification
# -----------------------------
@notifications.route('/notifications/<notif_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notif_id):
    user_id = get_jwt_identity()
    
    try:
        notif = Notification.objects.get(id=ObjectId(notif_id))
        
        if str(notif.user.id) != user_id:
            return jsonify({"msg": "Unauthorized"}), 403
        
        notif.delete()
        return jsonify({"msg": "Notification deleted"}), 200
        
    except DoesNotExist:
        return jsonify({"msg": "Notification not found"}), 404


# -----------------------------
# Clear All Notifications
# -----------------------------
@notifications.route('/notifications/clear', methods=['DELETE'])
@jwt_required()
def clear_notifications():
    user_id = get_jwt_identity()
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        Notification.objects(user=user).delete()
        
        return jsonify({"msg": "All notifications cleared"}), 200
        
    except DoesNotExist:
        return jsonify({"msg": "User not found"}), 404
