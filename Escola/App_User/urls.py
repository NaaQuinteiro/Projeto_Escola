from . import views
from django.urls import path

urlpatterns = [
    path ('', views.formulario_novo_user, name='cad_usuario'),
    path('salvar_usuario', views.salvar_usuario, name='salvar_usuario'),
]