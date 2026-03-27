import sqlite3

def get_db_connection():
    conexao = sqlite3.connect('usuarios.db')
    conexao.row_factory = sqlite3.Row
    return conexao