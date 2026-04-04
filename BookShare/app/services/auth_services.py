from colorama import Fore

from data.db import get_db_connection
from model.usuario import criar_usuario
from utils.limpar_tela import limpar_tela
from utils.security import hash_senha
from utils.validador import validar_input, validar_email_cadastro, validar_input_senha, validar_email_login, validar_senha_login


# Função para cadastrar um novo usuário
def cadastrar_usuario():
    conexao = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    print(Fore.YELLOW + "📋 CADASTRO DE USUÁRIO\n" + Fore.CYAN + "-"*30)

    
    # conexao = get_db_connection()
    # cursor = conexao.cursor()

    # Validação do nome
    # while True:
    #     nome = input("\nDigite seu nome: ")
    #     if len(nome) > 50 or len(nome) < 3:
    #         print(Fore.RED + " ❌ O nome deve conter entre 3 e 50 caracteres.")
    #         print(Fore.YELLOW + "👉 Tente novamente.")
    #     else:
    #         break
    nome = validar_input(
        Fore.YELLOW + "👉 Digite seu nome: ",
        lambda n: 3 <= len(n) <= 50,
        Fore.RED + "❌ O nome deve conter entre 3 e 50 caracteres.\n" + Fore.YELLOW + "👉 Tente novamente."
    )
        
    # Validação do email
    # while True:
    #     email = input("Digite seu email: ")

    #     # Verifica se o email já existe no banco de dados
    #     cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))

    #     if cursor.fetchone()[0] == 1:
    #         print(Fore.RED + " ❌ Email já cadastrado.")
    #         print(Fore.YELLOW + "👉 Tente novamente.")
    #         continue

    #     # Verifica se o email tem um formato válido
    #     if validar_email(email):
    #         break
    #     else:
    #         print(Fore.RED + " ❌ Formatação de email inválida.")
    #         print(Fore.YELLOW + "👉 Tente novamente.")

    email = validar_input(
        Fore.YELLOW + "👉 Digite seu email: ",
        lambda e: validar_email_cadastro(e, cursor),
        ""
    )

    # Validação da senha
    # while True:
    #     senha = input("Digite sua senha: ")
    #     if not validar_senha(senha):
    #         print(Fore.RED + " ❌ A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula, um número e um caractere especial.")
    #         print(Fore.YELLOW + "👉 Tente novamente.")

    #     # Confirmação da senha
    #     confirmacao_senha = input("Confirme sua senha: ")
    #     if senha != confirmacao_senha:
    #         print(Fore.RED + " ❌ As senhas não coincidem.")
    #         print(Fore.YELLOW + "👉 Tente novamente."   )
    #     else:
    #         senha_hashed = hash_senha(senha)
    #         break

    senha = validar_input_senha()
    senha_hashed = hash_senha(senha)
    


    # Inseri o novo usuário no banco de dados
    criar_usuario(nome, email, senha_hashed)
    print(Fore.GREEN + "Usuário cadastrado com sucesso!")

    cursor.close()
    conexao.close()

    return True


# Função para realizar o login do usuário
def login_usuario():
    conexao  = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    print(Fore.YELLOW + "📋 LOGIN DE USUÁRIO\n" + Fore.CYAN + "-"*30)

    # while True:
        
    #     email = input("Digite seu email: ")

    #     # Verifica se o email existe no banco de dados
    #     cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
    #     if cursor.fetchone()[0] == 1:
    #         break
    #     else:
    #         print(Fore.RED + " ❌ Email não encontrado.")
    #         print(Fore.YELLOW + "👉 Tente novamente.")

    email = validar_input(
        Fore.YELLOW + "👉 Digite seu email: ",
        lambda e: validar_email_login(e, cursor),
        ""
    )


    # while True:
    #     senha = input("Digite sua senha: ")

    #     # Transforma a senha digitada em hash e compara com a senha armazenada no banco de dados para aquele email
    #     senha_hashed = hash_senha(senha)
    #     cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
    #     senha_armazenada = cursor.fetchone()[0]
    #     if senha_hashed == senha_armazenada:
    #         print(Fore.GREEN + "Login bem-sucedido!")
    #         input(Fore.CYAN + "Pressione Enter para continuar...")
    #         break
    #     else:
    #         print(Fore.RED + " ❌ Senha incorreta.")
    #         print(Fore.YELLOW + "👉 Tente novamente.")

    senha = validar_input(
        Fore.YELLOW + "👉 Digite sua senha: ",
        lambda s: validar_senha_login(s, email, cursor),
        Fore.RED + "❌ Senha incorreta."
    )

    cursor.close()
    conexao.close()

    return True