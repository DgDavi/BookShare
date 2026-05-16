from services.user_services import UserService
from utils.limpar_tela import limpar_tela
from utils.validador import Validador

from colorama import Fore

class Register:
    def __init__(self):
        self.user_service = UserService()
        self.validador = Validador()

    def exibir(self):
        """
        Realiza o cadastro de um novo usuário via terminal.

        Returns:
            Usuario | None: Retorna o usuário criado em caso de sucesso.
            Caso o cadastro não seja concluído, retorna None.
        """

        limpar_tela()
        print(Fore.YELLOW + "📋 CADASTRO DE USUÁRIO\n" + Fore.CYAN + "-"*30)
        print()

    
        nome = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite seu nome: ",
            lambda n: 3 <= len(n) <= 50,
            Fore.RED + "❌ O nome deve conter entre 3 e 50 caracteres.\n" + Fore.YELLOW + "👉 Tente novamente."
        )
            
        email = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite seu email: ",
            self.user_service.validar_novo_email_unico,
            ""
        )

        senha = self.validador.validar_nova_senha()
        
        usuario_criado = self.user_service.criar_usuario(nome, email, senha)

        if usuario_criado:
            print(Fore.GREEN + "\nUsuário cadastrado com sucesso!")
            self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
        

            return usuario_criado
        
        return None
