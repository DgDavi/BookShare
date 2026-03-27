from utils.validador import validar_email, validar_senha
from utils.security import hash_senha
from data.db import get_db_connection
from data.schema import create_tables


# Função para cadastrar um novo usuário
def cadastrar_usuario():

    # Criar tabelas se não existirem
    create_tables()
    
    conexao = get_db_connection()
    cursor = conexao.cursor()

    # Validação do nome
    while True:
        nome = input("Digite seu nome: ")
        if len(nome) > 50 or len(nome) < 3:
            print("O nome deve conter entre 3 e 50 caracteres.")
            print("Tente novamente.")
        else:
            break
        
    # Validação do email
    while True:
        email = input("Digite seu email: ")
        if validar_email(email):
            break
        else:
            print("Email inválido.")
            print("Tente novamente.")

    # Validação da senha
    while True:
        senha = input("Digite sua senha: ")
        if validar_senha(senha):
            senha_hashed = hash_senha(senha)
            break
        else:
            print("A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula, um número e um caractere especial.")
            print("Tente novamente.")


    # Inseri o novo usuário no banco de dados
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hashed))
    conexao.commit()

    print("Usuário cadastrado com sucesso!")

    cursor.close()
    conexao.close()


# Função para realizar o login do usuário
def login_usuario():
    conexao  = get_db_connection()
    cursor = conexao.cursor()

    while True:
        email = input("Digite seu email: ")

        # Verifica se o email existe no banco de dados
        cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
        if cursor.fetchone()[0] == 1:
            break
        else:
            print("Email não encontrado.")
            print("Tente novamente.")

    while True:
        senha = input("Digite sua senha: ")

        # Transforma a senha digitada em hash e compara com a senha armazenada no banco de dados para aquele email
        senha_hashed = hash_senha(senha)
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        senha_armazenada = cursor.fetchone()[0]
        if senha_hashed == senha_armazenada:
            print("Login bem-sucedido!")
            break
        else:
            print("Senha incorreta.")
            print("Tente novamente.")


    cursor.close()
    conexao.close()