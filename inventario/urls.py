from django.urls import path
from .views import productoViews, ProveedorListaView, CategoriaListaView, MostrarProductos, ProveedorDetalleView, crearProducto, DashboardView
from . import views
from .views.proveedorViews import ProveedorCrearView, ProveedorEditarView


app_name = 'inventario'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'), 
    
    #PRODUCTO
    path('producto/', productoViews.ProductoView.as_view(), name='producto'),
    path ('crear_producto/', crearProducto.as_view(), name='crear_producto'),
    path('eliminar_producto/<int:pk>/',views.eliminar_producto_ajax,name='eliminar_producto_ajax'),
    path('producto/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='editar_producto'),
    path('producto/<int:id_producto>/', MostrarProductos, name='mostrar_productos'),
    path('productos/exportar/', productoViews.ExportarProdutosExcel, name='exportarProductosExcel'),

    
    #PROVEEDOR EMPRESA
    path('proveedorEmpresa/proveedorEmpresa_lista/', ProveedorListaView.as_view(), name='proveedorEmpresaLista'),
    path('proveedorEmpresa/proveedorEmpresa_detalle/<int:id_proveedor>/', ProveedorDetalleView, name='proveedorEmpresaDetalle'),
    path('proveedorEmpresa/proveedorEmpresa_crear/', ProveedorCrearView.as_view(), name='proveedorEmpresaCrear'),
    path('proveedorEmpresa/proveedorEmpresa_editar/<int:pk>/', ProveedorEditarView.as_view(), name='proveedorEmpresaEditar'),
    path('eliminarProveedor/<int:pk>/',views.EliminarProveedorAjax,name='eliminarProveedorAjax'),
    
    
    #PROVEEDOR CONTACTO
    path('contactoProveedor/contactoProveedor_lista/', views.ContactoProveedorListaView.as_view(), name='contactoProveedorLista'),
    path('contactoProveedor/contactoProveedor_detalle/<int:id_contacto_proveedor>/', views.ContactoProveedorDetalleView, name='contactoProveedorDetalle'),
    path('contactoProveedor/contactoProveedor_crear/', views.ContactoProveedorCrearView.as_view(), name='contactoProveedorCrear'),
    path('contactoProveedor/contactoProveedor_editar/<int:pk>/', views.ContactoProveedorEditarView.as_view(), name='contactoProveedorEditar'),
    path('contacto_proveedor/<int:pk>/', views.EliminarContactoProveedorAjax, name='eliminarContactoProveedorAjax'),
    
    #CATEGORIAS
    path('categoriaProducto/categoria_lista/', CategoriaListaView.as_view(), name='categoriaLista'),
    path('categoriaProducto/categoria_detalle/<int:id_categoria>/', views.CategoriaDetalleView, name='categoriaDetalle'),
    path('categoriaProducto/categoria_crear/', views.CategoriaCrearView.as_view(), name='categoriaCrear'),
    path('categoriaProducto/categoria_editar/<int:pk>/', views.CategoriaEditarView.as_view(), name='categoriaEditar'),
    path('categoriaProducto/<int:pk>/', views.EliminarCategoriaAjax, name='eliminarCategoriaAjax'),
    
      
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
    path('dashboard/dashboard',views.DashboardView.as_view(),name='dashboard'),
    
]
