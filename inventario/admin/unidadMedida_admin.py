from django.contrib import admin
from inventario.models.catalogo import UnidadMedida

@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    pass