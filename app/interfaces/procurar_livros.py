from colorama import Fore

from .exibir_livros import ExibirLivros
from services.livro_services import LivroService
from utils.validador import Validador
from utils.limpar_tela import limpar_tela

class ProcurarLivro:
    def __init__(self):
        self.validador = Validador()
        self.livro_service = LivroService()
        self.exibir_livros = ExibirLivros()

    def procurar_livros(self, usuario):
        """
        Exibe a tela de busca e apresenta os livros encontrados.

        Args:
            usuario (Usuario): Usuário autenticado que está pesquisando livros.

        Returns:
            None: Fluxo de interface com entrada e saída pelo terminal.
        """
        limpar_tela()
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "🔎 PROCURAR LIVRO".center(60))
        print(Fore.CYAN + "=" * 60)
        print()

        livro_procurado = self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite o nome ou autor do livro que está procurando: ")

        livros = self.livro_service.buscar_livros_por_termo(livro_procurado)

        limpar_tela()

        self.exibir_livros.exibir_livros_procurado(livros, usuario)

        self.validador.input_com_prompt_colorido(Fore.YELLOW + "\n👉 Pressione Enter para continuar...")
        return
