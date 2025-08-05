from django.urls import path,include  
from .views import IndexView, ProveedoresView, CategoriasView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('proveedores/', ProveedoresView.as_view(), name='proveedores'),
    path('categorias/', CategoriasView.as_view(), name='categorias'),
    
]