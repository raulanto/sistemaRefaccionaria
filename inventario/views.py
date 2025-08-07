from django.views import View
from django.views.generic import CreateView
from django.shortcuts import render
from .models import Producto,ProveedorEmpresa,ProductoImagen
from .form.producto_form import ProductoForm


class IndexView(View):
    def get(self, request):
        productos = Producto.objects.all()
        data= {
            'titulo': 'Inventario de Productos',
            'mensaje': 'Bienvenido al sistema de inventario de refacciones.',
            'productos': productos
        }
        return render(request, 'vista1.html', context=data)

class ProvedoresView(View):
    def get(self, request):
        proveedores = ProveedorEmpresa.objects.all()
        data = {
            'titulo': 'Proveedores',
            'mensaje': 'Bienvenido a la sección de proveedores.',
            'proveedores': proveedores
        }
        return render(request, 'provedores.html', context=data)


def MostrarProductos(request,id_producto):
    producto = Producto.objects.get(id=id_producto)
    imagen= ProductoImagen.objects.filter(producto=producto).order_by('orden')
    data={
        'titulo': 'Detalle del Producto',
        'mensaje': 'Aquí puedes ver los detalles del producto seleccionado.',
        'producto': producto,
        'imagenes': imagen,
    }
    return render(request, 'detalle/producto.html', context=data)



class CrearProducto(CreateView):
    model= Producto
    form_class = ProductoForm
    template_name = 'crud/crear_producto.html'
    success_url = '/producto/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Producto"
        context['mensaje'] = "Completa el formulario para crear un nuevo producto."
        return context
