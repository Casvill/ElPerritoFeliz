from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    # Qué columnas verás en la tabla del panel admin
    list_display = (
        'documento',
        'nombres',
        'apellidos',
        'tipo_usuario',
        'is_active',
        'is_staff',
        'fecha_registro',
    )
    list_filter = ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser')

    # Campos que no se pueden editar manualmente
    readonly_fields = ('fecha_registro', 'last_login')

    # Cómo se organizan los campos dentro del detalle de un usuario
    fieldsets = (
        (None, {'fields': ('documento', 'password')}),
        ('Información personal', {
            'fields': ('nombres', 'apellidos', 'email', 'fecha_nacimiento', 'foto')
        }),
        ('Contacto', {'fields': ('telefono', 'direccion')}),
        ('Rol y estado', {
            'fields': ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas', {
            'fields': ('fecha_vinculacion', 'fecha_registro', 'last_login')
        }),
    )

    # Campos al crear un nuevo usuario desde el panel admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'documento',
                'nombres',
                'apellidos',
                'tipo_usuario',
                'email',
                'password1',
                'password2',
            ),
        }),
    )

    search_fields = ('documento', 'nombres', 'apellidos', 'email')
    ordering = ('documento',)
