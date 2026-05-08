class LivroRepository:
    def criar_livro(self, livro, cursor):
        cursor.execute(
            "INSERT INTO livros (user_id, titulo, descricao, autor, disponivel) VALUES (?, ?, ?, ?, ?)",
            (livro.user_id, livro.titulo, livro.descricao, livro.autor, int(livro.disponivel))
        )
        livro.id = cursor.lastrowid
        return livro

    def buscar_livros_usuario(self, usuario, cursor):
        cursor.execute(
            "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
            "FROM livros WHERE user_id = ?",
            (usuario.id,)
        )
        return cursor.fetchall()

    def editar_titulo(self, livro, titulo, cursor):
        cursor.execute(
            "UPDATE livros SET titulo = ? WHERE id = ?",
            (titulo, livro.id)
        )
        livro.titulo = titulo

        cursor.execute("SELECT titulo FROM livros WHERE id = ?", (livro.id,))
        resultado = cursor.fetchone()
        return resultado is not None and resultado[0] == livro.titulo

    def editar_descricao(self, livro, descricao, cursor):
        cursor.execute(
            "UPDATE livros SET descricao = ? WHERE id = ?",
            (descricao, livro.id)
        )
        livro.descricao = descricao

        cursor.execute("SELECT descricao FROM livros WHERE id = ?", (livro.id,))
        resultado = cursor.fetchone()
        return resultado is not None and resultado[0] == livro.descricao

    def deletar_livro(self, livro, cursor):
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro.id,))
        return True

    def buscar_livros(self, termo, cursor):
        termo_busca = f"%{termo}%"
        cursor.execute(
            "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
            "FROM livros WHERE LOWER(TRIM(titulo)) LIKE ? OR LOWER(TRIM(autor)) LIKE ?",
            (termo_busca, termo_busca)
        )
        return cursor.fetchall()

    def buscar_livro_por_id(self, livro_id, cursor):
        cursor.execute(
            "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
            "FROM livros WHERE id = ?",
            (livro_id,)
        )
        return cursor.fetchone()

    def buscar_livros_emprestados(self, usuario_id, cursor):
        cursor.execute(
            "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
            "FROM livros WHERE usuario_emprestimo = ? AND disponivel = 0",
            (usuario_id,)
        )
        return cursor.fetchall()

    def usuario_tem_emprestimo_ativo(self, usuario_id, cursor):
        cursor.execute(
            "SELECT COUNT(1) FROM livros WHERE usuario_emprestimo = ? AND disponivel = 0",
            (usuario_id,)
        )
        resultado = cursor.fetchone()
        return resultado[0] > 0

    def emprestar_livro_repo(self, livro_id, usuario_id, data_emprestimo, cursor):
        cursor.execute(
            """
            UPDATE livros
            SET disponivel = 0,
                usuario_emprestimo = ?,
                data_emprestimo = ?
            WHERE id = ?
            """,
            (usuario_id, data_emprestimo, livro_id)
        )

    def devolver_livro_repo(self, livro_id, cursor):
        cursor.execute(
            """
            UPDATE livros
            SET disponivel = 1,
                usuario_emprestimo = NULL,
                data_emprestimo = NULL
            WHERE id = ?
            """,
            (livro_id,)
        )