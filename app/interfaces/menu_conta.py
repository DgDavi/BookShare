from colorama import Fore

from data.db import get_db_connection
from .exibir_usuario import exibir_usuario
from utils.limpar_tela import limpar_tela
from utils.validador import input_com_prompt_colorido


def menu_conta(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        while True:
            limpar_tela()

            exibir_usuario(usuario)
            print(Fore.CYAN + "-"*60)
            print()
            print(Fore.LIGHTMAGENTA_EX + "[1]" + Fore.WHITE + " Meus Livros")
            print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Editar")
            print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Deletar")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Voltar")
            print(Fore.CYAN + "-"*60)

            try:
                opcao = int(input_com_prompt_colorido(Fore.GREEN + "👉 Escolha uma opção: "))
            except ValueError:
                print(Fore.RED + "❌ Digite apenas números de opções válidas!")
                opcao = None

            if opcao == 1:
                from .exibir_livros import exibir_livros
                exibir_livros(usuario)
            elif opcao == 2:
                from .menu_editar import menu_editar
                menu_editar(usuario)
            elif opcao == 3:
                from .deletar_conta import deletar_conta
                if deletar_conta(usuario):
                    return
            elif opcao == 0:
                return
            else:
                print(Fore.RED + "❌ Opção inválida. Tente novamente.")
                input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
    finally:
        cursor.close()
        conexao.close()
