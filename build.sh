#!/bin/bash

echo "🚀 Iniciando build..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt --break-system-packages --quiet

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --noinput || echo "⚠️ Warning: Migrations failed"

# Recopilar estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear || echo "⚠️ Warning: Collectstatic failed"

echo "✅ Build completado"