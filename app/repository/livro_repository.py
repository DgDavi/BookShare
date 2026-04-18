def criar_livro(livro, cursor):
    cursor.execute(
        "INSERT INTO livros (user_id, titulo, descricao, autor, disponivel) VALUES (?, ?, ?, ?, ?)",
        (livro.user_id, livro.titulo, livro.descricao, livro.autor, int(livro.disponivel))
    )
    livro.id = cursor.lastrowid
    return livro


def buscar_livros_usuario(usuario, cursor):
    cursor.execute(
        "SELECT id, user_id, titulo, descricao FROM livros WHERE user_id = ?",
        (usuario.id,)
    )
    return cursor.fetchall()


def editar_titulo(livro, titulo, cursor):
    cursor.execute(
        "UPDATE livros SET titulo = ? WHERE id = ?",
        (titulo, livro.id)
    )

    livro.titulo = titulo

    cursor.execute(
        "SELECT titulo FROM livros WHERE id = ?",
        (livro.id,)
    )
    resultado = cursor.fetchone()

    if resultado is None:
        return False

    novo_titulo = resultado[0]
    return novo_titulo == livro.titulo


def editar_descricao(livro, descricao, cursor):
    cursor.execute(
        "UPDATE livros SET descricao = ? WHERE id = ?",
        (descricao, livro.id)
    )

    livro.descricao = descricao

    cursor.execute(
        "SELECT descricao FROM livros WHERE id = ?",
        (livro.id,)
    )
    resultado = cursor.fetchone()

    if resultado is None:
        return False

    nova_descricao = resultado[0]
    return nova_descricao == livro.descricao


def deletar_livro(livro, cursor):
    cursor.execute(
        "DELETE FROM livros WHERE id = ?",
        (livro.id,)
    )
    return True


def buscar_livros(livro, cursor):
    termo_busca = f"%{livro}%"
    cursor.execute(
        "SELECT id, user_id, titulo, descricao, autor, disponivel FROM livros WHERE titulo LIKE ? OR autor LIKE ?",
        (termo_busca, termo_busca)
    )
    resultado = cursor.fetchall()

    return resultado