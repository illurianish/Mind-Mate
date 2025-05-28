from flask import Blueprint, request, jsonify
from models.journal import JournalEntry
from extensions import db
from datetime import datetime

journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/', methods=['POST'])
def create_entry():
    data = request.get_json()
    
    entry = JournalEntry(
        user_id=1,  # Default user ID
        title=data.get('title', 'Untitled'),
        content=data['content'],
        mood_tag=data.get('mood_tag'),
        is_private=data.get('is_private', True)
    )
    
    db.session.add(entry)
    db.session.commit()
    
    return jsonify(entry.to_dict()), 201

@journal_bp.route('/', methods=['GET'])
def get_entries():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    entries = JournalEntry.query.filter_by(
        user_id=1  # Default user ID
    ).order_by(
        JournalEntry.created_at.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'entries': [entry.to_dict() for entry in entries.items],
        'total': entries.total,
        'pages': entries.pages,
        'current_page': entries.page
    })

@journal_bp.route('/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    entry = JournalEntry.query.filter_by(
        id=entry_id,
        user_id=1  # Default user ID
    ).first_or_404()
    
    return jsonify(entry.to_dict())

@journal_bp.route('/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    entry = JournalEntry.query.filter_by(
        id=entry_id,
        user_id=1  # Default user ID
    ).first_or_404()
    
    data = request.get_json()
    
    entry.title = data.get('title', entry.title)
    entry.content = data.get('content', entry.content)
    entry.mood_tag = data.get('mood_tag', entry.mood_tag)
    entry.is_private = data.get('is_private', entry.is_private)
    entry.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(entry.to_dict())

@journal_bp.route('/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = JournalEntry.query.filter_by(
        id=entry_id,
        user_id=1  # Default user ID
    ).first_or_404()
    
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({'message': 'Entry deleted successfully'})
