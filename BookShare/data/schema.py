from db import get_db_connection


def create_tables():
    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   senha TEXT NOT NULL 
                   )""")
    conexao.commit()
    return conexao, cursor
