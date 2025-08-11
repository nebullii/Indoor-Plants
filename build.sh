#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Wait for database to be ready and apply migrations
echo "Waiting for database to be ready..."
python manage.py migrate --check || true
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if needed (optional)
# python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'password')"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"