"""
URL configuration for desinkSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from desinkApp import views as appViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', appViews.index, name='index'),
    path('login/', appViews.login_view, name='login'),
    path('register/', appViews.register_view, name='register'),
    path('disenador/', appViews.soydisenador_view, name='disenador'),
    path('mipyme/', appViews.mipyme_view, name='mipyme'),
    path('logout/', appViews.logout_view, name='logout'),
    path('perfil_disenador/', appViews.perfil_disenador, name='perfil_disenador'),
    path("eliminar_portfolio/<int:portfolio_id>/", appViews.eliminar_portfolio, name="eliminar_portfolio"),
    path("perfil_mipyme/", appViews.perfil_mipyme, name="perfil_mipyme"),
    path("eliminar_proyecto/<int:project_id>/", appViews.eliminar_proyecto, name="eliminar_proyecto"),
    path('buscar_disenadores/', appViews.buscar_disenadores_view, name='buscar_disenadores'),
    path('buscar_proyectos/', appViews.buscar_proyectos_view, name='buscar_proyectos'),
    path("mensajes/", appViews.inbox, name="inbox"),
    path("mensajes/start/<int:user_id>/", appViews.conversation_start, name="conversation_start"),
    path("mensajes/<int:conversation_id>/", appViews.inbox, name="conversation_detail"),
]
