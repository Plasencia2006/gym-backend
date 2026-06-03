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
    entrenador_nombre = serializers.CharField(
        source='entrenador.get_full_name', 
        read_only=True
    )
    
    class Meta:
        model = Rutina
        fields = [
            'id', 'nombre', 'duracion', 'nivel', 'descripcion',
            'imagen', 'entrenador', 'entrenador_nombre',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'entrenador']
    
    def validate_imagen(self, value):
        """Validar imagen solo si se proporciona una nueva"""
        if value:
            # Validar tamaño (5MB max)
            max_size = 5 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError(
                    "La imagen no puede superar 5MB"
                )
            
            # Validar tipo
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Solo se permiten imágenes JPG, PNG o WebP"
                )
        
        return value
    
    def update(self, instance, validated_data):
        """
        Actualizar instancia manteniendo la imagen anterior si no se proporciona una nueva
        """
        print("=== UPDATE SERIALIZER ===")
        print("Instance:", instance)
        print("Validated data:", validated_data)
        
        # Si no se envía imagen, mantener la existente
        if 'imagen' not in validated_data or validated_data.get('imagen') is None:
            # Remover imagen del validated_data si es None
            validated_data.pop('imagen', None)
            print("Manteniendo imagen existente:", instance.imagen)
        
        # Actualizar campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        print("Rutina actualizada:", instance)
        return instance