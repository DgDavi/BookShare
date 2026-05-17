import bcrypt
import random
import string


def hash_senha(senha):
    senha_bytes = senha.encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_senha(senha, senha_hashed):
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hashed.encode("utf-8"))


def gerar_codigo(tamanho=6):
    return ''.join(random.choices(string.digits, k=tamanho))