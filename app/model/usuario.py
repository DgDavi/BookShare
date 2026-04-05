from data.db import get_db_connection


class Usuario:
    def __init__(self, nome, email, senha_hashed, id=None):
        self.id = id
        self.nome = nome
        self.emial = email
        self.senha = senha_hashed

def criar_usuario(usuario, cursor):
    
    # Inseri o novo usuário no banco de dados
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", 
                   (usuario.nome, usuario.email, usuario.senha_hashed))
    
    usuario.id = cursor.lastrowid

    return usuario
    