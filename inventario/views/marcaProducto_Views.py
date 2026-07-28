from django.db.models import ProtectedError
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from inventario.forms.marcaProducto_form import MarcaProductoForm
from inventario.models.catalogo.marca_producto import MarcaProducto


class MarcaProductoView(View):
    def get(self, request):
        marcaProducto = MarcaProducto.objects.all()
        data = {
            "titulo": "Marca Producto",
            "mensaje": "Bienvenido al sistema de marcas de productos.",
            "marcaProductos": marcaProducto,
        }
        return render(request, "marcaProducto/marca_lista.html", context=data)

class MarcaProductoDetalleView(View):
    def get(self, request, id_marca):
        marca = get_object_or_404(MarcaProducto, id=id_marca)
        data = {
            "titulo": "Detalle de la Marca",
            "marca": marca,
        }
        return render(request, "marcaProducto/marca_detalle.html", context=data)

class MarcaProductoCrearView(CreateView):
    model = MarcaProducto
    form_class = MarcaProductoForm
    template_name = "marcaProducto/marca_crear.html"
    success_url = "/marcaProducto/marca_lista/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear Marca"
        context["mensaje"] = "Completa el formulario para crear una nueva marca"
        return context

#Edición de marcas
class MarcaProductoEditarView(UpdateView):
    model = MarcaProducto
    form_class = MarcaProductoForm
    template_name = "marcaProducto/marca_crear.html"
    success_url = "/marcaProducto/marca_lista/"
    
def EliminarMarcaAjax(request, pk):
    if request.method == "POST":
        #marca manda a llamar a la funcion y busca la marca con el id que se le pasa, si no lo encuentra manda un error 404
        marca = get_object_or_404(MarcaProducto, pk=pk)
        try:
            # Intenta eliminar la marca de la base de datos.
            marca.delete()
            return JsonResponse({"estado": "ok"})
        except ProtectedError:
            return JsonResponse(
                {
                    "estado": "error",
                    "mensaje": "No se puede eliminar porque la marca ya tiene transacciones.",
                }
            )

