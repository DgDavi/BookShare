from datetime import datetime, timedelta

from data.db import get_db_connection

class LivroRepository:
    def criar_livro(self, livro):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "INSERT INTO livros (user_id, titulo, descricao, autor, disponivel) VALUES (?, ?, ?, ?, ?)",
                (livro.user_id, livro.titulo, livro.descricao, livro.autor, int(livro.disponivel))
            )
            livro.id = cursor.lastrowid
            conexao.commit()
            return livro
        finally:
            cursor.close()
            conexao.close()


    def buscar_livros_usuario(self, usuario):
        conexao = get_db_connection()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
                "FROM livros WHERE user_id = ?",
                (usuario.id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    

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
    

    def buscar_livros(self, termo):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            termo_busca = f"%{termo}%"
            cursor.execute(
                "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
                "FROM livros WHERE LOWER(TRIM(titulo)) LIKE ? OR LOWER(TRIM(autor)) LIKE ?",
                (termo_busca, termo_busca)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    def buscar_livro_por_id(self, livro_id):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
                "FROM livros WHERE id = ?",
                (livro_id,)
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()


    def buscar_livros_emprestados(self, usuario_id):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
                "FROM livros WHERE usuario_emprestimo = ? AND disponivel = 0",
                (usuario_id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    def usuario_tem_emprestimo_ativo(self, usuario_id):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT COUNT(1) FROM livros WHERE usuario_emprestimo = ? AND disponivel = 0",
                (usuario_id,)
            )
            resultado = cursor.fetchone()
            return resultado[0] > 0
        finally:
            cursor.close()
            conexao.close()


    def emprestar_livro_repo(self, livro_id, usuario_id, data_emprestimo):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
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
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()


    def devolver_livro_repo(self, livro_id):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
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
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()
            
    def atualizar_status_livro(self):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("""
                SELECT id, data_emprestimo
                FROM livros
                WHERE disponivel = 0
            """)
            livros = cursor.fetchall()

            livros_atualizados = 0

            for livro_id, data_emprestimo in livros:
                if not data_emprestimo:
                    continue

                data = datetime.strptime(data_emprestimo, "%Y-%m-%d %H:%M:%S")
                if datetime.now() > data + timedelta(days=7):
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
                    livros_atualizados += 1

            conexao.commit()
            return livros_atualizados
        finally:
            cursor.close()
            conexao.close()
        