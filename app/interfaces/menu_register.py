from services.user_services import UserService
from utils.limpar_tela import limpar_tela
from utils.security import gerar_codigo
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
        if nome is None:
            return None
            
        email = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite seu email: ",
            self.user_service.validar_novo_email_unico,
            ""
        )
        if email is None:
            return None
        
        codigo = gerar_codigo()
        self.validador.enviar_codigo(email, codigo)
        codigo_recebido = self.validador.input_com_prompt_colorido(
            Fore.YELLOW + "👉 Foi enviado um código para o seu email. Digite o código recebido: "
        )
        if isinstance(codigo_recebido, str) and codigo_recebido.strip() == '0':
            print(Fore.YELLOW + "Operação cancelada pelo usuário.")
            return None
        if self.user_service.verificar_codigo_email(codigo, codigo_recebido):
            print(Fore.GREEN + "✅ Código correto.")
        else:
            print(Fore.RED + "❌ Código errado. Operação cancelada.")
            return False
        

        senha = self.validador.validar_nova_senha()
        if senha is None:
            print(Fore.YELLOW + "Operação cancelada pelo usuário.")
            return None
        
        usuario_criado = self.user_service.cadastrar_usuario(nome, email, senha)

        if usuario_criado:
            print(Fore.GREEN + "\nUsuário cadastrado com sucesso!")
            self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")

            return usuario_criado
        
        return None
