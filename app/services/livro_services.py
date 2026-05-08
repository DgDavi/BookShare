from colorama import Fore
from datetime import datetime, timedelta

from data.db import get_db_connection
from utils.validador import Validador
from model.livro import Livro
from utils.limpar_tela import limpar_tela
from repository.livro_repository import LivroRepository

class LivroService:
    def __init__(self, livro_repo: LivroRepository, validador: Validador):
        self.livro_repo = livro_repo
        self.validador = validador

    def cadastrar_livro(self, usuario):
        """
        Coleta os dados de um livro no terminal e salva no banco.

        Args:
            usuario (Usuario): Usuário dono do livro que será cadastrado.

        Returns:
            Livro | None: Instância de livro criada quando o cadastro é concluído.
            Se houver falha no processo, retorna None.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        limpar_tela()
        print(Fore.YELLOW + "📋 CADASTRO DE LIVROS\n" + Fore.CYAN + "-"*30)
        print()

        titulo = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite o nome do livro: ",
            lambda n: 3 <= len(n) <= 40,
            Fore.YELLOW + "👉 O nome deve conter entre 3 e 40 caracteres."
        )

        descricao = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite a descrição do livro: ",
            lambda n:3 <= len(n) <= 200,
            Fore.YELLOW + "👉 A descrição deve conter entre 3 e 200 caracteres."
        )

        autor = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite o autor do livro: ",
            lambda n: 3 <= len(n) <= 40,
            Fore.YELLOW + "👉 O nome do autor deve conter entre 3 e 40 caracteres."
        )

        livro = Livro(titulo=titulo, descricao=descricao, autor=autor, user_id=usuario.id)
        livro_criado = self.livro_repo.criar_livro(livro, cursor)

        if livro_criado:
            conexao.commit()
            cursor.close()
            conexao.close()
            return livro_criado

        cursor.close()
        conexao.close()
        return None


    def listar_livros_do_usuario(self, usuario):
        """
        Lista os livros cadastrados pelo usuário.

        Args:
            usuario (Usuario): Usuário dono dos livros.

        Returns:
            list[sqlite3.Row]: Lista de livros pertencentes ao usuário.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            return self.livro_repo.buscar_livros_usuario(usuario, cursor)
        finally:
            cursor.close()
            conexao.close()


    def listar_livros_emprestados(self, usuario):
        """
        Lista os livros atualmente emprestados para o usuário.

        Args:
            usuario (Usuario): Usuário que pegou livros emprestados.

        Returns:
            list[sqlite3.Row]: Lista de empréstimos ativos do usuário.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            return self.livro_repo.buscar_livros_emprestados(usuario.id, cursor)
        finally:
            cursor.close()
            conexao.close()


    def buscar_livros_por_termo(self, termo):
        """
        Busca livros por título ou autor com normalização de texto.

        Args:
            termo (str): Texto digitado para pesquisa.

        Returns:
            list[sqlite3.Row]: Lista de livros encontrados.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            termo_normalizado = termo.strip().lower()
            return self.livro_repo.buscar_livros(termo_normalizado, cursor)
        finally:
            cursor.close()
            conexao.close()


    def emprestar_livro(self, cursor, conexao, livro_id, usuario_id):
        """
        Registra o empréstimo de um livro para um usuário.

        Args:
            cursor (sqlite3.Cursor): Cursor da transação atual.
            conexao (sqlite3.Connection): Conexão com o banco de dados.
            livro_id (int): Identificador do livro.
            usuario_id (int): Identificador do usuário que pega emprestado.

        Returns:
            None: Atualiza o banco e confirma a transação.
        """
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.livro_repo.emprestar_livro_repo(livro_id, usuario_id, data_atual, cursor)

        conexao.commit()


    def devolver_livro(self, cursor, conexao, livro_id):
        """
        Registra a devolução de um livro e libera sua disponibilidade.

        Args:
            cursor (sqlite3.Cursor): Cursor da transação atual.
            conexao (sqlite3.Connection): Conexão com o banco de dados.
            livro_id (int): Identificador do livro.

        Returns:
            None: Atualiza o banco e confirma a transação.
        """
        self.livro_repo.devolver_livro_repo(livro_id, cursor)

        conexao.commit()


    @staticmethod
    def livro_atrasado(data_emprestimo):
        """
        Verifica se um empréstimo ultrapassou o prazo de 7 dias.

        Args:
            data_emprestimo (str | None): Data do empréstimo em formato de texto.

        Returns:
            bool: True se o prazo foi excedido, caso contrário False.
        """
        if not data_emprestimo:
            return False

        data = datetime.strptime(data_emprestimo, "%Y-%m-%d %H:%M:%S")
        limite = data + timedelta(days=7)

        return datetime.now() > limite


    def atualizar_status_livros(self, cursor, conexao):
        """
        Atualiza o status dos livros e devolve os que venceram o prazo.

        Args:
            cursor (sqlite3.Cursor): Cursor da transação atual.
            conexao (sqlite3.Connection): Conexão com o banco de dados.

        Returns:
            None: Aplica atualizações de status e confirma a transação.
        """
        cursor.execute("""
            SELECT id, data_emprestimo
            FROM livros
            WHERE disponivel = 0
        """)
        livros = cursor.fetchall()

        for livro in livros:
            livro_id = livro[0]
            data_emprestimo = livro[1]

            if data_emprestimo and self.livro_atrasado(data_emprestimo):
                self.livro_repo.devolver_livro_repo(livro_id, cursor)

        conexao.commit()


    def tentar_emprestar_livro(self, usuario_id, livro_id):
        """
        Valida regras de negócio e tenta efetivar o empréstimo.

        Args:
            usuario_id (int): Identificador do usuário solicitante.
            livro_id (int): Identificador do livro solicitado.

        Returns:
            tuple[bool, str]: Resultado da operação com status e mensagem.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            self.atualizar_status_livros(cursor, conexao)

            livro = self.livro_repo.buscar_livro_por_id(livro_id, cursor)
            if not livro:
                return False, "❌ Livro não encontrado."

            if livro["user_id"] == usuario_id:
                return False, "❌ Você não pode pegar emprestado o próprio livro."

            if livro["disponivel"] == 0:
                return False, "❌ Livro indisponível no momento."

            if self.livro_repo.usuario_tem_emprestimo_ativo(usuario_id, cursor):
                return False, "❌ Você já possui um empréstimo ativo."

            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.livro_repo.emprestar_livro_repo(livro_id, usuario_id, data_atual, cursor)
            conexao.commit()

            return True, "✅ Empréstimo realizado por 7 dias."
        finally:
            cursor.close()
            conexao.close()


    def tentar_devolver_livro(self, usuario_id, livro_id):
        """
        Valida posse do empréstimo e tenta efetivar a devolução.

        Args:
            usuario_id (int): Identificador do usuário que devolve.
            livro_id (int): Identificador do livro a devolver.

        Returns:
            tuple[bool, str]: Resultado da operação com status e mensagem.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            livro = self.livro_repo.buscar_livro_por_id(livro_id, cursor)
            if not livro:
                return False, "❌ Livro não encontrado."

            if livro["usuario_emprestimo"] != usuario_id:
                return False, "❌ Esse livro não está emprestado para você."

            if livro["disponivel"] == 1:
                return False, "❌ Esse livro já está disponível."

            self.livro_repo.devolver_livro_repo(livro_id, cursor)
            conexao.commit()

            return True, "✅ Livro devolvido com sucesso."
        finally:
            cursor.close()
            conexao.close()
