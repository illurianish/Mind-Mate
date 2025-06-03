from datetime import datetime
from sqlalchemy.sql import func
from . import db

class Mood(db.Model):
    """
    This is where we store how people are feeling each day
    Think of it like a digital mood diary
    """
    __tablename__ = 'mood'
    
    # Basic database stuff
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # The actual mood data - all on a 1-5 scale to keep things simple
    mood_score = db.Column(db.Integer, nullable=False)    # How good/bad they feel overall
    energy_level = db.Column(db.Integer, nullable=False)  # How energetic vs tired
    anxiety_level = db.Column(db.Integer, nullable=False) # How anxious vs calm
    
    # Optional stuff users can add
    notes = db.Column(db.Text)                          # Whatever they want to write
    activities = db.Column(db.String(200))              # What they did that day (comma-separated)
    
    # When this mood entry was created
    timestamp = db.Column(db.DateTime, default=func.now())
    
    def to_dict(self):
        """
        Converts this mood entry into a dictionary that we can send as JSON
        Also converts the activities string back into a proper list
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'mood_score': self.mood_score,
            'energy_level': self.energy_level,
            'anxiety_level': self.anxiety_level,
            'notes': self.notes,
            'activities': self.activities.split(',') if self.activities else [],  # Convert back to list
            'timestamp': self.timestamp.isoformat()  # Make the timestamp JSON-friendly
        }
