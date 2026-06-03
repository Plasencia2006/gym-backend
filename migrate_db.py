import os
import django
from django.core.management import call_command

# Configurar variables de entorno para Neon
os.environ['DJANGO_SETTINGS_MODULE'] = 'gym_api.settings'
os.environ['USE_NEON'] = 'true'
os.environ['NEON_DATABASE_NAME'] = 'neondb'
os.environ['NEON_DATABASE_USER'] = 'neondb_owner'
os.environ['NEON_DATABASE_PASSWORD'] = 'npg_x8gtGeD0LPrz'
os.environ['NEON_DATABASE_HOST'] = 'ep-small-tooth-aqd9bg29-pooler.c-8.us-east-1.aws.neon.tech'
os.environ['NEON_DATABASE_PORT'] = '5432'

# Inicializar Django
django.setup()

print("=" * 60)
print("🚀 EJECUTANDO MIGRACIONES EN NEON")
print("=" * 60)

try:
    # Ejecutar migraciones
    print("\n📦 Ejecutando migrate...")
    call_command('migrate')
    print("✅ Migraciones completadas")
    
    # Recopilar archivos estáticos
    print("\n🎨 Ejecutando collectstatic...")
    call_command('collectstatic', '--noinput')
    print("✅ Archivos estáticos recopilados")
    
    print("\n" + "=" * 60)
    print("✅ TODO LISTO - Base de datos configurada")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()