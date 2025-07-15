from django.contrib import admin
from inventario.models import ProveedorEmpresa


@admin.register(ProveedorEmpresa)
class ProveedorEmpresaAdmin(admin.ModelAdmin):
    pass