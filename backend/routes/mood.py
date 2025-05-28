from flask import Blueprint, request, jsonify
from models.mood import Mood
from extensions import db
from datetime import datetime, timedelta

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/', methods=['POST'])
def create_mood():
    data = request.get_json()
    
    mood = Mood(
        user_id=1,  # Default user ID
        mood_score=data['mood_score'],
        energy_level=data['energy_level'],
        anxiety_level=data['anxiety_level'],
        notes=data.get('notes'),
        activities=','.join(data.get('activities', []))
    )
    
    db.session.add(mood)
    db.session.commit()
    
    return jsonify(mood.to_dict()), 201

@mood_bp.route('/', methods=['GET'])
def get_moods():
    timeframe = request.args.get('timeframe', 'week')
    
    if timeframe == 'week':
        start_date = datetime.utcnow() - timedelta(days=7)
    elif timeframe == 'month':
        start_date = datetime.utcnow() - timedelta(days=30)
    elif timeframe == 'year':
        start_date = datetime.utcnow() - timedelta(days=365)
    else:
        start_date = datetime.utcnow() - timedelta(days=7)
    
    moods = Mood.query.filter(
        Mood.user_id == 1,  # Default user ID
        Mood.timestamp >= start_date
    ).order_by(Mood.timestamp.desc()).all()
    
    return jsonify([mood.to_dict() for mood in moods])

@mood_bp.route('/stats', methods=['GET'])
def get_mood_stats():
    timeframe = request.args.get('timeframe', 'week')
    
    if timeframe == 'week':
        start_date = datetime.utcnow() - timedelta(days=7)
    elif timeframe == 'month':
        start_date = datetime.utcnow() - timedelta(days=30)
    else:
        start_date = datetime.utcnow() - timedelta(days=7)
    
    moods = Mood.query.filter(
        Mood.user_id == 1,  # Default user ID
        Mood.timestamp >= start_date
    ).all()
    
    if not moods:
        return jsonify({
            'average_mood': 0,
            'average_energy': 0,
            'average_anxiety': 0,
            'total_entries': 0
        })
    
    total_moods = len(moods)
    avg_mood = sum(mood.mood_score for mood in moods) / total_moods
    avg_energy = sum(mood.energy_level for mood in moods) / total_moods
    avg_anxiety = sum(mood.anxiety_level for mood in moods) / total_moods
    
    return jsonify({
        'average_mood': round(avg_mood, 2),
        'average_energy': round(avg_energy, 2),
        'average_anxiety': round(avg_anxiety, 2),
        'total_entries': total_moods
    }) 