import mysql.connector
import pandas as pd
import datetime
import os


class sql:
    def __init__(self):
        self._login = os.getenv('user_sql')
        self._senha = os.getenv('senha_sql')
        self.conexao = mysql.connector.connect(
            host = 'localhost',
            user = self._login,
            password = self._senha,
            database = 'relatorio_ifood', 
        )

        self.cursor = self.conexao.cursor()

    def criar_tabela_com_data(self):
        #Usa a data atual e formatação formatando para 'YYYY_MM_DD'
        data_atual = datetime.datetime.now().strftime("%Y_%m_%d")
        nome_tabela = f"Relatorio_{data_atual}"

        # Cria uma nova tabela com o nome da data atual
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {nome_tabela} (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                ROTAS VARCHAR(255),
                ENTREGAS INT,
                TOTAL_TAXAS DECIMAL(10, 2)
            );
        """)

        return nome_tabela

    def alimentar_tabela(self, df):
        nome_tabela = self.criar_tabela_com_data()
         # Substituir valores vazios ou não numéricos por 0 na coluna 'Entregas'
        df['Entregas'] = pd.to_numeric(df['Entregas'], errors='coerce').fillna(0).astype(int)

        for index, row in df.iterrows():
            self.cursor.execute(f"""
                INSERT INTO {nome_tabela} (ROTAS, ENTREGAS, TOTAL_TAXAS) 
                VALUES (%s, %s, %s)""", 
                (index, row['Entregas'], row['Total Taxa'])
            )
            #comita as mudanças
            self.conexao.commit()

        # Fechar a conexão
        self.cursor.close()
        self.conexao.close()

        