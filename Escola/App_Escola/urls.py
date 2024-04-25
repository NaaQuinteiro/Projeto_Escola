from . import views
from django.urls import path

# Rotas do projeto 
urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('login/', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro/', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('salvar_turma', views.salvar_turma_nova, name='salvar_turma_nova'),
    path('lista_turma/<int:id_professor>', views.lista_turma, name='lista_turma'),
    path('lista_atividade/<int:id_selecionado>', views.lista_atividade, name='lista_atividade' ),
    path('salvar_atividade_nova', views.salvar_atividade_nova, name='salvar_atividade_nova'),
    path('valida_excluir/<int:id_turma>', views.valida_excluir, name='valida_excluir'),
    path('atividade_arquivos/<str:nome_arquivo>', views.exibir_arquivo, name='exibir_arquivo'),
    path('sair', views.sair, name='sair')
    
]
