import hashlib

# Função que criptografa a senha usando SHA-256
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()