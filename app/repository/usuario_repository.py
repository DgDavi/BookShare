class UserRepository:

    def criar_usuario(self, usuario, cursor):
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", 
                    (usuario.nome, usuario.email, usuario.senha_hashed))
        
        usuario.id = cursor.lastrowid

        return usuario
        

    def buscar_dados_usuario(self, usuario, cursor):
        cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ?", (usuario.email,))
        dados_usuario = cursor.fetchone()
        return dados_usuario


    def obter_senha(self, usuario, cursor):
        """
        Retorna a senha hashed do usuário a partir do id.
        """
        cursor.execute("SELECT senha FROM usuarios WHERE id = ?", (usuario.id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None


    def deletar_usuario(self, usuario, cursor):
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario.id,))
        return True


    def editar_email(self, usuario, email, cursor):
        cursor.execute("UPDATE usuarios SET email = ? WHERE id = ?", (email, usuario.id))
        usuario.email = email
        
        cursor.execute("SELECT email FROM usuarios WHERE id = ?", (usuario.id,))
        resultado = cursor.fetchone()

        if resultado is None:
            return False
        
        novo_email = resultado[0]
        return novo_email == usuario.email


    def editar_nome(self, usuario, nome, cursor):
        cursor.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (nome, usuario.id))
        usuario.nome = nome

        cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario.id,))
        resultado = cursor.fetchone()

        if resultado is None:
            return False
        
        novo_nome = resultado[0]
        return novo_nome == usuario.nome


    def editar_senha(self, usuario, senha, cursor):
        cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (senha, usuario.id))
        usuario.senha_hashed = senha

        cursor.execute("SELECT senha FROM usuarios WHERE id = ?", (usuario.id,))
        resultado = cursor.fetchone()

        if resultado is None:
            return False
        
        nova_senha = resultado[0]
        return nova_senha == usuario.senha_hashed
    