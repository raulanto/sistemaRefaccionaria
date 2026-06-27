from django.urls import path
from .views import IndexView, ProveedoresView, CategoriasView, MostrarProductos, MostrarProveedores, crearProducto, ReportesView
from . import views


app_name = 'inventario'

urlpatterns = [
    path('', IndexView.as_view(), name='index'), 
    path('producto/', IndexView.as_view(), name='producto'),
    path('venta/', views.VentaView, name='venta'),


    path('proveedores/', ProveedoresView.as_view(), name='proveedores'),  
    path('categorias/', CategoriasView.as_view(), name='categorias'),
    path('contacto_proveedor/', views.ContactoProveedorView.as_view(), name='contacto_proveedor'),
    path ('crear_producto/', crearProducto.as_view(), name='crear_producto'),
    path('eliminar_producto/<int:pk>/',views.eliminar_producto_ajax,name='eliminar_producto_ajax'),
    path('stock-bajo/',views.ReportesView.as_view(),name='reportes'),
    path('producto/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='editar_producto'),

    
    #Vistas basadas en funciones
    #path('eliminar_producto/<int:pk>/',EliminarProducto.as_view(),name='eliminar_producto'),
    path('producto/<int:id_producto>/', MostrarProductos, name='mostrar_productos'), 
    path('proveedor/<int:id_proveedor>/', MostrarProveedores, name='mostrar_proveedor'),
    
]
