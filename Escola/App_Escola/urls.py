from . import views
from django.urls import path

# Rotas do projeto 
urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('login/', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro/', views.confirmar_cadastro, name='confirmar_cadastro'),
    # path('pageProfessor/', views.abre_pageProfessor, name='abre_pageProfessor'),
    # path('cadastroAtividade/', views.abre_cadastroAtividade, name='abre_cadastroAtividade'),
    # path('cadastroTurma/', views.abre_cadastroTurma, name='abre_cadastroTurma'),    
    
]
