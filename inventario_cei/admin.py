from django.contrib import admin

from .models import Admin, Client
from .models import Object, Space
from .models import Reserve

admin.site.site_header = 'Administrador de la Base de Datos del Sistema de Inventario'


class AdminAdministrator(admin.ModelAdmin):
    list_display = ('user', 'name', 'rut', 'mail')


admin.site.register(Admin, AdminAdministrator)


class ClientAdministrator(admin.ModelAdmin):
    list_display = ('user', 'name', 'rut', 'mail', 'enable')


admin.site.register(Client, ClientAdministrator)


class ObjectAdministrator(admin.ModelAdmin):
    list_display = ('name', 'description', 'condition', 'image')


admin.site.register(Object, ObjectAdministrator)


class SpaceAdministrator(admin.ModelAdmin):
    list_display = ('name', 'description', 'capacity', 'condition', 'image')


admin.site.register(Space, SpaceAdministrator)


class ReserveAdministrator(admin.ModelAdmin):
    list_display = ('user', 'start', 'finish', 'state')


admin.site.register(Reserve, ReserveAdministrator)
