#!/bin/bash

echo "🚀 Iniciando build..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt --break-system-packages

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --noinput || true

# Recopilar estáticos (ignorar errores de locale)
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear || true

# Crear superusuario si no existe
echo "👤 Creando superusuario..."
python manage.py shell << EOF || true
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123456',
        first_name='Admin',
        last_name='User',
        especialidad='Administrador',
        telefono='000000000'
    )
    print("✅ Superusuario creado: admin / admin123456")
else:
    print("⚠️ El superusuario ya existe")
EOF

echo "✅ Build completado"