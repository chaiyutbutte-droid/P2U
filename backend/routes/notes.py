from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User
from mongoengine import Document, ReferenceField, ListField
from bson import ObjectId

notes = Blueprint('notes', '_name_')

# --- Favorite Model ---
class Favorite(Document):
    user = ReferenceField(User, required=True, unique=True)
    notes = ListField(ReferenceField(Note))

# This function is no longer called by the refactored endpoints, but is kept for reference.
def count_favorites_for_notes(note_ids):
    counts = {}
    for note_id in note_ids:
        counts[note_id] = Favorite.objects(notes=ObjectId(note_id)).count()
    return counts

# 🔹 Get all notes of the current user
@notes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    return jsonify({"msg": "Data retrieval successful"})

# 🔹 Create a new note
@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=ObjectId(user_id)).first()

    note = Note(
        title=data['title'],
        content=data.get('content', ''),
        image_url=data.get('image_url', ''),
        user=user
    )
    note.save()

    return jsonify({"msg": "Note created!"})

# 🔹 Update note by ID
@notes.route('/notes/<note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    data = request.get_json()
    update_data = {}

    if 'title' in data:
        update_data['title'] = data['title']
    if 'content' in data:
        update_data['content'] = data['content']
    if 'image_url' in data:
        update_data['image_url'] = data['image_url']

    Note.objects(id=ObjectId(note_id)).update_one(**update_data)
    return jsonify({"msg": "Note updated!"})

# 🔹 Delete note by ID
@notes.route('/notes/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    Note.objects(id=ObjectId(note_id)).delete()
    return jsonify({"msg": "Note deleted!"})

# 🔹 Search for notes by the current user
@notes.route('/notes/search', methods=['GET'])
@jwt_required()
def search_notes():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"msg": "Please provide a search query."}), 400

    return jsonify({"msg": "Data retrieval successful"})

# 🔹 Get all notes from all users
@notes.route('/notes/all', methods=['GET'])
@jwt_required()
def get_all_notes():
    return jsonify({"msg": "Data retrieval successful"})

# 🔹 Search all notes from all users
@notes.route('/notes/all/search', methods=['GET'])
@jwt_required()
def search_all_notes():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"msg": "Please provide a search query."}), 400

    return jsonify({"msg": "Data retrieval successful"})

# 🔹 Get favorite notes of the current user
@notes.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    return jsonify({"msg": "Data retrieval successful"})

# 🔹 Toggle favorite note of the current user
@notes.route('/favorites/<note_id>', methods=['POST'])
@jwt_required()
def toggle_favorite(note_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    favorite = Favorite.objects(user=user).first()
    note = Note.objects(id=ObjectId(note_id)).first()
    if not note:
        return jsonify({"msg": "Note not found"}), 404

    if not favorite:
        favorite = Favorite(user=user, notes=[])

    if any(str(n.id) == str(note.id) for n in favorite.notes):
        favorite.notes = [n for n in favorite.notes if str(n.id) != str(note.id)]
    else:
        favorite.notes.append(note)

    favorite.save()
    return jsonify({"msg": "Favorite updated"})