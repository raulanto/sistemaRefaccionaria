from django.contrib import admin
from inventario.models.detalleVenta_modelo import DetalleVenta

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    pass