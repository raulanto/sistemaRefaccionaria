from django.contrib import admin
from inventario.models import ProductoImagen

@admin.register(ProductoImagen)
class ProductoImagenAdmin(admin.ModelAdmin):
    pass