from inventario.models.catalogo import MarcaProducto
from django.contrib import admin

@admin.register(MarcaProducto)
class MarcaProductoAdmin(admin.ModelAdmin):
    pass