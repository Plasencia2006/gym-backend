from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
import io
import traceback
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

def home(request):
    """Health check - Ruta raíz"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Gym Management API',
        'version': '1.0.0'
    })

@csrf_exempt
def setup_database(request):
    """
    EJECUTAR MIGRACIONES - ENDPOINT TEMPORAL
    ⚠️ ELIMINAR DESPUÉS DE USAR
    """
    secret = request.GET.get('secret')
    
    if secret != 'setup2026':
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    action = request.GET.get('action', 'migrate')
    output = io.StringIO()
    
    try:
        if action == 'migrate':
            call_command('migrate', stdout=output)
            call_command('collectstatic', '--noinput', stdout=output)
            result = output.getvalue()
            return HttpResponse(f"✅ Migraciones ejecutadas:\n\n{result}")
        
        elif action == 'createsuperuser':
            username = request.GET.get('username', 'admin')
            email = request.GET.get('email', 'admin@example.com')
            password = request.GET.get('password', 'admin123456')
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            if User.objects.filter(username=username).exists():
                return HttpResponse(f"⚠️ Usuario '{username}' ya existe")
            
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User',
                especialidad='Administrador',
                telefono='000000000'
            )
            return HttpResponse(f"✅ Superusuario creado:\nUsuario: {username}\nPassword: {password}")
        
        elif action == 'all':
            call_command('migrate', stdout=output)
            call_command('collectstatic', '--noinput', stdout=output)
            
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
            
            result = output.getvalue()
            return HttpResponse(f"✅ Todo listo:\n\n{result}\n\n✅ Superusuario: admin / admin123456")
        
    except Exception as e:
        error_output = traceback.format_exc()
        return HttpResponse(f"❌ Error:\n{error_output}")
    
@csrf_exempt
def test_cloudinary(request):
    """Probar conexión con Cloudinary"""
    try:
        # Verificar configuración
        config = cloudinary.config()
        
        return JsonResponse({
            'status': 'ok',
            'cloud_name': config.cloud_name,
            'api_key': config.api_key[:5] + '...' if config.api_key else 'NO CONFIGURADO',
            'api_secret': 'CONFIGURADO' if config.api_secret else 'NO CONFIGURADO',
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

urlpatterns = [
    path('', home, name='home'),
    path('setup-db/', setup_database, name='setup_database'),
    path('admin/', admin.site.urls),
    path('api/', include('entrenadores.urls')),
    path('test-cloudinary/', test_cloudinary, name='test_cloudinary'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)