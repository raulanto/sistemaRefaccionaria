from django.views import View
from django.shortcuts import render
from .models import Producto



class IndexView(View):
    def get(self, request):
        productos = Producto.objects.all()
        data= {
            'titulo': 'Sistema de Inventario',
            'mensaje': 'Bienvenido al sistema de inventario de refacciones.',
            'productos': productos
        }
        return render(request, 'vista1.html', context=data)

