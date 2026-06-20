from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from .form.producto_form import ProductoForm
from django.http import JsonResponse

from .models import Producto, ProveedorEmpresa, CategoriaProducto, ProductoImagen


class IndexView(View):
    def get(self, request):
        productos = Producto.objects.all()
        data = {
            "titulo": "Sistema de Inventario",
            "mensaje": "Bienvenido al sistema de inventario de refacciones.",
            "productos": productos,
        }
        return render(request, "productos.html", context=data)


class ProveedoresView(View):
    def get(self, request):
        proveedorEmpresas = ProveedorEmpresa.objects.all()
        data = {
            "titulo": "Proveedores",
            "mensaje": "Bienvenido al sistema de proveedores.",
            "proveedorEmpresas": proveedorEmpresas,
        }
        return render(request, "proveedores.html", context=data)


class CategoriasView(View):
    def get(self, request):
        categoriaProducto = CategoriaProducto.objects.all()
        data = {
            "titulo": "Categorias",
            "mensaje": "Bienvenido al sistema de categorías.",
            "categoriaProducto": categoriaProducto,
        }
        return render(request, "categorias.html", context=data)

class ContactoProveedorView(View):
    def get(self, request):
        contactoProveedores = ProveedorEmpresa.objects.all()
        data = {
            "titulo": "Contacto Proveedor",
            "mensaje": "Bienvenido al sistema de contacto de proveedores.",
            "contactoProveedores": contactoProveedores,
        }
        return render(request, "contacto_proveedor.html", context=data)


def MostrarProductos(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    imagenes = ProductoImagen.objects.filter(producto=producto).order_by("orden")
    data = {
        "titulo": "Detalle del Producto",
        "producto": producto,
        "imagenes": imagenes,
    }
    return render(request, "detalle/detalle_producto.html", context=data)


def MostrarProveedores(request, id_proveedor):
    proveedorEmpresa = get_object_or_404(ProveedorEmpresa, id=id_proveedor)
    data = {
        "titulo": "Detalle del Proveedor",
        "proveedorEmpresa": proveedorEmpresa,
    }
    return render(request, "detalle/detalle_proveedor.html", context=data)


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

def eliminar_producto_ajax(request, pk):
    if request.method == 'POST':
        producto = Producto.objects.get(pk=pk)
        producto.delete()
        return JsonResponse({
            'estado': 'ok'
        })
    
