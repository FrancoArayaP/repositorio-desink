from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout
from .models import Portfolio, Project, Profile, Conversation, Message
from django.utils import timezone
from django.db.models import Q
from .firebase_conf import storage, firebaseConfig
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import get_or_create_conversation



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
    # limpiar mensajes previos
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    # validar autenticación
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")

    # validar tipo de usuario
    tipo = getattr(request.user.profile, "user_type", None)
    if tipo != "designer":
        return redirect("index")

    # datos básicos del usuario
    nombre = request.user.first_name
    apellido = request.user.last_name
    photo_url = getattr(request.user.profile, "photo_url", None)
    about_me = getattr(request.user.profile, "about_me", "")

    # portafolio del diseñador
    portfolios = Portfolio.objects.filter(user=request.user)

    # contexto para el template
    context = {
        "nombre": nombre,
        "apellido": apellido,
        "tipo": tipo,
        "photo_url": photo_url,
        "about_me": about_me,
        "portfolios": portfolios,
    }

    return render(request, "disenador.html", context)

def mipyme_view(request):
    # limpiar mensajes previos
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    # validar autenticación
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")

    # validar tipo de usuario
    tipo = getattr(request.user.profile, "user_type", None)
    if tipo != "mipyme":
        return redirect("index")

    # datos básicos del usuario
    nombre = request.user.first_name
    apellido = request.user.last_name
    photo_url = getattr(request.user.profile, "photo_url", None)
    about_me = getattr(request.user.profile, "about_me", "")

    # proyectos asociados a la MiPyme
    projects = Project.objects.filter(user=request.user)

    # contexto para el template
    context = {
        "nombre": nombre,
        "apellido": apellido,
        "tipo": tipo,
        "photo_url": photo_url,
        "about_me": about_me,
        "projects": projects,
    }

    return render(request, "mipyme.html", context)

def logout_view(request):
    logout(request)
    return redirect("index")

