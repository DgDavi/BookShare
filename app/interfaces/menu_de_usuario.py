from colorama import Fore

from utils.limpar_tela import limpar_tela
from utils.validador import input_com_prompt_colorido

from interfaces.menu_conta import menu_conta
from services.livro_services import cadastrar_livro

# Menu do usuário logado
def menu_usuario(usuario):
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

        print()
        print(Fore.LIGHTMAGENTA_EX + "[1]" + Fore.WHITE + " Conta")
        print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Cadastrar Livro")
        print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Procurar Livro")
        print(Fore.LIGHTMAGENTA_EX + "[4]" + Fore.WHITE + " Cartão de Crédito")
        print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Logout")

        print(Fore.CYAN + "-"*60)


        try:
            opcao = int(input_com_prompt_colorido(Fore.GREEN + "👉 Escolha uma opção: "))
        except ValueError:
            print(Fore.RED + "❌ Digite apenas números de opções válidas!")
            opcao = None


        if opcao == 1:
            menu_conta(usuario)
        elif opcao == 2:
            cadastrar_livro(usuario)
        elif opcao == 3:
            from interfaces.procurar_livros import procurar_livros
            procurar_livros(usuario)
        elif opcao == 4:
            print("A fazer")
            input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
        elif opcao == 0:
            limpar_tela()
            return
        else:
            print(Fore.RED + "❌ Opção inválida. Tente novamente.")
            input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
