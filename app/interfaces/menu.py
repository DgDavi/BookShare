from colorama import Fore

from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from interfaces.menu_register import Register
from interfaces.menu_login import Login
from interfaces.menu_de_usuario import MenuUsuario
from .info_menu import InfoMenu

class MenuInicial:
    def __init__(self):
        self.menu_register = Register()
        self.menu_user = MenuUsuario()
        self.menu_info = InfoMenu()
        self.validador = Validador()
        self.menu_login = Login()

    def exibir(self):
        """
        Exibe o menu inicial e direciona o fluxo principal da aplicação.

        Returns:
            None: Fluxo contínuo de interface até o usuário sair da aplicação.
        """
        while True:
            limpar_tela()

            print(Fore.CYAN + "="*60)
            print(Fore.CYAN + "📚 BEM-VINDO AO BOOKSHARE".center(60))
            print(Fore.CYAN + "="*60)

            print(Fore.LIGHTMAGENTA_EX + "\n[1]" + Fore.WHITE + "Cadastrar usuário")
            print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Login")
            print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Sobre o projeto")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Sair")

            print(Fore.CYAN + "-"*60)

            opcao = self.validador.validar_opcao(Fore.GREEN + "👉 Escolha uma opção: ", 0, 3)

            # Chama a função de cadastro de usuário
            if opcao == 1:
                usuario = self.menu_register.exibir()
                if usuario:
                    self.menu_user.exibir(usuario)

            # Chama a função de login de usuário
            elif opcao == 2:
                usuario = self.menu_login.exibir()
                if usuario:
                    self.menu_user.exibir(usuario)

            # Chama a função de informações sobre o projeto
            elif opcao == 3:
                self.menu_info.exibir()

            # Fecha a aplicação
            elif opcao == 0:
                print("Saindo do aplicativo...")
                limpar_tela()
                exit()

            else:
                print(Fore.RED + "\n❌ Opção inválida. Tente novamente.")
                self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
