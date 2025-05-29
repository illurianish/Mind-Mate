# Deploying MindMate Backend to PythonAnywhere

## Steps to Deploy

1. Create a PythonAnywhere account at https://www.pythonanywhere.com/

2. Go to the Web tab and create a new web app:
   - Choose "Manual Configuration"
   - Select Python 3.11

3. In the PythonAnywhere bash console:
   ```bash
   # Clone the repository
   git clone https://github.com/illurianish/Mind-Mate.git
   cd Mind-Mate
   
   # Create and activate virtual environment
   mkvirtualenv --python=/usr/bin/python3.11 mindmate-env
   pip install -r backend/requirements.txt
   ```

4. Configure the Web app:
   - Go to the Web tab
   - Under "Code" section:
     - Set Source code: ~/Mind-Mate/backend
     - Set Working directory: ~/Mind-Mate/backend
   - Under "WSGI configuration file":
     - Click on the WSGI file link
     - Replace contents with the contents of mindmate_wsgi.py

5. Set up environment variables:
   - Go to the Web tab
   - Under "Environment variables" add:
     ```
     OPENAI_API_KEY=your-api-key
     SECRET_KEY=your-secret-key
     FLASK_ENV=production
     ```

6. Reload the web app

Your backend will be available at: `your-username.pythonanywhere.com`

## Updating the Frontend

Update the frontend's REACT_APP_API_URL in your GitHub Actions workflow to point to your new PythonAnywhere URL:

```yaml
REACT_APP_API_URL: https://your-username.pythonanywhere.com
```

## Maintenance

To update the deployment:
1. Pull latest changes in PythonAnywhere console:
   ```bash
   cd ~/Mind-Mate
   git pull origin main
   ```
2. Reload the web app from the Web tab 