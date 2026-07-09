from django.contrib import admin
from inventario.models.configuracionTicket_modelo import ConfiguracionTicket

@admin.register(ConfiguracionTicket)
class ConfiguracionTicketAdmin(admin.ModelAdmin):
    pass