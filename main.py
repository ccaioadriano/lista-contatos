import PySimpleGUI as sg
import pandas as pd
import sqlite3


# Definir o layout da janela
layout = [
    [sg.Text('Nome:'), sg.Input(key='-NOME-', expand_x=True, pad=10, enable_events=True)],
    [sg.Text('Email:'), sg.Input(key='-EMAIL-', expand_x=True, pad=10, enable_events=True)],
    [sg.Text('Telefone:'), sg.Input(key='-TELEFONE-', expand_x=True, pad=10, enable_events=True)],
    [sg.Button('Adicionar'), sg.Button('Exportar')],
    [sg.Input(key='-PESQUISAR-', enable_events=True)],
    [sg.Table(values=[], headings=['Nome', 'Email', 'Telefone'], auto_size_columns=True, justification='left', key='table_contatos', expand_x=True)]
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
    
    return contatos.sort()


def limpar_campos():
    janela['-NOME-'].update('')
    janela['-EMAIL-'].update('')
    janela['-TELEFONE-'].update('')


# Criar a janela
janela = sg.Window('Lista de contaos', layout)

#INSTANCIA DO BD
cria_database()

# Loop principal
while True:
    
    # Ler os eventos e valores da janela
    evento, valores = janela.read()

    #INICIA A LISTA DE CONTATOS
    table_values = listar_contatos()
    janela['table_contatos'].update(values=table_values)

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
    

    # #evento no campo NOME
    # if evento == '-NOME-':
    #     print(janela["-NOME-"].get())
        
    # #evento no campo EMAIL
    # if evento == '-EMAIL-':
    #     print(janela["-EMAIL-"].get())
        
    # #evento no campo TELEFONE
    # if evento == '-TELEFONE-':
    #     print(janela["-TELEFONE-"].get())
        
    # #evento no campo PESQUISAR
    # if evento == '-PESQUISAR-':
    #     print(janela["-PESQUISAR-"].get())
        
janela.close()