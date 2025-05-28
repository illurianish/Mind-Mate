from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db initialization to avoid circular imports
def init_models():
    from .user import User
    from .mood import Mood
    from .journal import JournalEntry
    from .cbt_exercise import CBTExercise
    from .chat import ChatHistory
    
    # Make models available at module level
    globals().update(locals())
    
    return {
        'User': User,
        'Mood': Mood,
        'JournalEntry': JournalEntry,
        'CBTExercise': CBTExercise,
        'ChatHistory': ChatHistory
    }

__all__ = ['db', 'User', 'Mood', 'JournalEntry', 'CBTExercise', 'ChatHistory', 'init_models']

# Models package 