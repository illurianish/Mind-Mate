from app import create_app
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

try:
    # Create Flask application
    app = create_app()
    logger.info("Application created successfully")
except Exception as e:
    logger.error(f"Failed to create application: {str(e)}")
    raise

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5002))
        logger.info(f"Starting application on port {port}")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise 