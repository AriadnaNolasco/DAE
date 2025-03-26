from django.shortcuts import render
from .models import Item

def item_list(request):
    items = Item.objects.all()  # Trae todos los objetos de la base de datos
    return render(request, 'core/item_list.html', {'items': items})
