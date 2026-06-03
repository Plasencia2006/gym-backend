from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Entrenador, Rutina


class EntrenadorSerializer(serializers.ModelSerializer):
    rutinas_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Entrenador
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'especialidad', 'telefono', 'foto', 'fecha_registro',
            'is_trainer', 'rutinas_count'
        ]
        read_only_fields = ['fecha_registro', 'is_trainer']
    
    def get_rutinas_count(self, obj):
        return obj.rutinas.count()


class EntrenadorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Entrenador
        fields = [
            'username', 'password', 'password2', 'first_name', 
            'last_name', 'email', 'especialidad', 'telefono'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden"
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        # Crear el usuario con create_user para que encripte la contraseña
        entrenador = Entrenador.objects.create_user(
            password=password,
            is_trainer=True,
            **validated_data
        )
        return entrenador


class RutinaSerializer(serializers.ModelSerializer):
    entrenador_nombre = serializers.CharField(source='entrenador.get_full_name', read_only=True)
    
    class Meta:
        model = Rutina
        fields = ['id', 'nombre', 'descripcion', 'duracion', 'nivel', 
                  'imagen', 'entrenador', 'entrenador_nombre', 'created_at', 'updated_at']
        read_only_fields = ['entrenador']
        
        # ✅ HACER IMAGEN OPCIONAL
        extra_kwargs = {
            'imagen': {
                'required': False,    # ← NO requerida
                'allow_null': True,   # ← Permitir NULL
                'allow_blank': True   # ← Permitir vacío
            }
        }
    
    def validate_imagen(self, value):
        """Validar imagen - permitir None"""
        if value is None or value == '':
            return None
        if value:
            max_size = 5 * 1024 * 1024  # 5MB
            if value.size > max_size:
                raise serializers.ValidationError("La imagen no puede superar 5MB")
        return value