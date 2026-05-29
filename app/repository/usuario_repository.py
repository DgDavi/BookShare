from data.db import get_db_connection
from datetime import datetime, timedelta

class UserRepository:

    def criar_usuario(self, usuario):
        """Insere um novo usuário no banco."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", 
                    (usuario.nome, usuario.email, usuario.senha_hashed))
        last_id = cursor.lastrowid
        conexao.commit()
        cursor.close()
        conexao.close()

        usuario.id = last_id
        return last_id
        

    def buscar_dados_usuario(self, usuario):
                """Busca os dados básicos de um usuário pelo email."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ?", (usuario.email,))
            dados_usuario = cursor.fetchone()
            return dados_usuario
        finally:
            cursor.close()
            conexao.close()


    def obter_senha(self, usuario):
        """Retorna a senha hash de um usuário."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("SELECT senha FROM usuarios WHERE id = ?", (usuario.id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        finally:
            cursor.close()
            conexao.close()


    def deletar_usuario(self, usuario):
        """Remove um usuário do banco."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario.id,))
        conexao.commit()
        cursor.close()
        conexao.close()
        return True


    def editar_email(self, usuario, email):
        """Atualiza o email de um usuário."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute("UPDATE usuarios SET email = ? WHERE id = ?", (email, usuario.id))
        conexao.commit()
        usuario.email = email
        
        cursor.execute("SELECT email FROM usuarios WHERE id = ?", (usuario.id,))
        resultado = cursor.fetchone()

        try:
            if resultado is None:
                return False
            
            novo_email = resultado[0]
            return novo_email == usuario.email
        finally:
            cursor.close()
            conexao.close()


    def editar_nome(self, usuario, nome):
        """Atualiza o nome de um usuário."""
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (nome, usuario.id))
        conexao.commit()
        usuario.nome = nome

        cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario.id,))
        resultado = cursor.fetchone()

        try:
            if resultado is None:
                return False
            
            novo_nome = resultado[0]
            return novo_nome == usuario.nome
        finally:
            cursor.close()
            conexao.close()


    def editar_senha(self, usuario, senha):
        """Atualiza a senha de um usuário."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (senha, usuario.id))
            usuario.senha_hashed = senha

            cursor.execute("SELECT senha FROM usuarios WHERE id = ?", (usuario.id,))
            resultado = cursor.fetchone()

            if resultado is None:
                return False

            nova_senha = resultado[0]
            conexao.commit()
            return nova_senha == usuario.senha_hashed
        finally:
            cursor.close()
            conexao.close()
    
    
    def logar_usuario(self, email):
        """Busca um usuário para autenticação pelo email."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,))
        usuario_login = cursor.fetchone()

        if usuario_login:
            return usuario_login
        return None

    def email_existe(self, email):
        """Verifica se um email já está cadastrado."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
            return cursor.fetchone()[0] == 1
        finally:
            cursor.close()
            conexao.close()

    def buscar_por_email(self, email):
        """Retorna o usuário cadastrado para um email."""
        return self.logar_usuario(email)

    def obter_status_por_id(self, usuario_id):
        """Calcula bloqueio e suspensão do usuário pelos empréstimos ativos."""
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT data_emprestimo FROM livros WHERE usuario_emprestimo = ? AND disponivel = 0",
                (usuario_id,)
            )
            rows = cursor.fetchall()

            bloqueado = 0
            suspenso_ate = None
            now = datetime.now()

            for (data_emprestimo,) in rows:
                if not data_emprestimo:
                    continue
                try:
                    d = datetime.strptime(data_emprestimo, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    continue
                overdue_days = (now - d).days
                if overdue_days > 7:
                    suspenso_ate = (now + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                    break
                if 4 <= overdue_days <= 7:
                    bloqueado = 1

            return {"bloqueado_atraso": bloqueado, "suspenso_ate": suspenso_ate}
        finally:
            cursor.close()
            conexao.close()
    