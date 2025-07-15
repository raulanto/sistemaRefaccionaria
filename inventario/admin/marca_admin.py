from inventario.models.catalogo import Marca
from django.contrib import admin

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    pass