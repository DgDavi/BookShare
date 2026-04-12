def criar_livro(livro, cursor):
    cursor.execute(
        "INSERT INTO livros (user_id, titulo, descricao) VALUES (?, ?, ?)",
        (livro.user_id, livro.titulo, livro.descricao)
    )
    livro.id = cursor.lastrowid
    return livro