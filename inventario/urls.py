from django.urls import path
from .views import IndexView, ProveedoresView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('proveedores/', ProveedoresView.as_view(), name='proveedores'),
]