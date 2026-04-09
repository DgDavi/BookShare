from colorama import Fore

from utils.limpar_tela import limpar_tela
from services.user_services import cadastrar_usuario, login_usuario
from interfaces.menu_de_usuario import menu_usuario


def menu_inical():
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
            opcao = int(input(Fore.YELLOW + "👉 Escolha uma opção: "))
        except ValueError:
            print(Fore.RED + "❌ Digite apenas números de opções válidas!")
            opcao = None

        # Chama a função de cadastro de usuário
        if opcao == 1:
            usuario = cadastrar_usuario()
            if usuario:
                menu_usuario(usuario)

        # Chama a função de login de usuário
        elif opcao == 2:
            usuario = login_usuario()
            if usuario:
                menu_usuario(usuario)

        # Chama a função de informações sobre o projeto
        elif opcao == 3:
            from .info_menu import info_menu
            info_menu()

        # Fecha a aplicação
        elif opcao == 0:
            print("Saindo do aplicativo...")
            limpar_tela()
            exit()

        else:
            print(Fore.RED + "n\❌ Opção inválida. Tente novamente.")
            input(Fore.YELLOW + "👉 Pressione Enter para continuar...")

