

from django.http import JsonResponse
from django.views import View

from inventario.form.proveedorForm import ProveedorForm
from inventario.models.provedorEmpresa_modelo import ProveedorEmpresa
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, ProtectedError




class crearProveedor(CreateView):
    model = ProveedorEmpresa
    form_class = ProveedorForm
    template_name = "proveedorEmpresa/proveedorEmpresa_crear.html"
    success_url = "/proveedorEmpresa/proveedorEmpresa_listar/"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear Proveedor"
        context["mensaje"] = "Completa el formulario para crear un nuevo proveedor"
        return context

class ProveedoresView(View):
    def get(self, request):
        proveedorEmpresas = ProveedorEmpresa.objects.all()
        data = {
            "titulo": "Proveedores",
            "mensaje": "Bienvenido al sistema de proveedores.",
            "proveedorEmpresas": proveedorEmpresas,
        }
        return render(request, "proveedorEmpresa/proveedorEmpresa_listar.html", context=data)

def MostrarProveedores(request, id_proveedor):
    proveedorEmpresa = get_object_or_404(ProveedorEmpresa, id=id_proveedor)
    data = {
        "titulo": "Detalle del Proveedor",
        "proveedorEmpresa": proveedorEmpresa,
    }
    return render(request, "detalle/detalle_proveedor.html", context=data)


def eliminar_proveedor_ajax(request, pk):
    if request.method == "POST":
        proveedor = get_object_or_404(ProveedorEmpresa, pk=pk)
        try:
            proveedor.delete()
            return JsonResponse({"estado": "ok"})
        except ProtectedError:
            return JsonResponse(
                {
                    "estado": "error",
                    "mensaje": "No se puede eliminar porque el proveedor ya tiene transacciones.",
                }
            )