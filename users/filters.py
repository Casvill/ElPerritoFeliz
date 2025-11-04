# ----------------------------------------------
# users/filters.py
# ----------------------------------------------
import django_filters
from django.db.models import Q
from .models import Usuario

class UsuarioFilter(django_filters.FilterSet):
    # Campo de búsqueda general
    search = django_filters.CharFilter(method='filter_search', label='Buscar')

    # Campos específicos
    tipo_usuario = django_filters.CharFilter(field_name='tipo_usuario', lookup_expr='iexact')
    fecha_nacimiento = django_filters.DateFromToRangeFilter()
    fecha_vinculacion = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Usuario
        fields = ['tipo_usuario', 'fecha_nacimiento', 'fecha_vinculacion']

    def filter_search(self, queryset, name, value):
        """Permite buscar en nombres, apellidos, email o documento"""
        return queryset.filter(
            Q(nombres__icontains=value)
            | Q(apellidos__icontains=value)
            | Q(email__icontains=value)
            | Q(documento__icontains=value)
        )
