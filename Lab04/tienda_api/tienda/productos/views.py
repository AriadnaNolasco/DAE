import requests
from django.shortcuts import render

def inicio(request):
    # Obtener todos los productos desde la API
    respuesta = requests.get('https://fakestoreapi.com/products')
    productos = respuesta.json()
    return render(request, 'productos/index.html', {'productos': productos})

def buscar_producto(request):
    resultados = []
    if request.method == 'POST':
        nombre_buscado = request.POST.get('nombre_producto', '').lower()
        respuesta = requests.get('https://fakestoreapi.com/products')
        if respuesta.status_code == 200:
            todos = respuesta.json()
            resultados = [p for p in todos if nombre_buscado in p['title'].lower()]
    return render(request, 'productos/buscar.html', {'resultados': resultados})
