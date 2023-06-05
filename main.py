import PySimpleGUI as sg
import pandas as pd
import sqlite3


# Definir o layout da janela
layout = [
    [sg.Text('Nome:'), sg.Input(key='-NOME-', expand_x=True, pad=10, enable_events=True)],
    [sg.Text('Email:'), sg.Input(key='-EMAIL-', expand_x=True, pad=10, enable_events=True)],
    [sg.Text('Telefone:'), sg.Input(key='-TELEFONE-', expand_x=True, pad=10, enable_events=True)],
    [sg.Button('Adicionar'), sg.Button('Carregar contatos'), sg.Button('Exportar')],
    [sg.Input('Pesquisar contato por nome...', key='-PESQUISAR-', enable_events=True)],
    [sg.Table(values=[], headings=['Nome', 'Email', 'Telefone'], auto_size_columns=True, justification='left', key='table_contatos', expand_x=True, visible=False)]
]


def cria_database():
    
    try:
      # Criar uma conexão com o banco de dados
        conexao = sqlite3.connect('lista-contatos.db')

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Criar uma tabela
        cursor.execute('''CREATE TABLE IF NOT EXISTS contatos
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        email TEXT, 
                        telefone TEXT)''')

    except ValueError:
      print("OCORREU UMA EXCEÇÂO AO CRIAR O BANCO DE DADOS")
        
def insert_contato(nome, email, telefone):
    
    try:
        # Criar uma conexão com o banco de dados
        conexao = sqlite3.connect('lista-contatos.db')

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Criar um contato
        cursor.execute('INSERT INTO contatos (id, nome, email, telefone) VALUES (?, ?, ?, ?)', (None, nome, email, telefone))
        
        conexao.commit()
    except:
      print('OCORREU UMA EXCEÇÂO AO INSERIR UM CONTATO')


def listar_contatos():
    # Criar uma conexão com o banco de dados
    conexao = sqlite3.connect('lista-contatos.db')

    # Criar um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # executa o select
    cursor.execute("SELECT nome, email, telefone FROM contatos")

    contatos = cursor.fetchall()
    
    #deixa a lista de contatos em ordem alfabetica
    contatos.sort()
    
    return contatos


def limpar_campos():
    janela['-NOME-'].update('')
    janela['-EMAIL-'].update('')
    janela['-TELEFONE-'].update('')

def pesquisa_por_nome(nome):
    # Criar uma conexão com o banco de dados
    conexao = sqlite3.connect('lista-contatos.db')

    # Criar um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # executa o select
    cursor.execute("SELECT nome, email, telefone FROM contatos WHERE nome LIKE ?", (f"{nome}%",))

    contatos = cursor.fetchall()
    
    #deixa a lista de contatos em ordem alfabetica
    contatos.sort()
    
    return contatos

def atualizar_tabela(valores):
    janela['table_contatos'].update(values=valores)


# Criar a janela
janela = sg.Window('Lista de contaos', layout)

#INSTANCIA DO BD
cria_database()

# Loop principal
while True:
    # Ler os eventos e valores da janela
    evento, valores = janela.read()

    # Finalizar o programa se a janela for fechada
    if evento == sg.WINDOW_CLOSED:
        break
    
    if evento == 'Adicionar':
        #dados do contato
        nome = janela["-NOME-"].get()
        
        email = janela["-EMAIL-"].get()
        
        telefone = janela["-TELEFONE-"].get()
        
        # Verificar se os campos não estão vazios
        if nome.strip() and email.strip() and telefone.strip():
 
            insert_contato(nome, email, telefone)
            
            sg.popup('Contato adicionado com sucesso!')
            
            limpar_campos()
            
        else:
            sg.popup('Por favor, preencha todos os campos.')
    
    if evento == 'Carregar contatos':
        contatos = listar_contatos()
        atualizar_tabela(contatos)

    if evento == '-PESQUISAR-':
        
        
        contatos_pesquisados = pesquisa_por_nome(valores['-PESQUISAR-'])
        
        janela['table_contatos'].update(visible=True)
        
        atualizar_tabela(contatos_pesquisados)


janela.close()