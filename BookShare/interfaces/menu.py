from utils.limpar_tela import limpar_tela
from colorama import Fore
from services.auth_services import cadastrar_usuario, login_usuario


def menu_inical():
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
        opcao = int(input(Fore.GREEN + "👉 Escolha uma opção: "))
    except ValueError:
        print(Fore.RED + "❌ Digite apenas números de opções válidas!")
        opcao = None

    # Chama a função de cadastro de usuário
    if opcao == 1:
        cadastrar_usuario()

    # Chama a função de login de usuário
    elif opcao == 2:
        login_usuario()

    elif opcao == 3:
        print("A fazer")

    # Fecha a aplicação
    elif opcao == 0:
        print("Saindo do aplicativo...")
        limpar_tela()
        exit()

    else:
        print(Fore.RED + "❌ Opção inválida. Tente novamente.")
        menu_inical()


def menu_usuario():
    limpar_tela()

    print(Fore.CYAN + "="*60)
    print(Fore.CYAN + "📚 MENU DO USUÁRIO".center(60))
    print(Fore.CYAN + "="*60)

    print()
    print(Fore.LIGHTMAGENTA_EX + "[1]" + Fore.WHITE + " Conta")
    print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Cadastrar Livro")
    print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Procurar Livro")
    print(Fore.LIGHTMAGENTA_EX + "[4]" + Fore.WHITE + " Cartão de Crédito")
    print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Sair")

    print(Fore.CYAN + "-"*60)


    try:
        opcao = int(input(Fore.GREEN + "👉 Escolha uma opção: "))
    except ValueError:
        print(Fore.RED + "❌ Digite apenas números de opções válidas!")
        opcao = None


    if opcao == 1:
        print("A fazer")

    elif opcao == 2:
        print("A fazer")
    
    elif opcao == 3:
        print("A fazer")

    elif opcao == 4:
        print("A fazer")
    
    elif opcao == 0:
        print("Saindo do aplicativo...")
        limpar_tela()
        exit()