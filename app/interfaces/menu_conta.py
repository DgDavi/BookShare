from colorama import Fore

from .exibir_usuario import ExibirUsuario
from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from .exibir_livros import ExibirLivros
from .devolver_livros import DevolverLivro
from .menu_editar import MenuEditar
from .deletar_conta import MenuDeletar

class MenuConta:
    def __init__(self, exibir_livros: ExibirLivros, devolver_livro: DevolverLivro, menu_editar: MenuEditar, deletar_contar: MenuDeletar, exibir_usuario: ExibirUsuario, validador: Validador):
        self.exibir_livros = exibir_livros
        self.devolver_livro = devolver_livro
        self.menu_editar = menu_editar
        self.deletar_conta = deletar_contar
        self.exibir_usuario = exibir_usuario
        self.validador = validador

    def menu_conta(self, usuario):
        """
        Exibe opções de conta do usuário e ações relacionadas aos livros.

        Args:
            usuario (Usuario): Usuário autenticado no sistema.

        Returns:
            None: Loop de navegação da área de conta.
        """

        while True:
            limpar_tela()

            self.exibir_usuario.exibir_usuario(usuario)
            print(Fore.CYAN + "-"*60)
            print()
            print(Fore.LIGHTMAGENTA_EX + "[1]" + Fore.WHITE + " Meus Livros")
            print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Devolver Livro")
            print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Editar")
            print(Fore.LIGHTMAGENTA_EX + "[4]" + Fore.WHITE + " Deletar")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Voltar")
            print(Fore.CYAN + "-"*60)

            try:
                opcao = int(self.validador.input_com_prompt_colorido(Fore.GREEN + "👉 Escolha uma opção: "))
            except ValueError:
                print(Fore.RED + "❌ Digite apenas números de opções válidas!")
                opcao = None

            if opcao == 1:
                self.exibir_livros.exibir_livros(usuario)
            elif opcao == 2:           
                self.devolver_livro.devolver_livros(usuario)
            elif opcao == 3:              
                self.menu_editar.menu_editar(usuario)
            elif opcao == 4:               
                if self.deletar_conta.deletar_conta(usuario):
                    return
            elif opcao == 0:
                return
            else:
                print(Fore.RED + "❌ Opção inválida. Tente novamente.")
                self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
