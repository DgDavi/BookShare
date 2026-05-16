from colorama import Fore
from datetime import datetime, timedelta

from utils.validador import Validador
from model.livro import Livro
from utils.limpar_tela import limpar_tela
from repository.livro_repository import LivroRepository

class LivroService:
    def __init__(self, livro_repo: LivroRepository, validador: Validador):
        self.livro_repo = livro_repo
        self.validador = validador

    def cadastrar_livro(self,nome, descricao, autor, usuario):
        """
        Coleta os dados de um livro no terminal e salva no banco.

        Args:
            usuario (Usuario): Usuário dono do livro que será cadastrado.

        Returns:
            Livro | None: Instância de livro criada quando o cadastro é concluído.
            Se houver falha no processo, retorna None.
        """
        livro = Livro(titulo=nome, descricao=descricao, autor=autor, user_id=usuario.id)
        livro_criado = self.livro_repo.criar_livro(livro)

        if livro_criado:
            return livro_criado
        return None


    def listar_livros_do_usuario(self, usuario):
        """
        Lista os livros cadastrados pelo usuário.

        Args:
            usuario (Usuario): Usuário dono dos livros.

        Returns:
            list[sqlite3.Row]: Lista de livros pertencentes ao usuário.
        """

        return self.livro_repo.buscar_livros_usuario(usuario)


    def listar_livros_emprestados(self, usuario):
        """
        Lista os livros atualmente emprestados para o usuário.

        Args:
            usuario (Usuario): Usuário que pegou livros emprestados.

        Returns:
            list[sqlite3.Row]: Lista de empréstimos ativos do usuário.
        """
        
        return self.livro_repo.buscar_livros_emprestados(usuario.id)


    def buscar_livros_por_termo(self, termo):
        """
        Busca livros por título ou autor com normalização de texto.

        Args:
            termo (str): Texto digitado para pesquisa.

        Returns:
            list[sqlite3.Row]: Lista de livros encontrados.
        """
        termo_normalizado = termo.strip().lower()
        return self.livro_repo.buscar_livros(termo_normalizado)


    def emprestar_livro(self, livro_id, usuario_id):
        """
        Registra o empréstimo de um livro para um usuário.

        Args:
            livro_id (int): Identificador do livro.
            usuario_id (int): Identificador do usuário que pega emprestado.

        Returns:
            None: Atualiza o banco.
        """
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.livro_repo.emprestar_livro_repo(livro_id, usuario_id, data_atual)


    def devolver_livro(self, livro_id):
        """
        Registra a devolução de um livro e libera sua disponibilidade.

        Args:
            livro_id (int): Identificador do livro.

        Returns:
            None: Atualiza o banco.
        """
        self.livro_repo.devolver_livro_repo(livro_id)


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


    def atualizar_status_livros(self):
        """
        Atualiza o status dos livros e devolve os que venceram o prazo.

        Returns:
            int: Quantidade de livros atualizados.
        """
        return self.livro_repo.atualizar_status_livro()


    def tentar_emprestar_livro(self, usuario_id, livro_id):
        """
        Valida regras de negócio e tenta efetivar o empréstimo.

        Args:
            usuario_id (int): Identificador do usuário solicitante.
            livro_id (int): Identificador do livro solicitado.

        Returns:
            tuple[bool, str]: Resultado da operação com status e mensagem.
        """
        self.atualizar_status_livros()

        livro = self.livro_repo.buscar_livro_por_id(livro_id)
        if not livro:
            return False, "❌ Livro não encontrado."

        if livro["user_id"] == usuario_id:
            return False, "❌ Você não pode pegar emprestado o próprio livro."

        if livro["disponivel"] == 0:
            return False, "❌ Livro indisponível no momento."

        if self.livro_repo.usuario_tem_emprestimo_ativo(usuario_id):
            return False, "❌ Você já possui um empréstimo ativo."

        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.livro_repo.emprestar_livro_repo(livro_id, usuario_id, data_atual)

        return True, "✅ Empréstimo realizado por 7 dias."


    def tentar_devolver_livro(self, usuario_id, livro_id):
        """
        Valida posse do empréstimo e tenta efetivar a devolução.

        Args:
            usuario_id (int): Identificador do usuário que devolve.
            livro_id (int): Identificador do livro a devolver.

        Returns:
            tuple[bool, str]: Resultado da operação com status e mensagem.
        """


        livro = self.livro_repo.buscar_livro_por_id(livro_id)
        if not livro:
            return False, "❌ Livro não encontrado."

        if livro["usuario_emprestimo"] != usuario_id:
            return False, "❌ Esse livro não está emprestado para você."

        if livro["disponivel"] == 1:
            return False, "❌ Esse livro já está disponível."

        self.livro_repo.devolver_livro_repo(livro_id)

        return True, "✅ Livro devolvido com sucesso."
