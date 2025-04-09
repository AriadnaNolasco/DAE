import requests
from django.shortcuts import render

def inicio(request):
    # Obtener todos los productos desde la API
    respuesta = requests.get('https://fakestoreapi.com/products')
    productos = respuesta.json()
    return render(request, 'productos/index.html', {'productos': productos})

def buscar_producto(request):
    resultado = None
    if request.method == 'POST':
        id_producto = request.POST.get('id_producto')
        respuesta = requests.get(f'https://fakestoreapi.com/products/{id_producto}')
        if respuesta.status_code == 200:
            resultado = respuesta.json()
    return render(request, 'productos/buscar.html', {'resultado': resultado})
