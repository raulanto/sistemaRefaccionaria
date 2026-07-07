from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from inventario.form.producto_form import ProductoForm
from inventario.models.productoImagen_modelo import ProductoImagen
from inventario.models.producto_modelo import Producto
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import F, ProtectedError


class IndexView(View):
    def get(self, request):
        productos = Producto.objects.all()
        data = {
            "titulo": "Sistema de Inventario",
            "mensaje": "Bienvenido al sistema de inventario de refacciones.",
            "productos": productos,
        }
        return render(request, "productos.html", context=data)


def MostrarProductos(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    imagenes = ProductoImagen.objects.filter(producto=producto).order_by("orden")
    data = {
        "titulo": "Detalle del Producto",
        "producto": producto,
        "imagenes": imagenes,
    }
    return render(request, "detalle/detalle_producto.html", context=data)


class crearProducto(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "crud/crear_producto.html"
    success_url = "/producto/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear Producto"
        context["mensaje"] = "Completa el formulario para crear un nuevo producto"
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "crud/crear_producto.html"
    success_url = "/producto/"


def eliminar_producto_ajax(request, pk):
    if request.method == "POST":
        producto = get_object_or_404(Producto, pk=pk)
        try:
            producto.delete()
            return JsonResponse({"estado": "ok"})
        except ProtectedError:
            return JsonResponse(
                {
                    "estado": "error",
                    "mensaje": "No se puede eliminar porque el producto ya fue vendido.",
                }
            )
