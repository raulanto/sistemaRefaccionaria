from django.contrib import admin
from inventario.models import ContactoProveedor


@admin.register(ContactoProveedor)
class ContactoProveedorAdmin(admin.ModelAdmin):
    pass