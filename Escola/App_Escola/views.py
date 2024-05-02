import mimetypes
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from hashlib import sha256
from .models import Professor
from .models import Turma 
from .models import Atividade
from django.db import connection, transaction
from django.contrib import messages #Biblioteca de mensagens de Django
import openpyxl

# Create your views here.

def initial_population():

    print("Vou popular")

    cursor = connection.cursor()

    # Popular Tabela Professor
    senha = '123456' # senha inical
    senha_armazenar = sha256(senha.encode()).hexdigest()
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof, Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Profa, Angela Markel', 'angela.markel@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Prof, Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "')"
    print('\ninseriu professor\n')
    cursor.execute(insert_sql_professor)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela proessor

    #----------------------------------------------------------------------------------------------------------------------------------------
    # Popular Tabela Turma
    #Montamos aqui nossa instrução SQL
    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1o Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2o Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3o Semestre - Desenvolvimento de Sistemas', 3)"
    print('\ninseriu turma\n')


    cursor.execute(insert_sql_turma)
    transaction.atomic() #Necessario commit para insert e update

    #Fim da população da tabela Turma


    #-----------------------------------------------------------------------------------------------------------------------------------------
    #Populando a Tabela Atividade 
    #Montamos aqui nossa instrução SQL
    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de Programação', 1),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Framework Django', 2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Conceitos de Gerenciamento de Projetos', 3)"
    print('\ninseriu atividade\n')

    cursor.execute(insert_sql_atividade)
    transaction.atomic() #Aqui ele garante que ou ele salva todas as linhas no banco, se não não salva nenhuma

    #Fim da População da tabela Atividade 

    print("Populado")



def abre_index(request):
    #return render(request, 'Index.html')
    dado_pesquisa = 'Obama'

    verifica_populado = Professor.objects.filter(nome__icontains = dado_pesquisa)

    if len(verifica_populado) == 0:
        print("Não está populado")
        initial_population() # chama a função para realizar a população
    else: 
        print("Achei o Obama", verifica_populado)

    return render(request, 'Login.html')

def enviar_login(request):

    if (request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email= email).values("nome", "senha", "id")
        print("\nDados do Professor ", dados_professor)

        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']

            if (senha == senha_criptografada):

                #Se logou corretamente traz as turmas do professor, para isso instalciamos o models turmas do professor 
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor = id_logado)
                print("\nTurma do professor ", turmas_do_professor)

                return render(request, 'Page_professor.html', {'usuario_logado': usuario_logado,
                                                                 'turmas_do_professor': turmas_do_professor,
                                                                 'id_logado': id_logado})
            else:
                messages.info(request, 'Usuario ou senha incorretos. Tente Novamente.')
                return render(request, 'Login.html')
        
        messages.info(request, 'Olá' + email + ', seja bem vindo! Percebemos que você é novo por aqui. Complete o seu cadastro.')
        return render(request, 'Cadastro.html', {'login': email})     


def confirmar_cadastro(request):

    if (request.method == 'POST'):
        nome = request.POST.get("nome")
        email= request.POST.get('login')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()

        grava_professor = Professor(
            nome = nome,
            email = email,
            senha = senha_criptografada
        )
        grava_professor.save()

        mensagem = "OLÁ PROFESSOR " +nome+ ", SEJA BEM VINDO!"
        return HttpResponse(mensagem)
    
def cad_turma(request, id_professor):
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']

    return render(request, 'CadastroTurma.html', {'usuario_logado': usuario_logado, 'id_logado': id_professor})

def salvar_turma_nova(request):
    if(request.method == 'POST'):
        nome_turma = request.POST.get('nome_turma')
        id_professor = request.POST.get('id_professor')
        professor = Professor.objects.get(id=id_professor)
        grava_turma = Turma(
            nome_turma=nome_turma,
            id_professor=professor,
        )

        grava_turma.save()
        messages.info(request, 'Turma ' + nome_turma + ' cadastrado com sucesso.')

        #redirecionando para nova url após gravação vem sucedida 
        return redirect('lista_turma', id_professor=id_professor)
        

def lista_turma(request, id_professor):
    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    id_logado = dados_professor[0]
    id_logado = id_logado['id']
    turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
    return render(request, 'Page_professor.html',
                  {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor,
                   'id_logado': id_logado})


