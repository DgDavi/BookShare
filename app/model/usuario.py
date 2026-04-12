class Usuario:
    def __init__(self, nome, email, senha_hashed, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hashed = senha_hashed