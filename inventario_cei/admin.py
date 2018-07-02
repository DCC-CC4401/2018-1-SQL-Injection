from django.contrib import admin

from .models import Admin, Client
from .models import Object, Space
from .models import Reserve

admin.site.site_header = 'Administrador de la Base de Datos del Sistema de Inventario'

admin.site.register(Admin)
admin.site.register(Client)
admin.site.register(Space)
admin.site.register(Object)
admin.site.register(Reserve)
