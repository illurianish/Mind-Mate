from flask import Blueprint, request, jsonify
from models.cbt_exercise import CBTExercise
from extensions import db

cbt_bp = Blueprint('cbt', __name__)

@cbt_bp.route('/', methods=['POST'])
def create_exercise():
    data = request.get_json()
    
    exercise = CBTExercise(
        user_id=1,  # Default user ID
        situation=data['situation'],
        thoughts=data['thoughts'],
        emotions=data['emotions'],
        behaviors=data['behaviors'],
        alternative_thoughts=data.get('alternative_thoughts'),
        rational_response=data.get('rational_response'),
        outcome=data.get('outcome')
    )
    
    db.session.add(exercise)
    db.session.commit()
    
    return jsonify(exercise.to_dict()), 201

@cbt_bp.route('/', methods=['GET'])
def get_exercises():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    exercises = CBTExercise.query.filter_by(
        user_id=1  # Default user ID
    ).order_by(
        CBTExercise.created_at.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'exercises': [exercise.to_dict() for exercise in exercises.items],
        'total': exercises.total,
        'pages': exercises.pages,
        'current_page': exercises.page
    })

@cbt_bp.route('/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = CBTExercise.query.filter_by(
        id=exercise_id,
        user_id=1  # Default user ID
    ).first_or_404()
    
    return jsonify(exercise.to_dict())

@cbt_bp.route('/<int:exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    exercise = CBTExercise.query.filter_by(
        id=exercise_id,
        user_id=1  # Default user ID
    ).first_or_404()
    
    data = request.get_json()
    
    exercise.situation = data.get('situation', exercise.situation)
    exercise.thoughts = data.get('thoughts', exercise.thoughts)
    exercise.emotions = data.get('emotions', exercise.emotions)
    exercise.behaviors = data.get('behaviors', exercise.behaviors)
    exercise.alternative_thoughts = data.get('alternative_thoughts', exercise.alternative_thoughts)
    exercise.rational_response = data.get('rational_response', exercise.rational_response)
    exercise.outcome = data.get('outcome', exercise.outcome)
    
    db.session.commit()
    
    return jsonify(exercise.to_dict())

@cbt_bp.route('/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = CBTExercise.query.filter_by(
        id=exercise_id,
        user_id=1  # Default user ID
    ).first_or_404()
    
    db.session.delete(exercise)
    db.session.commit()
    
    return jsonify({'message': 'Exercise deleted successfully'}) 