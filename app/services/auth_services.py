from colorama import Fore

from data.db import get_db_connection
from model.usuario import Usuario, criar_usuario
from utils.limpar_tela import limpar_tela
from utils.security import hash_senha
from utils.validador import validar_input, validar_email_cadastro, validar_input_senha, validar_email_login, validar_senha_login


# Função para cadastrar um novo usuário
def cadastrar_usuario():
    conexao = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    print(Fore.YELLOW + "📋 CADASTRO DE USUÁRIO\n" + Fore.CYAN + "-"*30)

    
    nome = validar_input(
        Fore.YELLOW + "👉 Digite seu nome: ",
        lambda n: 3 <= len(n) <= 50,
        Fore.RED + "❌ O nome deve conter entre 3 e 50 caracteres.\n" + Fore.YELLOW + "👉 Tente novamente."
    )
        

    email = validar_input(
        Fore.YELLOW + "👉 Digite seu email: ",
        lambda e: validar_email_cadastro(e, cursor),
        ""
    )


    senha = validar_input_senha()
    senha_hashed = hash_senha(senha)
    


    # Inseri o novo usuário no banco de dados
    usuario = Usuario(nome, email, senha_hashed)
    criar_usuario(usuario, cursor)
    print(Fore.GREEN + "Usuário cadastrado com sucesso!")
    
    conexao.commit()
    cursor.close()
    conexao.close()

    return True


# Função para realizar o login do usuário
def login_usuario():
    conexao  = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    print(Fore.YELLOW + "📋 LOGIN DE USUÁRIO\n" + Fore.CYAN + "-"*30)


    email = validar_input(
        Fore.YELLOW + "👉 Digite seu email: ",
        lambda e: validar_email_login(e, cursor),
        ""
    )


    senha = validar_input(
        Fore.YELLOW + "👉 Digite sua senha: ",
        lambda s: validar_senha_login(s, email, cursor),
        Fore.RED + "❌ Senha incorreta."
    )

    cursor.close()
    conexao.close()

    return True