import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()