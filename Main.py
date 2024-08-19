import pandas as pd
import os
import smtplib
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from email.message import EmailMessage
from io import BytesIO
from sql_connection import sql




email = 'lucasaugusto995@gmail.com' #os.getenv('email_us')
senha = os.getenv('senha_app')
email_remetente = os.getenv('email_de')
db = sql()

def enviar_email(email, senha, remetente, excel):
#configuração do email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    email_remetente = str(email)
    senha_remetente = str(senha)
    email_destinatario = remetente

    # Criação da mensagem de email
    msg = EmailMessage()
    msg['Subject'] = 'Resultados da Análise'
    msg['From'] = email_remetente
    msg['To'] = email_destinatario
    msg.set_content('Olá, segue em anexo o arquivo com os resultados.')

    # Anexando o arquivo Excel ao email
    msg.add_attachment(excel.read(), maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='resultados.xlsx')

    # Enviando o email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_remetente, senha_remetente)
        server.send_message(msg)

    return print("Email enviado com sucesso!")


Tk().withdraw()

#abre a janela de dialogo para selecionar o arquivo    
arquivo = askopenfilename(
    title = 'Selecione o arquivo Excel',
    filetype= [("Arquivo Excel", "*.xlsx * .xls")]
)

#lê o arquivo excel
df = pd.read_excel(arquivo)

#soma as taxas de entrega
soma_taxa_entrega_geral = sum(df['Tx. Entrega'])

total_pedidos = []
pedidos_raio1 = df.query('Entregador == "RAIO 1"')

# contagem de pedidos por entregador
#pedidos_raio = pd.DataFrame(df)
pedidos_raio = df['Entregador'].value_counts()
pedidos_df = pedidos_raio.reset_index()
pedidos_df.columns = ['Entregador', 'Quantidade']
pedidos_df = pedidos_df.sort_values(by='Quantidade', ascending=False)

#adiciona a uma lista as entregas de cada rota
for i in pedidos_df['Quantidade']:
    total_pedidos.append(i)

#soma das taxas por entregador
soma_taxa_raio1 = df[df['Entregador'] == 'RAIO 1']['Tx. Entrega'].sum()
soma_taxa_raio2 = df[df['Entregador'] == "RAIO 2 "]['Tx. Entrega'].sum()
soma_taxa_raio3 = df[df['Entregador'] =='RAIO 3']['Tx. Entrega'].sum()
ifood = df[df['Entregador'] =='IFOOD']['Tx. Entrega'].sum()
total = soma_taxa_raio1 + soma_taxa_raio2 + soma_taxa_raio3 + ifood

#Dicionario com as informações tratadas de cada rota.
dicionario_rotas = {'ROTA 1': (total_pedidos[0], soma_taxa_raio1),
                    'ROTA 2': (total_pedidos[2], soma_taxa_raio2), 
                    'ROTA 3': (total_pedidos[1], soma_taxa_raio3), 
                    'IFOOD': (total_pedidos[3], ifood),
                    'Total em taxas': ('', total)
                    }

#convertendo o dicionário para um DataFrame e arredondando os valores
resultado_df = pd.DataFrame(dicionario_rotas).T
resultado_df.columns = ['Entregas', 'Total Taxa']
resultado_df['Total Taxa'] = resultado_df['Total Taxa'].round(2)

#Convertendo o DataFrame para um arquivo Excel em memória usando openpyxl
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
    resultado_df.to_excel(writer, index=True, sheet_name='Resumo')

excel_buffer.seek(0)

db.alimentar_tabela(resultado_df)

enviar_email(email, senha, email_remetente, excel_buffer)
