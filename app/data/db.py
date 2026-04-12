import sqlite3

# Função para obter uma conexão com o banco de dados
def get_db_connection():
    conexao = sqlite3.connect('usuarios.db')
    conexao.execute('PRAGMA foreign_keys = ON')
    conexao.row_factory = sqlite3.Row
    return conexao
