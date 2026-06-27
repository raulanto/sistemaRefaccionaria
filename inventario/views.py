from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from inventario.models.catalogo.marca_producto import MarcaProducto
from .form.producto_form import ProductoForm
from django.http import JsonResponse
from django.db.models import F
from django.views.generic import ListView

from .models import Producto, ProveedorEmpresa, CategoriaProducto, ProductoImagen, ContactoProveedor


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
        
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'crud/crear_producto.html'
    success_url = "/producto/"
    
class ReportesView(View):
    def get(self, request):
        total_productos = Producto.objects.count()

        total_stock_bajo = Producto.objects.filter(
            stock__lte=F('stock_minimo')
        ).count()

        total_agotados = Producto.objects.filter(stock=0).count()
        total_marcas = MarcaProducto.objects.count()
        total_proveedores = ProveedorEmpresa.objects.count()
        total_categorias = CategoriaProducto.objects.count()
        total_contactos = ContactoProveedor.objects.count()
        productos_con_iva = Producto.objects.filter(tiene_iva=True).count()
        productos = Producto.objects.all()[:5]
        

        context = {
            "titulo": "Dashboard",
            "total_productos": total_productos,
            "total_stock_bajo": total_stock_bajo,
            "total_agotados": total_agotados,
            "total_marcas": total_marcas,
            "total_proveedores": total_proveedores,
            "total_categorias": total_categorias,
            "total_contactos": total_contactos,
            "productos_con_iva": productos_con_iva,
            "productos": productos,   
        }

        return render(request, "reportes/reportes.html", context)

def VentaView(request):
    productos = Producto.objects.all()
    data = {
        "titulo": "Venta de Productos",
        "mensaje": "Bienvenido al sistema de venta de productos.",
        "productos": productos,
    }
    return render(request, "venta.html", context=data)