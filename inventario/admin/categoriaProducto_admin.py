from django.contrib import admin
from inventario.models.catalogo import CategoriaProducto


@admin.register(CategoriaProducto)
class CategoriaProductoNameAdmin(admin.ModelAdmin):
    pass