def perfil_disenador(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")

    tipo = request.user.profile.user_type
    if tipo != "designer":
        return redirect("index")
    #foto de perfil
    if request.method == "POST" and "profile_photo" in request.FILES:
        file = request.FILES["profile_photo"]
        file_ext = file.name.split('.')[-1]
        file_name = f"profile_photos/{request.user.username}.{file_ext}"

        upload = storage.child(file_name).put(file)

        token = upload.get("downloadTokens")
        bucket = firebaseConfig["storageBucket"]

        # Generar URL pública
        photo_url = (
            f"https://firebasestorage.googleapis.com/v0/b/{bucket}/o/"
            f"profile_photos%2F{request.user.username}.{file_ext}"
            f"?alt=media&token={token}"
        )

        # Guardar URL en el usuario
        request.user.profile.photo_url = photo_url
        request.user.profile.save()
        return redirect("perfil_disenador")
    #acerca de mi
    if request.method == "POST" and "about_me" in request.POST:
        about_me_text = request.POST.get("about_me")
        request.user.profile.about_me = about_me_text
        request.user.profile.save()
        return redirect("perfil_disenador")
    
    if request.method == "POST" and "portfolio_title" in request.POST:
        title = request.POST.get("portfolio_title")
        description = request.POST.get("portfolio_description")
        image = request.FILES.get("portfolio_image")

        image_url = None
        if image:
            safe_name = f"portfolio/{request.user.username}_{title}.jpg"
            storage.child(safe_name).put(image)
            image_url = storage.child(safe_name).get_url(None)

        Portfolio.objects.create(
            user=request.user,
            title=title,
            description=description,
            image_url=image_url
        )
        return redirect("perfil_disenador")
    portfolios = Portfolio.objects.filter(user=request.user)

    context = {
        "nombre": request.user.first_name,
        "apellido": request.user.last_name,
        "tipo": tipo,
        "photo_url": request.user.profile.photo_url,
        "about_me": getattr(request.user.profile, "about_me", ""),
        "portfolios": portfolios,
    }
    return render(request, "perfil_disenador.html", context)

def eliminar_portfolio(request, portfolio_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("login")

    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    portfolio.delete()
    return redirect("perfil_disenador")

def perfil_mipyme(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")

    tipo = request.user.profile.user_type
    if tipo != "mipyme":
        return redirect("index")
    #foto de perfil
    if request.method == "POST" and "profile_photo" in request.FILES:
        file = request.FILES["profile_photo"]
        file_ext = file.name.split('.')[-1]
        file_name = f"profile_photos/{request.user.username}.{file_ext}"

        upload = storage.child(file_name).put(file)

        token = upload.get("downloadTokens")
        bucket = firebaseConfig["storageBucket"]

        # Generar URL pública
        photo_url = (
            f"https://firebasestorage.googleapis.com/v0/b/{bucket}/o/"
            f"profile_photos%2F{request.user.username}.{file_ext}"
            f"?alt=media&token={token}"
        )

        # Guardar URL en el usuario
        request.user.profile.photo_url = photo_url
        request.user.profile.save()
        return redirect("perfil_mipyme")
    #acerca de mi
    if request.method == "POST" and "about_me" in request.POST:
        about_me_text = request.POST.get("about_me")
        request.user.profile.about_me = about_me_text
        request.user.profile.save()
        return redirect("perfil_mipyme")
    # Guardar nuevo proyecto
    if request.method == "POST" and "project_title" in request.POST:
        title = request.POST.get("project_title")
        description = request.POST.get("project_description")
        salary_min = request.POST.get("salary_min")
        salary_max = request.POST.get("salary_max")

        Project.objects.create(
            user=request.user,
            title=title,
            description=description,
            salary_min=salary_min,
            salary_max=salary_max
        )
        messages.success(request, "Proyecto agregado correctamente.")
        return redirect("perfil_mipyme")

    projects = Project.objects.filter(user=request.user)

    context = {
        "nombre": request.user.first_name,
        "apellido": request.user.last_name,
        "tipo": tipo,
        "photo_url": getattr(request.user.profile, "photo_url", None),
        "about_me": getattr(request.user.profile, "about_me", ""),
        "projects": projects,
    }
    return render(request, "perfil_mipyme.html", context)

def eliminar_proyecto(request, project_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("login")

    proyecto = get_object_or_404(Project, id=project_id, user=request.user)
    proyecto.delete()
    messages.success(request, "Proyecto eliminado correctamente.")
    return redirect("perfil_mipyme")

@login_required(login_url="login")
def buscar_disenadores_view(request):
    query = request.GET.get("q", "")

    # filtrar perfiles de tipo 'designer'
    designers_qs = Profile.objects.filter(user_type="designer")

    if query:
        designers_qs = designers_qs.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(about_me__icontains=query)
        )

    designers = []
    for d in designers_qs.select_related("user"):
        if not hasattr(d, "user") or d.user is None:
            continue

        portfolios = Portfolio.objects.filter(user=d.user)

        designers.append({
            "id": d.user.id,
            "nombre": d.user.first_name,
            "apellido": d.user.last_name,
            "photo_url": getattr(d, "photo_url", None),
            "about_me": getattr(d, "about_me", ""),
            "portfolios": portfolios,
        })

    context = {
        "designers": designers,
        "query": query,
    }
    return render(request, "buscar_disenadores.html", context)

@login_required(login_url="login")
def buscar_proyectos_view(request):
    query = request.GET.get("q", "")

    # filtrar proyectos
    projects_qs = Project.objects.all()
    if query:
        projects_qs = projects_qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    projects = []
    for p in projects_qs.select_related("user__profile"):
        projects.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "salary_min": p.salary_min,
            "salary_max": p.salary_max,
            "user": p.user,
            "profile": getattr(p.user, "profile", None),
        })

    context = {
        "projects": projects,
        "query": query,
    }
    return render(request, "buscar_proyectos.html", context)

def inbox(request, conversation_id=None):
    """
    Vista principal: lista de conversaciones a la izquierda y chat actual a la derecha.
    Si conversation_id es None muestra panel vacío a la derecha.
    POST en esta vista crea un mensaje en la conversación actual.
    """
    # Todas las conversaciones del usuario (más recientes primero por último mensaje)
    conversations = Conversation.objects.filter(participants=request.user).distinct().order_by('-created_at')

    conversation = None
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        # seguridad: sólo participantes pueden ver
        if not conversation.participants.filter(id=request.user.id).exists():
            return redirect('inbox')

        if request.method == "POST":
            text = request.POST.get("text", "").strip()
            if text:
                Message.objects.create(conversation=conversation, sender=request.user, text=text)
            return redirect('conversation_detail', conversation_id=conversation.id)

    context = {
        "conversations": conversations,
        "conversation": conversation,
    }
    return render(request, "conversation_detail.html", context)

@login_required
def conversation_start(request, user_id):
    """
    Crear o recuperar conversación entre request.user y user_id, redirigir a detalle.
    """
    other = get_object_or_404(User, id=user_id)
    if other == request.user:
        return redirect('inbox')

    conv = get_or_create_conversation(request.user, other)
    return redirect('conversation_detail', conversation_id=conv.id)