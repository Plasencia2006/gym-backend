from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Entrenador, Rutina
from .serializers import (
    EntrenadorSerializer, 
    EntrenadorRegisterSerializer,
    RutinaSerializer
)


class IsTrainer(BasePermission):  # ✅ CORREGIDO: BasePermission viene de permissions
    """Permiso personalizado solo para entrenadores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_trainer


class RegisterView(APIView):
    """Registro de nuevo entrenador"""
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request):
        print("=" * 50)
        print("REGISTER VIEW - Request received")
        print("Content-Type:", request.content_type)
        print("Data:", request.data)
        print("=" * 50)
        
        serializer = EntrenadorRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            entrenador = serializer.save()
            refresh = RefreshToken.for_user(entrenador)
            
            return Response({
                'entrenador': EntrenadorSerializer(entrenador).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Login de entrenador"""
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request):
        print("=" * 50)
        print("LOGIN VIEW - Request received")
        print("Content-Type:", request.content_type)
        print("Data:", request.data)
        print("=" * 50)
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username y password son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user and user.is_trainer:
            refresh = RefreshToken.for_user(user)
            return Response({
                'entrenador': EntrenadorSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        return Response(
            {'error': 'Credenciales inválidas o no es entrenador'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class EntrenadorViewSet(viewsets.ModelViewSet):
    """ViewSet para Entrenadores - CRUD completo"""
    queryset = Entrenador.objects.all()
    serializer_class = EntrenadorSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    @action(detail=False, methods=['get'])
    def mi_perfil(self, request):
        """Obtener perfil del entrenador logueado"""
        serializer = EntrenadorSerializer(request.user)
        return Response(serializer.data)


class RutinaViewSet(viewsets.ModelViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def perform_create(self, serializer):
        """Crear rutina asignando el entrenador actual"""
        try:
            print("CREANDO RUTINA")
            print("User:", self.request.user)
            serializer.save(entrenador=self.request.user)
        except Exception as e:
            print("ERROR al crear:", str(e))
            raise
    
    def perform_update(self, serializer):
        """Actualizar rutina - SOLO actualizar campos enviados"""
        try:
            print("ACTUALIZANDO RUTINA")
            print("User:", self.request.user)
            print("Data:", self.request.data)
            print("Files:", self.request.FILES)
            
            # Guardar sin tocar el entrenador (se mantiene el original)
            serializer.save()
        except Exception as e:
            print("ERROR al actualizar:", str(e))
            raise
    
    def update(self, request, *args, **kwargs):
        """Override del update para manejar mejor los datos"""
        partial = kwargs.pop('partial', True)  # Permitir actualización parcial
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            print("ERROR en update:", str(e))
            return Response(
                {'error': str(e), 'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get_queryset(self):
        queryset = Rutina.objects.all()
        entrenador_id = self.request.query_params.get('entrenador_id', None)
        if entrenador_id is not None:
            queryset = queryset.filter(entrenador_id=entrenador_id)
        return queryset