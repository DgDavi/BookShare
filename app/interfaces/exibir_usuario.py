from colorama import Fore

from services.user_services import obter_dados_usuario

def exibir_usuario(usuario):
    dados_usuario = obter_dados_usuario(usuario)

    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "📋 DADOS DO USUÁRIO".center(60))
    print(Fore.CYAN + "=" * 60)

    if dados_usuario:
        print(Fore.LIGHTMAGENTA_EX + "Id: " + Fore.WHITE + f"{dados_usuario[0]}")
        print(Fore.LIGHTMAGENTA_EX + "Nome: " + Fore.WHITE + f"{dados_usuario[1]}")
        print(Fore.LIGHTMAGENTA_EX + "Email: " + Fore.WHITE + f"{dados_usuario[2]}")

    return True