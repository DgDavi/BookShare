from colorama import Fore


class Usuario:
    def __init__(self, nome, email, senha_hashed, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hashed = senha_hashed

def criar_usuario(usuario, cursor):
    
    # Inseri o novo usuário no banco de dados
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
    cursor.execute("DELETE FROM usuarios WHERE email = ?", (usuario.email,))
    return True