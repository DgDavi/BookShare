class Livro:
    def __init__(self, titulo, descricao, user_id, id=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.user_id = user_id