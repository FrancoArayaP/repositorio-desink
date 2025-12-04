from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)  
            messages.success(request, "Has iniciado sesión correctamente")
            return redirect("https://www.google.com/search?client=opera-gx&q=si+funciono&sourceid=opera&ie=UTF-8&oe=UTF-8")
        else:
            messages.error(request, "Credenciales inválidas")
            return redirect("login")

    return render(request, "login.html")



def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("userType")

        if User.objects.filter(username=email).exists():
            messages.error(request, "El correo ya está registrado")
            return redirect("register")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.profile.user_type = user_type
        user.profile.save()

        messages.success(request, "Cuenta creada correctamente. Ahora inicia sesión.")
        return redirect("login")
    return render(request, "register.html")
