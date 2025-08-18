# Deployment Guide

## Environment Variables Required for Production

Set these environment variables in your deployment platform:

```bash
# Required: Generate a secure secret key (at least 50 characters)
SECRET_KEY=your-very-long-secure-secret-key-here-at-least-50-characters

# Optional: Set to False for production
DEBUG=False

# Optional: Add your domain
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## Deployment Steps

1. **Copy .env.example to .env and update values**
2. **Set environment variables in your deployment platform**
3. **Deploy using the provided Procfile and build.sh**

## Render.com Deployment

1. Create a new Web Service
2. Set environment variables in the dashboard
3. Deploy from your Git repository

## Heroku Deployment

1. Add Heroku remote: `heroku git:remote -a your-app-name`
2. Set config vars: `heroku config:set SECRET_KEY=your-secret-key`
3. Deploy: `git push heroku main`

## Local Development

Copy `.env.example` to `.env` and set `DEBUG=True` for development.
