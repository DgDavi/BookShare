from colorama import Fore

from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from services.livro_services import LivroService

class CadastroLivro:
    def __init__(self):
        self.livro_service = LivroService()
        self.validador = Validador()

    def exibir(self, usuario):
        limpar_tela()
        print(Fore.YELLOW + "📋 CADASTRO DE LIVROS\n" + Fore.CYAN + "-"*30 + "\n")

        titulo = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite o nome do livro: ",
            lambda n: 3 <= len(n) <= 40,
            Fore.YELLOW + "👉 O nome deve conter entre 3 e 40 caracteres."
        )
        if titulo is None:
            print(Fore.YELLOW + "Operação cancelada pelo usuário.")
            return None

        descricao = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite a descrição do livro: ",
            lambda n:3 <= len(n) <= 200,
            Fore.YELLOW + "👉 A descrição deve conter entre 3 e 200 caracteres."
        )
        if descricao is None:
            print(Fore.YELLOW + "Operação cancelada pelo usuário.")
            return None

        autor = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite o autor do livro: ",
            lambda n: 3 <= len(n) <= 40,
            Fore.YELLOW + "👉 O nome do autor deve conter entre 3 e 40 caracteres."
        )
        if autor is None:
            print(Fore.YELLOW + "Operação cancelada pelo usuário.")
            return None

        livro = self.livro_service.cadastrar_livro(titulo, descricao, autor, usuario)

        if livro:
            self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
            return livro
        
        return None