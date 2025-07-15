from django.contrib import admin
from inventario.models.catalogo import Modelo

@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    pass