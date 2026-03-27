from utils.validador import validar_email, validar_senha
from utils.security import hash_senha
from data.db import get_db_connection
from data.schema import create_tables


# Função para cadastrar um novo usuário
def cadastrar_usuario():
    from data.db import get_db_connection
    from utils.security import hash_senha

    # Criar tabelas se não existirem
    create_tables()
    
    conexao = get_db_connection()
    cursor = conexao.cursor()

    while True:
        nome = input("Digite seu nome: ")
        if len(nome) > 50 or len(nome) < 3:
            print("O nome deve conter entre 3 e 50 caracteres.")
            print("Tente novamente.")
        else:
            break
        
    while True:
        email = input("Digite seu email: ")
        if validar_email(email):
            break
        else:
            print("Email inválido.")
            print("Tente novamente.")

    while True:
        senha = input("Digite sua senha: ")
        if validar_senha(senha):
            senha_hashed = hash_senha(senha)
            break
        else:
            print("A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula, um número e um caractere especial.")
            print("Tente novamente.")


    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hashed))
    conexao.commit()

    print("Usuário cadastrado com sucesso!")

    cursor.close()
    conexao.close()