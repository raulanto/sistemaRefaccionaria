from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
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
