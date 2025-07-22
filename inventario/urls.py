from django.urls import path
from .views import IndexView,ProvedoresView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('provedores/', ProvedoresView.as_view(), name='provedores'),

]