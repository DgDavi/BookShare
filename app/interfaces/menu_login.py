from colorama import Fore

from utils.limpar_tela import limpar_tela
from services.user_services import UserService
from utils.validador import Validador

class Login:
    def __init__(self, user_service: UserService, validador: Validador):
        self.user_service = user_service
        self.validador = validador

    def exibir(self):

        limpar_tela()
        print(Fore.YELLOW + "📋 LOGIN DE USUÁRIO\n" + Fore.CYAN + "-"*30)
        print()


        email = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite seu email: ",
            self.validador.validar_email,
            ""
        )


        senha = self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua senha: ")

        usuario = self.user_service.login_usuario(email, senha)

        if not usuario:
            print(Fore.RED + "❌ Email ou senha incorretos.")
            self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
            return None

        print(Fore.GREEN + "\nLogin realizado com sucesso!")
        self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")

        return usuario