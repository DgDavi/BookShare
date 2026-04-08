from colorama import Fore

from .security import hash_senha

# Função para validar email  com @ e .com
def validar_email(email):
    return (
        "@" in email and
        "." in email and
        email.index("@") < email.index(".")
    )


# Função para validar senha com pelo menos 8 caracteres, uma letra maiúscula, um número e um caractere especial
def validar_senha(senha):
    maiuscula = any(c.isupper() for c in senha)
    numero = any(c.isdigit() for c in senha)
    especial = any(not c .isalnum() for c in senha)
    tamanho = len(senha) >= 8
    return maiuscula and numero and especial and tamanho


def validar_input(mensagem, validacao_funcao, mensagem_erro, *args):
    while True:
        valor = input(mensagem)
        if validacao_funcao(valor, *args):
            return valor
        else:
            if mensagem_erro and mensagem_erro.strip():
                print(mensagem_erro)


def validar_nova_senha():
    while True:
        senha = input(Fore.YELLOW + "👉 Digite sua nova senha: ")
        if not validar_senha(senha):
            print(Fore.RED + "❌ A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula, um número e um caractere especial")
            continue

        confirmacao = input(Fore.YELLOW + "👉 Digite sua senha novamente: ")

        if senha != confirmacao:
            print(Fore.RED + "❌ As senhas não coincidem.")
            print(Fore.YELLOW + "👉 Tente novamente.")
            continue

        return senha


def validar_novo_email(email, cursor):

    if not validar_email(email):
        print(Fore.RED + "❌ Formatação do email incorreta.")
        return False

    cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))

    if cursor.fetchone()[0] == 1:
        print(Fore.RED + "❌ Email já cadastrado.")
        return False
    
    return True


def validar_email_login(email, cursor):

    cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
    if cursor.fetchone()[0] == 0:
        print(Fore.RED + "❌ Email não encontrado.")
        return False
    return True


def validar_senha_login(senha, email, cursor):
    senha_hashed = hash_senha(senha)

    cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    if not resultado:
        return False
    senha_original = resultado[0]

    if senha_hashed != senha_original:
        return False
    return True
