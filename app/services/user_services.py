from colorama import Fore

from data.db import get_db_connection
from model.usuario import Usuario
from utils.limpar_tela import limpar_tela
from utils.security import hash_senha
from repository.usuario_repository import criar_usuario
from utils.validador import validar_input, validar_novo_email, validar_nova_senha, validar_email_login, validar_senha_login, input_com_prompt_colorido


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
        input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
    
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
    input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")

    return usuario


