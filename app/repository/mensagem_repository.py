from datetime import datetime
from data.db import get_db_connection

class MensagemRepository:

    def criar_mensagem(self, user_id, texto_mensagem, conexao=None):
        """
        Salva uma nova menagem para um usuário no banco de dados.
        
        """
        conexao_propria = conexao is None
        if conexao_propria:
            conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO mensagens (user_id, mensagem, data_criacao) VALUES (?, ?, ?)",
                (user_id, texto_mensagem, data_atual)
            )
            if conexao_propria:
                conexao.commit()
            return True
        finally:
            cursor.close()
            if conexao_propria:
                conexao.close()

    def buscar_mensagens_usuario(self, user_id):
        """
        Retorna todas as mensagens destinadas a um usuário específico.
        
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT id, user_id, mensagem, data_criacao FROM mensagens WHERE user_id = ? ORDER BY data_criacao DESC",
                (user_id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()