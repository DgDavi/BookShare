class Livro:
    def __init__(self, titulo, descricao, autor, user_id, disponivel = True,  id=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.autor = autor
        self.disponivel = disponivel
        self.user_id = user_id