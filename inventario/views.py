from django.views import View
from django.shortcuts import render
from .models import Producto, ProveedorEmpresa, CategoriaProducto



class IndexView(View):
    def get(self, request):
        productos = Producto.objects.all()
        data= {
            'titulo': 'Sistema de Inventario',
            'mensaje': 'Bienvenido al sistema de inventario de refacciones.',
            'productos': productos
        }
        return render(request, 'vista1.html', context=data)

class ProveedoresView(View):
     def get(self, request):
        proveedorEmpresas = ProveedorEmpresa.objects.all()
        data= {
            'titulo': 'Proveedores',
            'mensaje': 'Bienvenido al sistema de Proveedores.',
             'proveedorEmpresas': proveedorEmpresas 
        }
        return render(request, 'proveedores.html', context=data)
     
class CategoriasView(View):
    def get(self, request):
        categoriaProducto = CategoriaProducto.objects.all()
        data= {
            'titulo': 'Categorias',
            'mensaje': 'Bienvenido al sistema de Proveedores.',
             'categoriaProducto': categoriaProducto
        }
        return render(request, 'categorias.html', context=data)