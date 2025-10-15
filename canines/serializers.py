#----------------------------------------------
# Import necessary modules
#----------------------------------------------
from rest_framework import serializers
from .models import Canino
from users.models import Usuario


#----------------------------------------------
# Serializer for the Canino model
#----------------------------------------------
class CaninoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Canino model.
    Converts Canino model instances to JSON and validates input data.
    """

    # Optional: show the owner's full name (read-only)
    dueno_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Canino
        fields = [
            'id_canino',
            'nombre',
            'raza',
            'edad',
            'peso',
            'fecha_registro',
            'id_dueno',
            'dueno_nombre',
        ]

    #----------------------------------------------
    # Custom method to display owner's full name
    #----------------------------------------------
    def get_dueno_nombre(self, obj):
        if obj.id_dueno:
            return f"{obj.id_dueno.nombres} {obj.id_dueno.apellidos}"
        return None

    #----------------------------------------------
    # Validate the dog's owner exists
    #----------------------------------------------
    def validate_id_dueno(self, value):
        if not Usuario.objects.filter(id_usuario=value.id_usuario).exists():
            raise serializers.ValidationError("El dueño especificado no existe.")
        return value
