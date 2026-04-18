from colorama import Fore

from data.db import get_db_connection
from repository.usuario_repository import buscar_dados_usuario

def exibir_usuario(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    dados_usuario = buscar_dados_usuario(usuario, cursor)
    cursor.close()
    conexao.close()

    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "📋 DADOS DO USUÁRIO".center(60))
    print(Fore.CYAN + "=" * 60)

    if dados_usuario:
        print(Fore.LIGHTMAGENTA_EX + "Id: " + Fore.WHITE + f"{dados_usuario[0]}")
        print(Fore.LIGHTMAGENTA_EX + "Nome: " + Fore.WHITE + f"{dados_usuario[1]}")
        print(Fore.LIGHTMAGENTA_EX + "Email: " + Fore.WHITE + f"{dados_usuario[2]}")

    return True