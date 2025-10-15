from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Bienvenido a El Perrito Feliz 🐾</h1><p>API Django en ejecución.</p>")
