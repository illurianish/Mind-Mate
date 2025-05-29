import os
import sys

# Add the path to your Flask application
path = os.path.expanduser('~/mindmate-backend')
if path not in sys.path:
    sys.path.append(path)

# Import your Flask application
from app import app as application

# This is the PythonAnywhere WSGI configuration file
application.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-this') 