from datetime import datetime, timedelta

from data.db import get_db_connection

from repository.mensagem_repository import MensagemRepository

class LivroRepository:
    def criar_livro(self, livro):
        """Insere um novo livro no banco."""
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
        """Lista os livros cadastrados por um usuário."""
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
        """Atualiza o título de um livro."""
        cursor.execute(
            "UPDATE livros SET titulo = ? WHERE id = ?",
            (titulo, livro.id)
        )
        livro.titulo = titulo

        cursor.execute("SELECT titulo FROM livros WHERE id = ?", (livro.id,))
        resultado = cursor.fetchone()
        return resultado is not None and resultado[0] == livro.titulo
    

    def editar_descricao(self, livro, descricao, cursor):
        """Atualiza a descrição de um livro."""
        cursor.execute(
            "UPDATE livros SET descricao = ? WHERE id = ?",
            (descricao, livro.id)
        )
        livro.descricao = descricao

        cursor.execute("SELECT descricao FROM livros WHERE id = ?", (livro.id,))
        resultado = cursor.fetchone()
        return resultado is not None and resultado[0] == livro.descricao
    

    def deletar_livro(self, livro, cursor):
        """Remove um livro do banco."""
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro.id,))
        return True
    

    def buscar_livros(self, termo, limite, offset):
        """Busca livros por título ou autor com limite e offset."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            termo_busca = f"%{termo}%"
            cursor.execute(
                "SELECT id, user_id, titulo, descricao, autor, disponivel, usuario_emprestimo, data_emprestimo "
                "FROM livros WHERE LOWER(TRIM(titulo)) LIKE ? OR LOWER(TRIM(autor)) LIKE ? "
                "LIMIT ? OFFSET ?",
                (termo_busca, termo_busca, limite, offset)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    def contar_livros(self, termo):
        """Conta os livros que batem com o termo informado."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            termo_busca = f"%{termo}%"

            cursor.execute("""
                SELECT COUNT(*)
                FROM livros 
                WHERE LOWER(TRIM(titulo)) LIKE ? OR LOWER(TRIM(autor)) LIKE ?""",
                (termo_busca, termo_busca))
            
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conexao.close()


    def buscar_livro_por_id(self, livro_id):
        """Busca um livro pelo identificador."""
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
        """Lista os livros emprestados para um usuário."""
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
        """Verifica se o usuário já possui um empréstimo ativo."""
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


    def usuario_ja_esta_na_fila(self, livro_id, usuario_id):
        """Verifica se um usuário já entrou na fila de um livro."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT 1 FROM fila_emprestimos WHERE livro_id = ? AND user_id = ?",
                (livro_id, usuario_id)
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conexao.close()


    def posicao_na_fila(self, livro_id, usuario_id):
        """Retorna a posição do usuário na fila de um livro."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT user_id FROM fila_emprestimos WHERE livro_id = ? ORDER BY data_solicitacao ASC, id ASC",
                (livro_id,)
            )
            for posicao, fila in enumerate(cursor.fetchall(), start=1):
                if fila[0] == usuario_id:
                    return posicao
            return None
        finally:
            cursor.close()
            conexao.close()


    def adicionar_usuario_na_fila(self, livro_id, usuario_id):
        """Inclui um usuário na fila de empréstimo de um livro."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT OR IGNORE INTO fila_emprestimos (livro_id, user_id, data_solicitacao) VALUES (?, ?, ?)",
                (livro_id, usuario_id, data_atual)
            )
            conexao.commit()
            posicao = self.posicao_na_fila(livro_id, usuario_id)

            cursor.execute(
                "SELECT titulo, user_id FROM livros WHERE id = ?",
                (livro_id,)
            )
            livro = cursor.fetchone()
            if livro:
                titulo = livro[0]
                dono_id = livro[1]
                if dono_id != usuario_id:
                    msg_repo = MensagemRepository()
                    mensagem = f"📥 Um usuário entrou na fila de empréstimo do seu livro '{titulo}'. Posição na fila: {posicao}."
                    msg_repo.criar_mensagem(dono_id, mensagem, conexao)

            return posicao
        finally:
            cursor.close()
            conexao.close()


    def _promover_proximo_da_fila(self, livro_id, cursor, conexao):
        """Reserva o livro para a próxima pessoa da fila."""
        cursor.execute(
            "SELECT titulo FROM livros WHERE id = ?",
            (livro_id,)
        )
        livro = cursor.fetchone()
        if not livro:
            return False

        cursor.execute(
            """
            SELECT id, user_id
            FROM fila_emprestimos
            WHERE livro_id = ?
            ORDER BY data_solicitacao ASC, id ASC
            LIMIT 1
            """,
            (livro_id,)
        )
        proximo = cursor.fetchone()
        if not proximo:
            return False

        fila_id, usuario_id = proximo[0], proximo[1]
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            UPDATE livros
            SET disponivel = 0,
                usuario_emprestimo = ?,
                data_emprestimo = ?
            WHERE id = ?
            """,
            (usuario_id, data_atual, livro_id)
        )
        cursor.execute(
            "DELETE FROM fila_emprestimos WHERE id = ?",
            (fila_id,)
        )

        msg_repo = MensagemRepository()
        msg_repo.criar_mensagem(
            usuario_id,
            f"📚 O livro '{livro[0]}' ficou disponível e foi reservado para você pela fila de empréstimo.",
            conexao
        )
        return True



    def emprestar_livro_repo(self, id, usuario_emprestimo, data_emprestimo):
        """Atualiza o livro para marcar o empréstimo e inicia o histórico."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("SELECT titulo, user_id FROM livros WHERE id = ?", (id,))
            livro_dados = cursor.fetchone()
            
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
            
            # REGISTRO DE HISTÓRICO: Insere um novo registro na tabela de histórico, salvando qual livro foi pego, por quem e o momento exato do empréstimo
            cursor.execute(
                """
                INSERT INTO historico_emprestimos (livro_id, usuario_id, data_emprestimo)
                VALUES (?, ?, ?)
                """,
                (id, usuario_emprestimo, data_emprestimo)
            )
            # ---------------------------------------------------------------------------
            
            if livro_dados:
                titulo = livro_dados[0]   
                user_id = livro_dados[1]  
                
                data_inicio = datetime.strptime(data_emprestimo, "%Y-%m-%d %H:%M:%S")
                data_fim = data_inicio + timedelta(days=7)
                
                data_inicio_pt = data_inicio.strftime("%d/%m/%Y às %H:%M")
                data_fim_pt = data_fim.strftime("%d/%m/%Y às %H:%M")
                
                msg_repo = MensagemRepository()
                
                msg_aviso = (
                    f"📖 Seu livro '{titulo}' foi pego emprestado às {data_inicio_pt}. "
                    f"O prazo limite é de 7 dias e ele será devolvido no máximo até o dia {data_fim_pt}."
                )
                
                msg_repo.criar_mensagem(user_id, msg_aviso, conexao)
            
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()


    def devolver_livro_repo(self, livro_id):
        """Atualiza o livro para marcar a devolução e registra no histórico."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT titulo, user_id, usuario_emprestimo FROM livros WHERE id = ?",
                (livro_id,)
            )
            livro_info = cursor.fetchone()

            #Atualiza a tabela de livros 
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

           
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                UPDATE historico_emprestimos 
                SET data_devolucao = ? 
                WHERE livro_id = ? AND data_devolucao IS NULL
                """,
                (data_atual, livro_id)
            )
           

            if livro_info:
                titulo = livro_info[0]
                dono_id = livro_info[1]
                usuario_devolveu = livro_info[2]

                nome_devolvedor = None
                if usuario_devolveu:
                    cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario_devolveu,))
                    linha = cursor.fetchone()
                    if linha:
                        nome_devolvedor = linha[0]

                remetente_texto = f" pelo usuário {nome_devolvedor} (id {usuario_devolveu})" if nome_devolvedor else (f" pelo usuário id {usuario_devolveu}" if usuario_devolveu else "")
                mensagem = f"✅ O livro '{titulo}' foi devolvido{remetente_texto}."
                msg_repo = MensagemRepository()
                msg_repo.criar_mensagem(dono_id, message=mensagem, conexao=conexao) # Ajustado para passar conexao se necessário

            self._promover_proximo_da_fila(livro_id, cursor, conexao)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()
            
    
    def atualizar_status_livro(self):
        """Atualiza atrasos, suspensões e devoluções automáticas."""
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
                now = datetime.now()
                overdue_days = (now - data).days

                if overdue_days <= 0:
                    continue

                if 1 <= overdue_days <= 3:
                    aviso = f"⚠️ Seu empréstimo do livro '{titulo}' está com {overdue_days} dia(s) de atraso. Por favor devolva-o para evitar punições." 
                    msg_repo.criar_mensagem(usuario_emprestimo, aviso, conexao)
                    continue

                if 4 <= overdue_days <= 7:
                    aviso = (
                        f"🚫 Você está bloqueado de novos empréstimos até devolver o livro '{titulo}'."
                        f" Atraso atual: {overdue_days} dia(s)."
                    )
                    msg_repo.criar_mensagem(usuario_emprestimo, aviso, conexao)
                    continue

                if overdue_days > 7:
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
                    self._promover_proximo_da_fila(livro_id, cursor, conexao)

                    msg_dono = f"📢 O prazo de empréstimo do livro '{titulo}' acabou. Ele já está disponível para empréstimos novamente!"
                    msg_locatario = f"⚠️ O prazo de 7 dias para o livro '{titulo}' expirou. Ele foi devolvido automaticamente ao dono."
                    msg_repo.criar_mensagem(user_id, msg_dono, conexao)
                    msg_repo.criar_mensagem(usuario_emprestimo, msg_locatario, conexao)

                    aviso_suspensao = (
                        f"⛔ Sua conta está sendo suspensa temporariamente devido ao atraso na devolução do livro '{titulo}'."
                        " Você não poderá buscar nem pegar livros até regularizar a situação."
                    )
                    msg_repo.criar_mensagem(usuario_emprestimo, aviso_suspensao, conexao)

                    livros_atualizados += 1

            conexao.commit()
            return livros_atualizados
        finally:
            cursor.close()
            conexao.close()

    def buscar_historico_emprestimos(self, user_id):
        """Busca o histórico de empréstimos de um usuário."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
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

    def buscar_historico_completo_usuario(self, usuario_id):
        """Busca o histórico completo (ativos e devolvidos) usando a nova tabela."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
           
            # CONSULTA DE HISTÓRICO COMPLETO: Faz um JOIN entre a tabela de histórico e a tabela de livros para buscar título e autor
            # Filtra pelo ID do usuário logado e ordena do mais recente para o mais antigo.
           
            cursor.execute(
                """
                SELECT l.titulo, l.autor, h.data_emprestimo, h.data_devolucao
                FROM historico_emprestimos h
                JOIN livros l ON h.livro_id = l.id
                WHERE h.usuario_id = ?
                ORDER BY h.data_emprestimo DESC
                """,
                (usuario_id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
