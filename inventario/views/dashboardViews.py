
from django.views import View

from inventario.models.catalogo.categoria_producto import CategoriaProducto
from inventario.models.catalogo.marca_producto import MarcaProducto
from inventario.models.contactoProveedor_modelo import ContactoProveedor
from inventario.models.producto_modelo import Producto
from inventario.models.provedorEmpresa_modelo import ProveedorEmpresa
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, ProtectedError

class ReportesView(View):
    def get(self, request):
        total_productos = Producto.objects.count()

        total_stock_bajo = Producto.objects.filter(stock__lte=F("stock_minimo")).count()

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

