from colorama import Fore

from services.user_services import UserService

class ExibirUsuario:
    def __init__(self):
        self.user_service = UserService()

    def exibir_usuario(self, usuario):
        """Exibe os dados básicos do usuário autenticado."""
        dados_usuario = self.user_service.obter_dados_usuario(usuario)

        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "📋 DADOS DO USUÁRIO".center(60))
        print(Fore.CYAN + "=" * 60)

        if dados_usuario:
            print(Fore.LIGHTMAGENTA_EX + "Id: " + Fore.WHITE + f"{dados_usuario[0]}")
            print(Fore.LIGHTMAGENTA_EX + "Nome: " + Fore.WHITE + f"{dados_usuario[1]}")
            print(Fore.LIGHTMAGENTA_EX + "Email: " + Fore.WHITE + f"{dados_usuario[2]}")

        return True
    