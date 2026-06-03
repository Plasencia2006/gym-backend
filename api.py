import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Configurar Django ANTES de importar get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_api.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()