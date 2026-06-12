from django.contrib import admin
from inventario.models import CategoriaProducto


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "padre",
    )

    search_fields = (
        "nombre",
    )

    list_filter = (
        "padre",
    )

    ordering = (
        "nombre",
    )