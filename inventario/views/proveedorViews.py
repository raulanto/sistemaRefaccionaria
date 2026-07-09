

from django.http import JsonResponse
from django.views import View

from inventario.form.proveedorForm import ProveedorForm
from inventario.models.provedorEmpresa_modelo import ProveedorEmpresa
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, ProtectedError


#Lista de proveedores
class ProveedorListaView(View):
    def get(self, request):
        proveedorEmpresas = ProveedorEmpresa.objects.all()
        data = {
            "titulo": "Proveedores",
            "mensaje": "Bienvenido al sistema de proveedores.",
            "proveedorEmpresas": proveedorEmpresas,
        }
        return render(request, "proveedorEmpresa/proveedorEmpresa_lista.html", context=data)

#Detalle de proveedor
def ProveedorDetalleView(request, id_proveedor):
    proveedorEmpresa = get_object_or_404(ProveedorEmpresa, id=id_proveedor)
    data = {
        "titulo": "Detalle del Proveedor",
        "proveedorEmpresa": proveedorEmpresa,
    }
    return render(request, "proveedorEmpresa/proveedorEmpresa_detalle.html", context=data)


#Creación de proveedores
class ProveedorCrearView(CreateView):
    model = ProveedorEmpresa
    form_class = ProveedorForm
    template_name = "proveedorEmpresa/proveedorEmpresa_crear.html"
    success_url = "/proveedorEmpresa/proveedorEmpresa_lista/"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear Proveedor"
        context["mensaje"] = "Completa el formulario para crear un nuevo proveedor"
        return context

#Edición de proveedores
class ProveedorEditarView(UpdateView):
    model = ProveedorEmpresa
    form_class = ProveedorForm
    template_name = "proveedorEmpresa/proveedorEmpresa_crear.html"
    success_url = "/proveedorEmpresa/proveedorEmpresa_lista/"

#Eliminar proveedor
def EliminarProveedorAjax(request, pk):
    if request.method == "POST":
        #proveedor manda a llamar a la funcion y busca el proveedor con el id que se le pasa, si no lo encuentra manda un error 404
        proveedor = get_object_or_404(ProveedorEmpresa, pk=pk)
        try:
            # Intenta eliminar el proveedor de la base de datos.
            proveedor.delete()
            return JsonResponse({"estado": "ok"})
        except ProtectedError:
            return JsonResponse(
                {
                    "estado": "error",
                    "mensaje": "No se puede eliminar porque el proveedor ya tiene transacciones.",
                }
            )