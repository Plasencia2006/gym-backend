import os
import sys
from pathlib import Path

# Agregar el path del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_api.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()