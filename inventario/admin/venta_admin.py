from django.contrib import admin
from inventario.models.venta_modelo import Venta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    pass