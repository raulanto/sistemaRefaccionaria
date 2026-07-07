from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from inventario.models.catalogo.categoria_producto import CategoriaProducto


class CategoriasView(View):
    def get(self, request):
        categoriaProducto = CategoriaProducto.objects.all()
        data = {
            "titulo": "Categorias",
            "mensaje": "Bienvenido al sistema de categorías.",
            "categoriaProducto": categoriaProducto,
        }
        return render(request, "categorias.html", context=data)

