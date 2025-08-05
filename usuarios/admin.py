from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'tipo', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil', {'fields': ('tipo',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Perfil', {'fields': ('tipo',)}),
    )
