from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Disenador
import hashlib

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Encriptar la contraseña ingresada para compararla con la guardada
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            usuario = Disenador.objects.get(email=email, pass_hash=password_hash)
            # Si existe, redirigir al dashboard
            return redirect("https://www.google.com")
        except Disenador.DoesNotExist:
            messages.error(request, "https://www.google.com/search?client=opera-gx&q=nop&sourceid=opera&ie=UTF-8&oe=UTF-8")
            return redirect("login")

    return render(request, "login.html")