from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from inventario.forms.contactoProveedor_form import ContactoProveedorForm
from inventario.models.contactoProveedor_modelo import ContactoProveedor
from inventario.models.provedorEmpresa_modelo import ProveedorEmpresa
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import F, ProtectedError


class ContactoProveedorListaView(View):
    def get(self, request):
        contactoProveedores = ContactoProveedor.objects.all()
        data = {
            "titulo": "Contacto Proveedor",
            "mensaje": "Bienvenido al sistema de contacto de proveedores.",
            "contactoProveedores": contactoProveedores,
        }
        return render(request, "contactoProveedor/contactoProveedor_lista.html", context=data)

#Detalle de contacto proveedor
def ContactoProveedorDetalleView(request, id_contacto_proveedor):
    contactoProveedor = get_object_or_404(ProveedorEmpresa, id=id_contacto_proveedor)
    data = {
        "titulo": "Detalle del Contacto del Proveedor",
        "contactoProveedor": contactoProveedor,
    }
    return render(request, "contactoProveedor/contactoProveedor_detalle.html", context=data)

#Creación de proveedores
class ContactoProveedorCrearView(CreateView):
    model = ContactoProveedor
    form_class = ContactoProveedorForm
    template_name = "contactoProveedor/contactoProveedor_crear.html"
    success_url = "/contactoProveedor/contactoProveedor_lista/"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear Contacto del Proveedor"
        context["mensaje"] = "Completa el formulario para crear un nuevo contacto de proveedor"
        return context
    
class ContactoProveedorEditarView(UpdateView):
    model = ContactoProveedor
    form_class = ContactoProveedorForm
    template_name = "contactoProveedor/contactoProveedor_crear.html"
    success_url = "/contactoProveedor/contactoProveedor_lista/"

#Eliminar proveedor
def EliminarContactoProveedorAjax(request, pk):
    if request.method == "POST":
        contacto_proveedor = get_object_or_404(ContactoProveedor, pk=pk)
        try:
            contacto_proveedor.delete()
            return JsonResponse({"estado": "ok"})
        except ProtectedError:
            return JsonResponse(
                {
                    "estado": "error",
                    "mensaje": "No se puede eliminar porque el contacto de proveedor ya tiene transacciones.",
                }
            )