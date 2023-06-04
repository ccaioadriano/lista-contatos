import PySimpleGUI as sg
import pandas as pd
import sqlite3

# Definir o layout da janela
layout = [
    [sg.Text('Nome:'), sg.Input(key='-NOME-', expand_x=True, pad=10)],
    [sg.Text('Email:'), sg.Input(key='-EMAIL-', expand_x=True, pad=10)],
    [sg.Text('Telefone:'), sg.Input(key='-TELEFONE-', enable_events=True, expand_x=True, pad=10)],
    [sg.Button('Adicionar'), sg.Button('Exportar')],
    [sg.Input(key='-PESQUISA-', enable_events=True), sg.Button('Pesquisar Contato')],
    [sg.Table(values=[], headings=['Nome', 'Email', 'Telefone'], auto_size_columns=True, justification='left', key='table_registros', expand_x=True)]
]

# Criar a janela
janela = sg.Window('Lista de contaos', layout)

# Loop principal
while True:
    # Ler os eventos e valores da janela
    evento, valores = janela.read()

    # Finalizar o programa se a janela for fechada
    if evento == sg.WINDOW_CLOSED:
        break
    
    if evento == 'Adicionar':
        sg.popup("Contato Adicionado com sucesso.")

janela.close()