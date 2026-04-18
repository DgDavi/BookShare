from colorama import Fore


def criar_usuario(usuario, cursor):
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", 
                   (usuario.nome, usuario.email, usuario.senha_hashed))
    
    usuario.id = cursor.lastrowid

    return usuario
    

def buscar_dados_usuario(usuario, cursor):
    cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ?", (usuario.email,))
    dados_usuario = cursor.fetchone()
    return dados_usuario


def deletar_usuario(usuario, cursor):
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario.id,))
    return True


def editar_email(usuario, email, cursor):
    cursor.execute("UPDATE usuarios SET email = ? WHERE id = ?", (email, usuario.id))
    usuario.email = email
    
    cursor.execute("SELECT email FROM usuarios WHERE id = ?", (usuario.id,))
    resultado = cursor.fetchone()

    if resultado is None:
        return False
    
    novo_email = resultado[0]
    return novo_email == usuario.email


def editar_nome(usuario, nome, cursor):
    cursor.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (nome, usuario.id))
    usuario.nome = nome

    cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario.id,))
    resultado = cursor.fetchone()

    if resultado is None:
        return False
    
    novo_nome = resultado[0]
    return novo_nome == usuario.nome


def editar_senha(usuario, senha, cursor):
    cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (senha, usuario.id))
    usuario.senha_hashed = senha

    cursor.execute("SELECT senha FROM usuarios WHERE id = ?", (usuario.id,))
    resultado = cursor.fetchone()

    if resultado is None:
        return False
    
    nova_senha = resultado[0]
    return nova_senha == usuario.senha_hashed