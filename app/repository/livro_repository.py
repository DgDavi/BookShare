from datetime import datetime, timedelta

from data.db import get_db_connection

from repository.mensagem_repository import MensagemRepository

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


    def emprestar_livro_repo(self, id, usuario_emprestimo, data_emprestimo):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            #Buscar nome livro e dono do livro
            cursor.execute("SELECT titulo, user_id FROM livros WHERE id = ?", (id,))
            livro_dados = cursor.fetchone()
            
            #Uptade no banco para guardar o usuário que pegou emprestado e a data da operação
            cursor.execute(
                """
                UPDATE livros
                SET disponivel = 0,
                    usuario_emprestimo = ?,
                    data_emprestimo = ?
                WHERE id = ?
                """,
                (usuario_emprestimo, data_emprestimo, id)
            )
            
            
            if livro_dados:
                titulo = livro_dados[0]   
                user_id = livro_dados[1]  
                
                #Cálculo da data
                data_inicio = datetime.strptime(data_emprestimo, "%Y-%m-%d %H:%M:%S")
                data_fim = data_inicio + timedelta(days=7)
                
                data_inicio_pt = data_inicio.strftime("%d/%m/%Y às %H:%M")
                data_fim_pt = data_fim.strftime("%d/%m/%Y às %H:%M")
                
                msg_repo = MensagemRepository()
                
                msg_aviso = (
                    f"📖 Seu livro '{titulo}' foi pego emprestado às {data_inicio_pt}. "
                    f"O prazo limite é de 7 dias e ele será devolvido no máximo até o dia {data_fim_pt}."
                )
                
                # Manda a mensagem para o dono
                msg_repo.criar_mensagem(user_id, msg_aviso, conexao)
            
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
                SELECT id, data_emprestimo, user_id, usuario_emprestimo, titulo
                FROM livros
                WHERE disponivel = 0
            """)
            livros = cursor.fetchall()

            livros_atualizados = 0
            msg_repo = MensagemRepository()

            for livro_id, data_emprestimo, user_id, usuario_emprestimo, titulo in livros:
                if not data_emprestimo:
                    continue

                data = datetime.strptime(data_emprestimo, "%Y-%m-%d %H:%M:%S")
                
                # Se o prazo de 7 dias estourou
                if datetime.now() > data + timedelta(days=7):
                    # Devolve o livro no banco
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
                    
                    
                    #Mensagens de aviso para o Dono(user_id) e para o Locatário(usuario_emprestimo)
                    
                    msg_dono = f"📢 O prazo de empréstimo do livro '{titulo}' acabou. Ele já está disponível para empréstimos novamente!"
                    msg_locatario = f"⚠️ O prazo de 7 dias para o livro '{titulo}' expirou. Ele foi devolvido automaticamente ao dono."
                    
                    msg_repo.criar_mensagem(user_id, msg_dono, conexao)
                    msg_repo.criar_mensagem(usuario_emprestimo, msg_locatario, conexao)

                    livros_atualizados += 1

            conexao.commit()
            return livros_atualizados
        finally:
            cursor.close()
            conexao.close()

    def buscar_historico_emprestimos(self, user_id):
    
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            # Busca os livros, onde o usuario_emprestimo(usuário "atual") é o usuário logado
            cursor.execute(
                """
                SELECT titulo, data_emprestimo 
                FROM livros 
                WHERE usuario_emprestimo = ?
                """, 
                (user_id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()