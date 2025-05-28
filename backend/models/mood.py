from datetime import datetime
from sqlalchemy.sql import func
from . import db

class Mood(db.Model):
    __tablename__ = 'mood'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    mood_score = db.Column(db.Integer, nullable=False)  # 1-5 scale
    energy_level = db.Column(db.Integer, nullable=False)  # 1-5 scale
    anxiety_level = db.Column(db.Integer, nullable=False)  # 1-5 scale
    notes = db.Column(db.Text)
    activities = db.Column(db.String(200))  # Comma-separated activities
    timestamp = db.Column(db.DateTime, default=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'mood_score': self.mood_score,
            'energy_level': self.energy_level,
            'anxiety_level': self.anxiety_level,
            'notes': self.notes,
            'activities': self.activities.split(',') if self.activities else [],
            'timestamp': self.timestamp.isoformat()
        }
