from django.urls import path
from .views import inicio, buscar_producto

urlpatterns = [
    path('', inicio, name='inicio'),
    path('buscar/', buscar_producto, name='buscar_producto'),
]
