# Fix for Static and Media File 404 Errors

## Problem Identified
DEBUG=False is preventing Django from serving static and media files automatically.

## Solution Options

### Option 1: Development Fix (Quick)
Set DEBUG=True in your environment:

**Windows:**
```bash
# Create .env file in Donotech directory
echo DEBUG=True > .env
```

**Linux/Mac:**
```bash
# Create .env file in Donotech directory
echo "DEBUG=True" > .env
```

**Then restart your server:**
```bash
python manage.py runserver
```

### Option 2: Production Setup (DEBUG=False)
When DEBUG=False, you need to configure proper static file serving:

#### 1. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

#### 2. Configure Web Server (Example for nginx)
```nginx
# /etc/nginx/sites-available/donotech
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/Donotech/staticfiles/;
    }

    location /media/ {
        alias /path/to/Donotech/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

#### 3. Update settings.py for production
```python
# Add these if using WhiteNoise for static files
# pip install whitenoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Option 3: Using WhiteNoise (Simple Production)
1. Install WhiteNoise:
```bash
pip install whitenoise
```

2. Update settings.py:
```python
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... your existing middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

3. Run collectstatic:
```bash
python manage.py collectstatic --noinput
```

## Verification Steps

After implementing any solution:

1. **Check static files:**
   - Visit: http://localhost:8000/static/css/custom.css
   - Should load without 404

2. **Check media files:**
   - Visit: http://localhost:8000/media/logos/TECH%20SOLUTIONS%20PVT%20LTD.png
   - Should load without 404

3. **Check tieup images:**
   - Visit: http://localhost:8000/media/tieups/PDI.jpg
   - Should load without 404

## Environment Variables Template

Create `.env` file in Donotech directory:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Common Issues and Solutions

1. **Static files not found after collectstatic:**
   - Ensure STATIC_ROOT is set correctly
   - Check file permissions

2. **Media files not uploading:**
   - Ensure MEDIA_ROOT directory exists
   - Check write permissions

3. **WhiteNoise not working:**
   - Ensure it's added to MIDDLEWARE
   - Run collectstatic after installation
