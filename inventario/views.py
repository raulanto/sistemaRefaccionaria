from django.views import View
from django.shortcuts import render
from .models import Producto,ProveedorEmpresa



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