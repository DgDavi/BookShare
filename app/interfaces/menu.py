from colorama import Fore

from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from services.user_services import UserService
from interfaces.menu_de_usuario import MenuUsuario
from .info_menu import InfoMenu

class MenuInicial:
    def __init__(self, user_serivice: UserService, menu_user: MenuUsuario, menu_info: InfoMenu, validador: Validador):
        self.user_service = user_serivice
        self.menu_user = menu_user
        self.menu_info = menu_info
        self.validador = validador

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

            print()
            print(Fore.LIGHTMAGENTA_EX + "[1]" + Fore.WHITE + " Cadastrar usuário")
            print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Login")
            print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Sobre o projeto")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Sair")

            print(Fore.CYAN + "-"*60)

            try:
                opcao = int(self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Escolha uma opção: "))
            except ValueError:
                print(Fore.RED + "❌ Digite apenas números de opções válidas!")
                opcao = None

            # Chama a função de cadastro de usuário
            if opcao == 1:
                usuario = self.user_service.cadastrar_usuario()
                if usuario:
                    self.menu_user.exibir(usuario)

            # Chama a função de login de usuário
            elif opcao == 2:
                usuario = self.user_service.login_usuario()
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
