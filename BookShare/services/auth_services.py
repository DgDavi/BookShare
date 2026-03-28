from colorama import Fore

from data.db import get_db_connection
from data.schema import create_tables
from model.usuario import create_usuario
from utils.limpar_tela import limpar_tela
from utils.security import hash_senha
from utils.validador import validar_email, validar_senha

# Função para cadastrar um novo usuário
def cadastrar_usuario():
    limpar_tela()
    print(Fore.YELLOW + "📋 CADASTRO DE USUÁRIO\n" + Fore.CYAN + "-"*30)

    # Criar tabelas se não existirem
    create_tables()
    
    conexao = get_db_connection()
    cursor = conexao.cursor()

    # Validação do nome
    while True:
        nome = input("\nDigite seu nome: ")
        if len(nome) > 50 or len(nome) < 3:
            print(Fore.RED + " ❌ O nome deve conter entre 3 e 50 caracteres.")
            print(Fore.YELLOW + "👉 Tente novamente.")
        else:
            break
        
    # Validação do email
    while True:
        email = input("\nDigite seu email: ")

        # Verifica se o email já existe no banco de dados
        cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))

        if cursor.fetchone()[0] == 1:
            print(Fore.RED + " ❌ Email já cadastrado.")
            print(Fore.YELLOW + "👉 Tente novamente.")
            continue

        if validar_email(email):
            break
        else:
            print(Fore.RED + " ❌ Formatação de email inválida.")
            print(Fore.YELLOW + "👉 Tente novamente.")

    # Validação da senha
    while True:
        senha = input("\nDigite sua senha: ")
        if not validar_senha(senha):
            print(Fore.RED + " ❌ A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula, um número e um caractere especial.")
            print(Fore.YELLOW + "👉 Tente novamente.")

        # Confirmação da senha
        confirmacao_senha = input("Confirme sua senha: ")
        if senha != confirmacao_senha:
            print(Fore.RED + " ❌ As senhas não coincidem.")
            print(Fore.YELLOW + "👉 Tente novamente."   )
        else:
            senha_hashed = hash_senha(senha)
            break


    # Inseri o novo usuário no banco de dados
    create_usuario(nome, email, senha_hashed)
    print(Fore.GREEN + "Usuário cadastrado com sucesso!")

    cursor.close()
    conexao.close()


# Função para realizar o login do usuário
def login_usuario():
    limpar_tela()
    conexao  = get_db_connection()
    cursor = conexao.cursor()
    print(Fore.YELLOW + "📋 LOGIN DE USUÁRIO\n" + Fore.CYAN + "-"*30)

    while True:
        
        email = input("Digite seu email: ")

        # Verifica se o email existe no banco de dados
        cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
        if cursor.fetchone()[0] == 1:
            break
        else:
            print(Fore.RED + " ❌ Email não encontrado.")
            print(Fore.YELLOW + "👉 Tente novamente.")

    while True:
        senha = input("Digite sua senha: ")

        # Transforma a senha digitada em hash e compara com a senha armazenada no banco de dados para aquele email
        senha_hashed = hash_senha(senha)
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        senha_armazenada = cursor.fetchone()[0]
        if senha_hashed == senha_armazenada:
            print(Fore.GREEN + "Login bem-sucedido!")
            break
        else:
            print(Fore.RED + " ❌ Senha incorreta.")
            print(Fore.YELLOW + "👉 Tente novamente.")


    cursor.close()
    conexao.close()