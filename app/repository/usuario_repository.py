from data.db import get_db_connection

class UserRepository:

    def criar_usuario(self, usuario):
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
        """Retorna a senha hashed do usuário a partir do id."""
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
        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario.id,))
        conexao.commit()
        cursor.close()
        conexao.close()
        return True


    def editar_email(self, usuario, email):
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
        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,))
        usuario_login = cursor.fetchone()

        if usuario_login:
            return usuario_login
        return None

    def email_existe(self, email):
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
            return cursor.fetchone()[0] == 1
        finally:
            cursor.close()
            conexao.close()

    def buscar_por_email(self, email):
        return self.logar_usuario(email)
    