# PARTE NOVA SE DER ERRO APAGA Q DA TUDO CERTO

def salvar_atividade_nova(request):
    if(request.method == 'POST'):
        nome_atividade = request.POST.get('nome_atividade')
        id_selecionado = request.POST.get('id_selecionado')    
        print(f'salvar_atividade{nome_atividade}{id_selecionado}') 

        turma = Turma.objects.get(id=id_selecionado)     

        arquivo = request.FILES.get('arquivo')   
        print (arquivo) 

        grava_atividade = Atividade(
            nome_atividade = nome_atividade,
            id_turma=turma,
            arquivo = arquivo
        )
        print(f'resultados de salvar atividade {nome_atividade}{turma}{arquivo}')

        grava_atividade.save()

        return redirect('lista_atividade', id_selecionado=id_selecionado)


def lista_atividade(request, id_selecionado):
    print(f'captura da turma {id_selecionado}')
    dados_turma = Turma.objects.filter(id=id_selecionado).values('nome_turma', 'id')
    print(f'dados da Turma {dados_turma}')
   
    atividades_da_turma = Atividade.objects.filter(id_turma = id_selecionado)
    print(f'Atividaes retornadas {atividades_da_turma}')
    print(id_selecionado)

    return render(request, 'CadastroAtividade.html',
                  {'atividades_da_turma': atividades_da_turma, 
                   'id_selecionado':id_selecionado })


# def valida_excluir(request, id_turma):
   
#     id_professor = request.GET.get('id_professor')
   
#     turma = get_object_or_404(Turma, id=id_turma)
   
#     if Atividade.objects.filter(id_turma=turma.id):
#         messages.info(request, 'Não é possível excluir esta turma pois ela tem atividades cadastradas.')
       
#         return redirect('lista_turma', id_professor=id_professor)
    
#     turma.delete()

#     return redirect('lista_turma', id_professor=id_professor)

def excluir_turma(request, id_turma):
    with transaction.atomic():
        turma = Turma.objects.get(pk=id_turma)
        id_professor = turma.id_professor_id

        turma.delete()

        professor = Professor.objects.get(pk=id_professor)
        turmas_professor = Turma.objects.filter(id_professor=id_professor)

    return render(request, "Page_professor.html", {
        "usuario_logado": professor.nome, 
        "turmas_do_professor": turmas_professor,
        "id_logado": id_professor
    })
def exibir_arquivo(request, nome_arquivo):
    caminho_arquivo = os.path.join('atividade_arquivos/', nome_arquivo)

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'rb') as arquivo:
            conteudo = arquivo.read()
        
        tipo_mimetype, _ = mimetypes.guess_type(caminho_arquivo)

        resposta = HttpResponse(conteudo, content_type=tipo_mimetype)

        resposta['Content-Disposition'] = 'inline; filename="' + nome_arquivo + '"'
        return resposta
    else:
        return HttpResponse('Arquivo não encontrado', status=404)


def exportar_para_excel_turmas(request):
    # Consulta para obter os dados que deseja exportar 
    dados_turma = Turma.objects.all()

    # Criando um novo arquivo excel 
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'TURMAS'

    #Escrevendo cabeçalhos 
    sheet["A1"] = 'ID'
    sheet["B1"] = 'NOME DA TURMA'

    #Escrevendo os dados 
    for index, turma in enumerate(dados_turma, start=2):
        sheet[f'A{index}'] = turma.id
        sheet[f'B{index}'] = turma.nome_turma


    #Salvando o arquivo Excel 
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=turma.xlsx'
    workbook.save(response)
    return response


def exportar_para_excel_Atividades(request):
    dados_atividades = Atividade.objects.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "ATIVIDADES"

    #Escrevendo cabeçalhos 
    sheet["A1"] = 'ID'
    sheet["B1"] = 'NOME DA ATIVIDADE'
    sheet["C1"] = 'TURMA'

    #Escrevendo os dados 
    for index, atividade in enumerate(dados_atividades, start=2):
        sheet[f'A{index}'] = atividade.id
        sheet[f'B{index}'] = atividade.nome_atividade
        sheet[f'C{index}'] = str(atividade.id_turma)
        
    #Salvando o arquivo Excel 
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=atividades.xlsx'
    workbook.save(response)
    return response 


def sair(request):
    return render(request, 'Login.html')