from colorama import Fore

from data.db import get_db_connection
from model.usuario import buscar_dados_usuario
from utils.limpar_tela import limpar_tela


def menu_conta(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()

    print()
    buscar_dados_usuario(usuario, cursor)
    print()
    print(Fore.LIGHTMAGENTA_EX + "[1]" + Fore.WHITE + " Editar")
    print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Deletar")
    print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Voltar")
    print()

    cursor.close()
    conexao.commit()

    try:
        opcao = int(input(Fore.GREEN + "👉 Escolha uma opção: "))
    except ValueError:
        print(Fore.RED + "❌ Digite apenas números de opções válidas!")
        opcao = None

    if opcao == 1:
        print("A fazer")
    elif opcao == 2:
        from interfaces.deletar_conta import deletar_conta
        deletar_conta(usuario)
    elif opcao == 0:
        from interfaces.menu_de_usuario import menu_usuario
        menu_usuario(usuario)    
