from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User, Favorite
from mongoengine.errors import DoesNotExist, ValidationError

notes = Blueprint("notes", __name__)

# 📝 สร้าง Note ใหม่
@notes.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    note = Note(
        title=data.get("title"),
        content=data.get("content", ""),
        image_url=data.get("image_url", None),
        user=user
    )
    note.save()
    return jsonify({"msg": "Note created successfully", "note_id": str(note.id)}), 201


# 📜 ดึง Note ทั้งหมดของผู้ใช้
@notes.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    notes_list = Note.objects(user=user_id).order_by("-created_at")
    return Response(notes_list.to_json(), mimetype="application/json"), 200


# 🔍 ดึง Note ตาม ID
@notes.route("/notes/<note_id>", methods=["GET"])
@jwt_required()
def get_note_by_id(note_id):
    try:
        note = Note.objects.get(id=note_id)
    except DoesNotExist:
        return jsonify({"error": "Note not found"}), 404
    return Response(note.to_json(), mimetype="application/json"), 200


# ✏️ แก้ไข Note
@notes.route("/notes/<note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        note = Note.objects.get(id=note_id, user=user_id)
    except DoesNotExist:
        return jsonify({"error": "Note not found"}), 404

    allowed_fields = {"title", "content", "image_url"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    try:
        note.update(**update_data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"msg": "Note updated successfully"}), 200


# 🗑 ลบ Note
@notes.route("/notes/<note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()

    try:
        note = Note.objects.get(id=note_id, user=user_id)
    except DoesNotExist:
        return jsonify({"error": "Note not found"}), 404

    note.delete()
    return jsonify({"msg": "Note deleted successfully"}), 200


# ⭐ เพิ่ม Note เข้า Favorite
@notes.route("/favorites/<note_id>", methods=["POST"])
@jwt_required()
def add_to_favorites(note_id):
    user_id = get_jwt_identity()

    try:
        user = User.objects.get(id=user_id)
        note = Note.objects.get(id=note_id)  # ไม่จำเป็นต้องเป็นเจ้าของ note
    except DoesNotExist:
        return jsonify({"error": "Note not found"}), 404

    favorite, created = Favorite.objects.get_or_create(user=user)
    if note not in favorite.notes:
        favorite.notes.append(note)
        favorite.save()

    return jsonify({"msg": "Note added to favorites"}), 200


# 📜 ดึง Favorite Notes
@notes.route("/favorites", methods=["GET"])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()

    try:
        favorite = Favorite.objects.get(user=user_id)
    except DoesNotExist:
        return jsonify([]), 200

    return Response(favorite.notes.to_json(), mimetype="application/json"), 200