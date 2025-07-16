from django.contrib import admin
from inventario.models import ProveedorEmpresa


@admin.register(ProveedorEmpresa)
class ProveedorEmpresaAdmin(admin.ModelAdmin):
    list_display = ["nombre","telefono","email","sitio_web"]
    list_editable = ["sitio_web"]
    list_filter = ["nombre"]

