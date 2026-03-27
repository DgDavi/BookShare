
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
    