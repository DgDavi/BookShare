from colorama import Fore

from data.db import get_db_connection
from model.usuario import Usuario
from utils.limpar_tela import limpar_tela
from utils.security import hash_senha
from utils.validador import validar_input, validar_novo_email, validar_nova_senha, validar_email_login, validar_senha_login


def cadastrar_usuario():
    conexao = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    print(Fore.YELLOW + "📋 CADASTRO DE USUÁRIO\n" + Fore.CYAN + "-"*30)
    print()

    
    nome = validar_input(
        Fore.YELLOW + "👉 Digite seu nome: ",
        lambda n: 3 <= len(n) <= 50,
        Fore.RED + "❌ O nome deve conter entre 3 e 50 caracteres.\n" + Fore.YELLOW + "👉 Tente novamente."
    )
        

    email = validar_input(
        Fore.YELLOW + "👉 Digite seu email: ",
        validar_novo_email,
        "",
        cursor
    )


    senha = validar_nova_senha()
    senha_hashed = hash_senha(senha)
    


    # Inseri o novo usuário no banco de dados
    usuario = Usuario(nome, email, senha_hashed)
    usuario_criado = criar_usuario(usuario, cursor)

    if usuario_criado:
        print(Fore.GREEN + "\nUsuário cadastrado com sucesso!")
        input(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
    
        conexao.commit()
        cursor.close()
        conexao.close()

        return usuario
    
    return None


def login_usuario():
    conexao  = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    print(Fore.YELLOW + "📋 LOGIN DE USUÁRIO\n" + Fore.CYAN + "-"*30)
    print()


    email = validar_input(
        Fore.YELLOW + "👉 Digite seu email: ",
        validar_email_login,
        "",
        cursor
    )


    senha = validar_input(
        Fore.YELLOW + "👉 Digite sua senha: ",
        validar_senha_login,
        Fore.RED + "❌ Senha incorreta.",
        email,
        cursor
    )

    cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,))
    usuario_logado = cursor.fetchone()

    if not usuario_logado:
        cursor.close()
        conexao.close()
        return None

    usuario = Usuario(
        nome=usuario_logado[1],
        email=usuario_logado[2],
        senha_hashed=usuario_logado[3],
        id=usuario_logado[0]
    )

    cursor.close()
    conexao.close()
    print(Fore.GREEN + "\nLogin realizado com sucesso!")
    input(Fore.GREEN + "Pressione a tecla Enter para seguir... ")

    return usuario


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