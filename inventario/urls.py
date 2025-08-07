from django.urls import path
from .views import IndexView,ProvedoresView,MostrarProductos,CrearProducto

app_name = 'inventario'

urlpatterns = [
    path('producto/', IndexView.as_view(), name='index'),
    path('provedores/', ProvedoresView.as_view(), name='provedores'),
    path('crear-producto/', CrearProducto.as_view(), name='crear_producto'),
    #Vistas basadas en funcion
    path('producto/<int:id_producto>/', MostrarProductos, name='mostrar_producto'),

]