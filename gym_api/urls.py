from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


def home(request):
    """Ruta raíz - Health Check"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Gym Management API v1.0',
        'deployed': True,
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'entrenadores': '/api/entrenadores/',
            'rutinas': '/api/rutinas/',
            'login': '/api/entrenadores/login/',
            'register': '/api/entrenadores/register/',
        }
    })


urlpatterns = [
    # ✅ RUTA RAÍZ - Necesaria para Vercel
    path('', home, name='home'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include('entrenadores.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Servir media files en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)