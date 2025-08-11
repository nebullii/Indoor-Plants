#!/usr/bin/env bash
# Exit on error but show what failed
set -o errexit

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check database connection
echo "Testing database connection..."
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indoor_plant.settings')
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('✓ Database connection successful')
except Exception as e:
    print(f'✗ Database connection failed: {e}')
    exit(1)
"

# Show current migration status
echo "Checking migration status..."
python manage.py showmigrations || echo "Could not show migrations"

# Run migrations with verbose output
echo "Running migrations with verbose output..."
python manage.py migrate --verbosity=2

# Verify tables exist
echo "Verifying key tables exist..."
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indoor_plant.settings')
django.setup()
from django.db import connection

tables_to_check = ['django_session', 'products_category', 'products_product']
with connection.cursor() as cursor:
    for table in tables_to_check:
        cursor.execute(\"SELECT count(*) FROM information_schema.tables WHERE table_name = %s\", [table])
        exists = cursor.fetchone()[0] > 0
        print(f'Table {table}: {\"✓\" if exists else \"✗\"} {\"exists\" if exists else \"missing\"}')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"