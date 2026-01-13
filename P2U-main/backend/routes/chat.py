from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from datetime import datetime

from models import User, Conversation, Message

chat = Blueprint('chat', __name__)


# -----------------------------
# Get User's Conversations
# -----------------------------
@chat.route('/chat/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    user_id = get_jwt_identity()
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        conversations = Conversation.objects(participants=user).order_by('-last_message_at')
        
        result = []
        for conv in conversations:
            # Get the other participant
            other_user = None
            for p in conv.participants:
                if str(p.id) != user_id:
                    other_user = p
                    break
            
            # Count unread messages
            unread = Message.objects(conversation=conv, sender__ne=user, is_read=False).count()
            
            result.append({
                "id": str(conv.id),
                "other_user": {
                    "id": str(other_user.id),
                    "username": other_user.username,
                    "profile_image_url": other_user.profile_image_url,
                    "shop_name": other_user.shop_name
                } if other_user else None,
                "last_message": conv.last_message,
                "last_message_at": conv.last_message_at.strftime("%Y-%m-%d %H:%M:%S") if conv.last_message_at else None,
                "unread_count": unread
            })
        
        return jsonify({
            "conversations": result,
            "total": len(result)
        }), 200
        
    except DoesNotExist:
        return jsonify({"msg": "User not found"}), 404


# -----------------------------
# Get Messages in a Conversation
# -----------------------------
@chat.route('/chat/<conversation_id>', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    user_id = get_jwt_identity()
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        conv = Conversation.objects.get(id=ObjectId(conversation_id))
        
        # Check if user is participant
        if user not in conv.participants:
            return jsonify({"msg": "Unauthorized"}), 403
        
        messages = Message.objects(conversation=conv).order_by('created_at')
        
        # Mark messages as read
        Message.objects(conversation=conv, sender__ne=user, is_read=False).update(set__is_read=True)
        
        result = []
        for msg in messages:
            result.append({
                "id": str(msg.id),
                "sender": {
                    "id": str(msg.sender.id),
                    "username": msg.sender.username,
                    "profile_image_url": msg.sender.profile_image_url
                },
                "content": msg.content,
                "is_read": msg.is_read,
                "is_mine": str(msg.sender.id) == user_id,
                "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Get other user info
        other_user = None
        for p in conv.participants:
            if str(p.id) != user_id:
                other_user = p
                break
        
        return jsonify({
            "messages": result,
            "conversation_id": str(conv.id),
            "other_user": {
                "id": str(other_user.id),
                "username": other_user.username,
                "profile_image_url": other_user.profile_image_url,
                "shop_name": other_user.shop_name
            } if other_user else None
        }), 200
        
    except DoesNotExist:
        return jsonify({"msg": "Conversation not found"}), 404


# -----------------------------
# Send a Message
# -----------------------------
@chat.route('/chat', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    recipient_id = data.get('recipient_id')
    content = data.get('content')
    
    if not recipient_id or not content:
        return jsonify({"msg": "Recipient and content are required"}), 400
    
    try:
        sender = User.objects.get(id=ObjectId(user_id))
        recipient = User.objects.get(id=ObjectId(recipient_id))
        
        # Find or create conversation
        conv = Conversation.objects(
            participants__all=[sender, recipient],
            participants__size=2
        ).first()
        
        if not conv:
            conv = Conversation(
                participants=[sender, recipient],
                created_at=datetime.utcnow()
            )
            conv.save()
        
        # Create message
        message = Message(
            conversation=conv,
            sender=sender,
            content=content
        )
        message.save()
        
        # Update conversation
        conv.last_message = content[:100]  # Truncate for preview
        conv.last_message_at = datetime.utcnow()
        conv.save()
        
        return jsonify({
            "msg": "Message sent",
            "message": {
                "id": str(message.id),
                "content": message.content,
                "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            },
            "conversation_id": str(conv.id)
        }), 201
        
    except DoesNotExist:
        return jsonify({"msg": "User not found"}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


# -----------------------------
# Start Conversation with Seller
# -----------------------------
@chat.route('/chat/start/<seller_id>', methods=['POST'])
@jwt_required()
def start_conversation(seller_id):
    user_id = get_jwt_identity()
    
    if user_id == seller_id:
        return jsonify({"msg": "Cannot start conversation with yourself"}), 400
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        seller = User.objects.get(id=ObjectId(seller_id))
        
        # Check if conversation already exists
        conv = Conversation.objects(
            participants__all=[user, seller],
            participants__size=2
        ).first()
        
        if conv:
            return jsonify({
                "conversation_id": str(conv.id),
                "existing": True
            }), 200
        
        # Create new conversation
        conv = Conversation(
            participants=[user, seller],
            created_at=datetime.utcnow()
        )
        conv.save()
        
        return jsonify({
            "conversation_id": str(conv.id),
            "existing": False
        }), 201
        
    except DoesNotExist:
        return jsonify({"msg": "User not found"}), 404
