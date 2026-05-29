import bcrypt
import random
import string


def hash_senha(senha):
    """Gera o hash de uma senha."""
    senha_bytes = senha.encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_senha(senha, senha_hashed):
    """Compara uma senha em texto puro com o hash salvo."""
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hashed.encode("utf-8"))


def gerar_codigo(tamanho=6):
    """Gera um código numérico aleatório."""
    return ''.join(random.choices(string.digits, k=tamanho))