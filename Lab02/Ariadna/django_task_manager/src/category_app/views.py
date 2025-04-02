from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Bienvenido a la aplicación de categorías</h1>")
