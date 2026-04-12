class Livros:
    def __init__(self, titulo, descricao, id=None, user_id=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.user_id = user_id