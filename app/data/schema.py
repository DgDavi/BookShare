from data.db import get_db_connection

# Função para criar as tabelas do banco de dados
def create_tables():
    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   senha TEXT NOT NULL 
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE)""")
    conexao.commit()
    return conexao, cursor
