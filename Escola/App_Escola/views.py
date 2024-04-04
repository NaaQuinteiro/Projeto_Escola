from django.shortcuts import render
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages #Biblioteca de mensagens de Django

# Create your views here.
def abre_index(request):
    return render(request, 'Index.html')


def abre_login(request):
    return render(request, 'Login.html')


def abre_pageProfessor(request):
    return render(request, 'Page_professor.html')

def abre_cadastro(request):
    return render(request, 'Cadastro.html')


def abre_cadastroTurma(request):
    return render(request, 'CadastroTurma.html')

def abre_cadastroAtividade(request):
    return render(request, 'CadastroAtividade.html')

def initial_population():

    print("Vou popular")

    cursor = connection.cursor()

    # Popular Tabela Professor
    senha = '123456' # senha inical
    senha_armazenar = sha256(senha.encode()).hexdigest()
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof, Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Profa, Angela Markel', 'angela.markel@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Prof, Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "'),"

    cursor.execute(insert_sql_professor)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela proessor

    # Popular Tabela Turma
    #Montamos aqui nossa instrução SQL
    