from colorama import Fore

from data.db import get_db_connection
from repository.usuario_repository import buscar_dados_usuario
from utils.limpar_tela import limpar_tela


def menu_conta(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        while True:
            limpar_tela()

            buscar_dados_usuario(usuario, cursor)
            print(Fore.CYAN + "-"*60)
            print()
            print(Fore.LIGHTMAGENTA_EX + "[1]" + Fore.WHITE + " Editar")
            print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Deletar")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Voltar")
            print(Fore.CYAN + "-"*60)

            try:
                opcao = int(input(Fore.GREEN + "👉 Escolha uma opção: "))
            except ValueError:
                print(Fore.RED + "❌ Digite apenas números de opções válidas!")
                opcao = None

            if opcao == 1:
                from interfaces.menu_editar import menu_editar
                menu_editar(usuario)
            elif opcao == 2:
                from interfaces.deletar_conta import deletar_conta
                if deletar_conta(usuario):
                    return
            elif opcao == 0:
                return
            else:
                print(Fore.RED + "❌ Opção inválida. Tente novamente.")
                input(Fore.YELLOW + "👉 Pressione Enter para continuar...")
    finally:
        cursor.close()
        conexao.close()
