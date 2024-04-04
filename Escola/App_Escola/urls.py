from . import views
from django.urls import path

# Rotas do projeto 
urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('login/', views.abre_login, name='abre_login'),
    path('cadastro/', views.abre_cadastro, name='abre_Cadastro'),
    path('pageProfessor/', views.abre_pageProfessor, name='abre_pageProfessor'),
    path('cadastroAtividade/', views.abre_cadastroAtividade, name='abre_cadastroAtividade'),
    path('cadastroTurma/', views.abre_cadastroTurma, name='abre_cadastroTurma'),    
    
]
