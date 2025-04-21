#!/bin/bash

# Wait for database to be ready
while ! nc -z db 5432; do
  sleep 0.1
done

# Apply database migrations
python manage.py migrate

# Start server
exec "$@"