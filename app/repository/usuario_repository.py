from colorama import Fore


def criar_usuario(usuario, cursor):
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", 
                   (usuario.nome, usuario.email, usuario.senha_hashed))
    
    usuario.id = cursor.lastrowid

    return usuario
    

def buscar_dados_usuario(usuario, cursor):
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "📋 DADOS DO USUÁRIO".center(60))
    print(Fore.CYAN + "=" * 60)

    cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ?", (usuario.email,))
    dados_usuario = cursor.fetchone()

    if dados_usuario:
        print(Fore.LIGHTMAGENTA_EX + "Id: " + Fore.WHITE + f"{dados_usuario[0]}")
        print(Fore.LIGHTMAGENTA_EX + "Nome: " + Fore.WHITE + f"{dados_usuario[1]}")
        print(Fore.LIGHTMAGENTA_EX + "Email: " + Fore.WHITE + f"{dados_usuario[2]}")
        return True

    print(Fore.RED + "❌ Nenhum dado de usuário encontrado.")
    return False


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