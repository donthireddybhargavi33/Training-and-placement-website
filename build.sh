#!/bin/bash
# Build script for deployment

# Update pip and install build dependencies
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

# Create cache table if using database caching
python manage.py createcachetable --database default

echo "Build completed successfully!"
