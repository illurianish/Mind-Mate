from datetime import datetime
from sqlalchemy.sql import func
from . import db

class CBTExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    situation = db.Column(db.Text, nullable=False)
    thoughts = db.Column(db.Text, nullable=False)
    emotions = db.Column(db.Text, nullable=False)
    behaviors = db.Column(db.Text, nullable=False)
    alternative_thoughts = db.Column(db.Text)
    rational_response = db.Column(db.Text)
    outcome = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'situation': self.situation,
            'thoughts': self.thoughts,
            'emotions': self.emotions,
            'behaviors': self.behaviors,
            'alternative_thoughts': self.alternative_thoughts,
            'rational_response': self.rational_response,
            'outcome': self.outcome,
            'created_at': self.created_at.isoformat()
        } 