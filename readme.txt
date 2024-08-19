# Projeto de Análise de Entregas e Envio de Relatório por Email

Este projeto é dividido em duas partes principais: a primeira realiza a análise de dados de entregas a partir de um arquivo Excel, gera um resumo das taxas por rota, e envia um relatório por email. A segunda parte insere esses dados processados em uma tabela MySQL, criando uma nova tabela a cada dia com a data no nome.

## Estrutura do Projeto

- `main.py`: Script principal que realiza a leitura do arquivo Excel, processamento dos dados, alimentação do banco de dados e envio do email.
- `sql_connection.py`: Script que contém a classe `sql`, responsável por gerenciar a conexão com o banco de dados MySQL, criar tabelas com base na data e inserir os dados processados.

## Funcionalidades

### `main.py`

- **Leitura do Arquivo Excel**: O usuário seleciona um arquivo Excel que contém os dados de entregas.
- **Cálculo das Taxas de Entrega**: O script processa o arquivo, somando as taxas de entrega por rota e gerando um resumo.
- **Envio do Relatório por Email**: O resumo é convertido em um arquivo Excel e enviado por email ao destinatário configurado.
- **Inserção no Banco de Dados**: Os dados processados são passados para o `sql_connection.py` para serem armazenados no MySQL.

### `sql_connection.py`

- **Conexão com MySQL**: Estabelece uma conexão com o banco de dados MySQL usando as credenciais armazenadas em variáveis de ambiente.
- **Criação de Tabela Diária**: Cria uma nova tabela no banco de dados com o nome baseado na data do dia em que o script é executado.
- **Inserção de Dados**: Insere os dados processados no `main.py` na tabela criada.

## Instalação

### Pré-requisitos

- Python 3.x
- MySQL
- As seguintes bibliotecas Python:
  - pandas
  - openpyxl
  - smtplib
  - tkinter
  - mysql-connector-python

### Como instalar

1. Clone este repositório:
    ```bash
    git clone https://github.com/seuusuario/analise-entregas.git
    ```

2. Acesse a pasta do projeto:
    ```bash
    cd analise-entregas
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Configuração

1. **Configuração das Variáveis de Ambiente**:

   Defina as seguintes variáveis de ambiente:

   - **Para o envio de email**:
     - `email_us`: Seu endereço de email.
     - `senha_app`: A senha de app gerada para o seu email.
     - `email_de`: O endereço de email do destinatário.

   - **Para a conexão com o MySQL**:
     - `user_sql`: Usuário do MySQL.
     - `senha_sql`: Senha do MySQL.

2. **Configuração do Banco de Dados**:

   Crie um banco de dados no MySQL chamado `relatorio_ifood` para armazenar as tabelas geradas diariamente.

   ```sql
   CREATE DATABASE relatorio_ifood;
