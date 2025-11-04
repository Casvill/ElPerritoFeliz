# ----------------------------------------------
# users/filters.py
# ----------------------------------------------
import django_filters
from .models import Usuario

class UsuarioFilter(django_filters.FilterSet):
    # 🔹 Filtro que busca texto parcial en varios campos
    search = django_filters.CharFilter(method='filter_search', label='Buscar')

    tipo_usuario = django_filters.CharFilter(field_name='tipo_usuario', lookup_expr='iexact')
    fecha_nacimiento = django_filters.DateFromToRangeFilter()
    fecha_vinculacion = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Usuario
        fields = ['tipo_usuario', 'fecha_nacimiento', 'fecha_vinculacion']

    def filter_search(self, queryset, name, value):
        """
        Permite buscar en múltiples campos (nombres, apellidos, email, documento)
        """
        return queryset.filter(
            django_filters.Q(nombres__icontains=value)
            | django_filters.Q(apellidos__icontains=value)
            | django_filters.Q(email__icontains=value)
            | django_filters.Q(documento__icontains=value)
        )
