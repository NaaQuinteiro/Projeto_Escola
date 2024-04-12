from . import views
from django.urls import path

# Rotas do projeto 
urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('login/', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro/', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('salvar_turma', views.salvar_turma_nova, name='salvar_turma_nova'),
    path('lista_turma/<int:id_professor>', views.lista_turma, name='lista_turma')
    # path('pageProfessor/', views.abre_pageProfessor, name='abre_pageProfessor'),
    # path('cadastroAtividade/', views.abre_cadastroAtividade, name='abre_cadastroAtividade'),
    # path('cadastroTurma/', views.abre_cadastroTurma, name='abre_cadastroTurma'),    
    
]
