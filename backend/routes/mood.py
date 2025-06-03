from flask import Blueprint, request, jsonify
from models.mood import Mood
from extensions import db
from datetime import datetime, timedelta

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/', methods=['POST'])
def create_mood():
    """
    This is where people log how they're feeling
    We track mood, energy, anxiety, and any notes they want to add
    """
    try:
        data = request.get_json()
        
        # Basic validation - make sure we have the important stuff
        if not data:
            return jsonify({'error': 'No data provided - we need to know how you\'re feeling!'}), 400
        
        required_fields = ['mood_score', 'energy_level', 'anxiety_level']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field} - we need this to track your mood'}), 400
        
        # Create a new mood entry
        mood = Mood(
            user_id=1,  # TODO: Replace with actual user authentication
            mood_score=data['mood_score'],
            energy_level=data['energy_level'],
            anxiety_level=data['anxiety_level'],
            notes=data.get('notes', ''),  # Notes are optional
            activities=','.join(data.get('activities', []))  # Convert list to string
        )
        
        db.session.add(mood)
        db.session.commit()
        
        return jsonify(mood.to_dict()), 201
        
    except Exception as e:
        print(f"Error saving mood: {str(e)}")
        return jsonify({'error': 'Something went wrong saving your mood entry'}), 500

@mood_bp.route('/', methods=['GET'])
def get_moods():
    """
    Gets mood entries for a specific time period
    Default is the last week, but you can ask for month or year too
    """
    try:
        timeframe = request.args.get('timeframe', 'week')
        
        # Figure out how far back to look
        if timeframe == 'week':
            start_date = datetime.utcnow() - timedelta(days=7)
        elif timeframe == 'month':
            start_date = datetime.utcnow() - timedelta(days=30)
        elif timeframe == 'year':
            start_date = datetime.utcnow() - timedelta(days=365)
        else:
            # If they give us something weird, just default to a week
            start_date = datetime.utcnow() - timedelta(days=7)
        
        # Get all the mood entries in that timeframe
        moods = Mood.query.filter(
            Mood.user_id == 1,  # TODO: Use real user ID when auth is implemented
            Mood.timestamp >= start_date
        ).order_by(Mood.timestamp.desc()).all()
        
        return jsonify([mood.to_dict() for mood in moods])
        
    except Exception as e:
        print(f"Error getting moods: {str(e)}")
        return jsonify({'error': 'Unable to load mood data right now'}), 500

@mood_bp.route('/stats', methods=['GET'])
def get_mood_stats():
    """
    Calculates some basic statistics about mood trends
    Useful for showing progress over time
    """
    try:
        timeframe = request.args.get('timeframe', 'week')
        
        # Same time calculation as above
        if timeframe == 'week':
            start_date = datetime.utcnow() - timedelta(days=7)
        elif timeframe == 'month':
            start_date = datetime.utcnow() - timedelta(days=30)
        else:
            start_date = datetime.utcnow() - timedelta(days=7)
        
        moods = Mood.query.filter(
            Mood.user_id == 1,  # TODO: Real user authentication
            Mood.timestamp >= start_date
        ).all()
        
        # If there are no mood entries, return zeros
        if not moods:
            return jsonify({
                'average_mood': 0,
                'average_energy': 0,
                'average_anxiety': 0,
                'total_entries': 0,
                'message': 'No mood data for this time period yet'
            })
        
        # Calculate averages - basic math but useful for tracking trends
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
        
    except Exception as e:
        print(f"Error calculating mood stats: {str(e)}")
        return jsonify({'error': 'Unable to calculate mood statistics right now'}), 500 