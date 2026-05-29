from colorama import Fore

from utils.limpar_tela import limpar_tela
from services.user_services import UserService
from utils.validador import Validador

class Login:
    def __init__(self):
        self.user_service = UserService()
        self.validador = Validador()

    def exibir(self):
        """Executa o fluxo de login do usuário."""

        limpar_tela()
        print(Fore.YELLOW + "📋 LOGIN DE USUÁRIO\n" + Fore.CYAN + "-"*30)
        print()


        email = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite seu email: ",
            self.validador.validar_email,
            Fore.RED + "❌ Formatação do email incorreta.\n" + Fore.YELLOW + "👉 Tente novamente."
        )

        if email is None:
            return None


        senha = self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua senha: ")
        if isinstance(senha, str) and senha.strip() == '0':
            return None

        usuario = self.user_service.login_usuario(email, senha)

        if not usuario:
            print(Fore.RED + "❌ Email ou senha incorretos.")
            self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
            return None

        print(Fore.GREEN + "\nLogin realizado com sucesso!")
        self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")

        return usuario