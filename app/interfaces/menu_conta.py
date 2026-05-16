from colorama import Fore

from .exibir_usuario import ExibirUsuario
from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from .exibir_livros import ExibirLivros
from .devolver_livros import DevolverLivro
from .menu_editar import MenuEditar
from .deletar_conta import MenuDeletar

class MenuConta:
    def __init__(self):
        self.exibir_livros = ExibirLivros()
        self.devolver_livro = DevolverLivro()
        self.menu_editar = MenuEditar()
        self.deletar_conta = MenuDeletar()
        self.exibir_usuario = ExibirUsuario()
        self.validador = Validador()

    def exibir(self, usuario):
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
            
            print(Fore.LIGHTMAGENTA_EX + "\n[1]" + Fore.WHITE + " Meus Livros")
            print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Devolver Livro")
            print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Editar")
            print(Fore.LIGHTMAGENTA_EX + "[4]" + Fore.WHITE + " Deletar")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Voltar")
            print(Fore.CYAN + "-"*60)

            opcao = self.validador.validar_opcao(0, 4)

            if opcao == 1:
                self.exibir_livros.exibir(usuario)
            elif opcao == 2:           
                self.devolver_livro.devolver_livros(usuario)
            elif opcao == 3:              
                self.menu_editar.exibir(usuario)
            elif opcao == 4:               
                if self.deletar_conta.deletar_conta(usuario):
                    return
            elif opcao == 0:
                return
            else:
                print(Fore.RED + "❌ Opção inválida. Tente novamente.")
                self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
