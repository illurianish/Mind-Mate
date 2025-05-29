# Deploying MindMate Backend to Heroku

## Prerequisites
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login to Heroku CLI: `heroku login`

## Deployment Steps

1. Create a new Heroku app:
```bash
heroku create mindmate-backend
```

2. Set environment variables:
```bash
heroku config:set OPENAI_API_KEY=your-api-key
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

3. Deploy the code:
```bash
git push heroku main
```

4. Ensure at least one instance is running:
```bash
heroku ps:scale web=1
```

5. Open the app:
```bash
heroku open
```

## Update Frontend Configuration

Update the frontend's REACT_APP_API_URL in your GitHub Actions workflow to point to your new Heroku URL:

```yaml
REACT_APP_API_URL: https://your-app-name.herokuapp.com
```

## Maintenance

To view logs:
```bash
heroku logs --tail
```

To update deployment:
```bash
git push heroku main
``` 