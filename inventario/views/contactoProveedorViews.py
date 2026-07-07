from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from inventario.models.provedorEmpresa_modelo import ProveedorEmpresa


class ContactoProveedorView(View):
    def get(self, request):
        contactoProveedores = ProveedorEmpresa.objects.all()
        data = {
            "titulo": "Contacto Proveedor",
            "mensaje": "Bienvenido al sistema de contacto de proveedores.",
            "contactoProveedores": contactoProveedores,
        }
        return render(request, "contacto_proveedor.html", context=data)
