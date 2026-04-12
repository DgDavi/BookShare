import sqlite3

# Função para obter uma conexão com o banco de dados
def get_db_connection():
    conexao = sqlite3.connect('usuarios.db')
    conexao.row_factory = sqlite3.Row
    return conexao

def get_db_connection_livros():
    conexao = sqlite3.connect('livros.db')
    conexao.row_factory = sqlite3.Row
    return conexao