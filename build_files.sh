#!/bin/bash
echo "Building Django static files..."
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput --clear