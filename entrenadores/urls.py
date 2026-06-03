from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntrenadorViewSet, RutinaViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register(r'entrenadores', EntrenadorViewSet, basename='entrenador')
router.register(r'rutinas', RutinaViewSet, basename='rutina')

urlpatterns = [
    # Endpoints de autenticación
    path('entrenadores/register/', RegisterView.as_view(), name='register'),
    path('entrenadores/login/', LoginView.as_view(), name='login'),
    
    # Router URLs
    path('', include(router.urls)),
]