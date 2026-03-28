from data.db import get_db_connection


def create_usuario(nome, email, senha_hashed):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hashed))
    conexao.commit()

     # Inseri o novo usuário no banco de dados