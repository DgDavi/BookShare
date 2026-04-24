class Livro:
    def __init__(self, titulo, descricao, autor, user_id, disponivel = True, usuario_emprestimo=None, data_emprestimo=None, id=None):
        
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.autor = autor
        self.disponivel = disponivel
        self.usuario_emprestimo = usuario_emprestimo
        self.data_emprestimo = data_emprestimo
        self.user_id = user_id