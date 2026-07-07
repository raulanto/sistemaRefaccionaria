from django.urls import path
from .views import IndexView, ProveedoresView, CategoriasView, MostrarProductos, MostrarProveedores, crearProducto, ReportesView
from . import views
from .views.proveedorViews import crearProveedor


app_name = 'inventario'

urlpatterns = [
    path('', ReportesView.as_view(), name='index'), 
    
    #PRODUCTO
    path ('crear_producto/', crearProducto.as_view(), name='crear_producto'),
    path('producto/', IndexView.as_view(), name='producto'),
    path('eliminar_producto/<int:pk>/',views.eliminar_producto_ajax,name='eliminar_producto_ajax'),
    path('producto/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='editar_producto'),
    path('producto/<int:id_producto>/', MostrarProductos, name='mostrar_productos'), 
    
    #PROVEEDOR EMPRESA
    path('proveedorEmpresa/proveedorEmpresa_listar/', ProveedoresView.as_view(), name='proveedorEmpresaListar'),  
    path('proveedorEmpresa/proveedorEmpresa_crear/', crearProveedor.as_view(), name='proveedorEmpresaCrear'),
    path('contacto_proveedor/', views.ContactoProveedorView.as_view(), name='contacto_proveedor'),
    path('proveedor/<int:id_proveedor>/', MostrarProveedores, name='mostrar_proveedor'),
    
    #CATEGORIAS
    path('categorias/', CategoriasView.as_view(), name='categorias'),
    
    #VENTA
    path('venta/', views.VentaView, name='venta'),
    path("guardar_venta/", views.guardar_venta, name="guardar_venta"),
    path("ventas_historial/", views.ventas_historial, name="ventas_historial"),
    path('venta/<int:id>/', views.detalle_venta_nota, name='detalle_venta_nota'),
    path("venta/<int:id>/ticket/",views.imprimir_ticket,name="imprimir_ticket",),
    path("cancelar_venta/<int:id>/", views.cancelar_venta, name="cancelar_venta"),
    
    #CONFIGURACION TICKET
    path("configuracion_ticket/", views.configuracion_ticket, name="configuracion_ticket"),
    
    #DASHBOARD
    path('stock-bajo/',views.ReportesView.as_view(),name='reportes'),
    
]
