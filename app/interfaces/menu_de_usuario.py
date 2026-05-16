from colorama import Fore

from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from interfaces.procurar_livros import ProcurarLivro
from interfaces.menu_conta import MenuConta
from services.livro_services import LivroService
from interfaces.menu_livro_cadastro import CadastroLivro

class MenuUsuario:
    def __init__(self, livro_service: LivroService, menu_conta: MenuConta, procurar_livro: ProcurarLivro, validador: Validador, cadastro_livro: CadastroLivro):
        self.livro_service = livro_service
        self.menu_conta = menu_conta
        self.procurar_livro = procurar_livro
        self.validador = validador
        self.cadastro_livro = cadastro_livro

    # Menu do usuário logado
    def exibir(self, usuario):
        """
        Exibe o menu principal do usuário autenticado.

        Args:
            usuario (Usuario): Usuário logado no sistema.

        Returns:
            None: Loop de navegação até o logout.
        """
        while True:
            limpar_tela()

            print(Fore.CYAN + "="*60)
            print(Fore.CYAN + "📚 MENU DO USUÁRIO".center(60))
            print(Fore.CYAN + "="*60)

            print(Fore.LIGHTMAGENTA_EX + "\n[1]" + Fore.WHITE + " Conta")
            print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Cadastrar Livro")
            print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Procurar Livro")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Logout")

            print(Fore.CYAN + "-"*60)


            opcao = self.validador.validar_opcao(Fore.GREEN + "👉 Escolha uma opção: ", 0, 3)


            if opcao == 1:
                self.menu_conta.exibir(usuario)
            elif opcao == 2:
                self.cadastro_livro.exibir(usuario)
            elif opcao == 3:        
                self.procurar_livro.procurar_livros(usuario)
            elif opcao == 0:
                limpar_tela()
                return
            else:
                print(Fore.RED + "❌ Opção inválida. Tente novamente.")
                self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
