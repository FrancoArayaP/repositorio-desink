from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout

def index(request):
    return render(request, 'index.html')

def login_view(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            u = User.objects.get(username=email)
            auth_login(request, user)  
            messages.success(request, "Has iniciado sesión correctamente")
            if u.profile.user_type == "designer":
                return redirect("disenador")
            if u.profile.user_type == "mipyme":
                return redirect("mipyme")
        else:
            messages.error(request, "Credenciales inválidas")
            return redirect("login")

    return render(request, "login.html")

def register_view(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
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
        storage = messages.get_messages(request)
        for _ in storage:
            pass
        messages.success(request, "Cuenta creada correctamente. Ahora inicia sesión.")
        return redirect("login")
    return render(request, "register.html")

def soydisenador_view(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")
    
    nombre = request.user.first_name
    apellido = request.user.last_name
    tipo = request.user.profile.user_type
    if tipo != "designer":
        return redirect("index")
    return render(request, 'disenador.html')

def mipyme_view(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")
    nombre = request.user.first_name
    apellido = request.user.last_name
    tipo = request.user.profile.user_type
    if tipo != "mipyme":
        return redirect("index")
    return render(request, 'mipyme.html')  

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente")
    return redirect("index")