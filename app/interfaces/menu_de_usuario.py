from colorama import Fore

from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from .procurar_livros import ProcurarLivro
from .menu_conta import MenuConta
from services.livro_services import LivroService
from .menu_livro_cadastro import CadastroLivro
from .caixa_entrada import CaixaEntrada
from .historico_emprestimos import HistoricoEmprestimos

class MenuUsuario:
    def __init__(self):
        self.livro_service = LivroService()
        self.menu_conta = MenuConta()
        self.procurar_livro = ProcurarLivro()
        self.validador = Validador()
        self.cadastro_livro = CadastroLivro()
        self.caixa_entrada = CaixaEntrada()
        self.historico = HistoricoEmprestimos()

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
            print(Fore.LIGHTMAGENTA_EX + "[4]" + Fore.WHITE + " Caixa de Entrada")
            print(Fore.LIGHTMAGENTA_EX + "[5]" + Fore.WHITE + " Histórico de Empréstimos")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Logout")

            print(Fore.CYAN + "-"*60)


            opcao = self.validador.validar_opcao(0, 5)


            if opcao == 1:
                if self.menu_conta.exibir(usuario):
                    return True
            elif opcao == 2:
                self.cadastro_livro.exibir(usuario)
            elif opcao == 3:        
                self.procurar_livro.procurar_livros(usuario)
            elif opcao == 4:
                self.caixa_entrada.exibir(usuario)
            elif opcao == 5:
                self.historico.exibir(usuario)
            elif opcao == 0:
                limpar_tela()
                return
            else:
                print(Fore.RED + "❌ Opção inválida. Tente novamente.")
                self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
