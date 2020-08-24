from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from Usuarios.models import Usuario
from Usuarios.forms import CrearUsuarioForm, ModificarUsuarioForm

class UsuarioAdmin(UserAdmin):
    add_form = CrearUsuarioForm
    form = ModificarUsuarioForm
    model = Usuario
    list_display = ["username"]

admin.site.register(Usuario, UsuarioAdmin)
# Register your models here.
