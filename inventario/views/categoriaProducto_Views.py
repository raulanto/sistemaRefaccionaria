from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from inventario.forms.categoriaProducto_form import CategoriaProductoForm
from inventario.models.catalogo.categoria_producto import CategoriaProducto
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import F, ProtectedError


class CategoriaListaView(View):
    def get(self, request):
        categoriaProducto = CategoriaProducto.objects.all()
        data = {
            "titulo": "Categorias",
            "mensaje": "Bienvenido al sistema de categorías.",
            "categoriaProducto": categoriaProducto,
        }
        return render(request, "categoriaProducto/categoria_lista.html", context=data)

#Detalle de categoría
def CategoriaDetalleView(request, id_categoria):
    categoria = get_object_or_404(CategoriaProducto, id=id_categoria)
    data = {
        "titulo": "Detalle de la Categoría",
        "categoria": categoria,
    }
    return render(request, "categoriaProducto/categoria_detalle.html", context=data)


class CategoriaCrearView(CreateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = "categoriaProducto/categoria_crear.html"
    success_url = "/categoriaProducto/categoria_lista/"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear Categoría"
        context["mensaje"] = "Completa el formulario para crear una nueva categoría"
        return context

#Edición de categorías
class CategoriaEditarView(UpdateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = "categoriaProducto/categoria_crear.html"
    success_url = "/categoriaProducto/categoria_lista/"
    
#Eliminar categoría
def EliminarCategoriaAjax(request, pk):
    if request.method == "POST":
        #categoría manda a llamar a la funcion y busca la categoría con el id que se le pasa, si no lo encuentra manda un error 404
        categoriaProducto = get_object_or_404(CategoriaProducto, pk=pk)
        try:
            # Intenta eliminar la categoría de la base de datos.
            categoriaProducto.delete()
            return JsonResponse({"estado": "ok"})
        except ProtectedError:
            return JsonResponse(
                {
                    "estado": "error",
                    "mensaje": "No se puede eliminar porque la categoría ya tiene transacciones.",
                }
            )