import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Agregar el path del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_api.settings')

application = get_wsgi_application()