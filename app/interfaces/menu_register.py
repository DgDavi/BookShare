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
        """Executa o fluxo de cadastro de usuário."""

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
        
       
        
        
       #checar se o código foi realmente enviado
        if not self.validador.enviar_codigo(email, codigo):
            print(Fore.RED + "\n❌ Não foi possível enviar o código de verificação.")
            print(Fore.RED + "   Verifique as configurações de e-mail no arquivo .env.")
            self.validador.input_com_prompt_colorido(Fore.YELLOW + "\n👉 Pressione Enter para voltar ao menu...")
            return None

       #ao passar da etapa anterior, ai sim o código é pedido
        codigo_recebido = self.validador.input_com_prompt_colorido(
            Fore.YELLOW + "👉 Um código foi enviado para o seu email. Digite o código recebido: "
        )
        
        if isinstance(codigo_recebido, str) and codigo_recebido.strip() == '0':
            print(Fore.YELLOW + "Operação cancelada pelo usuário.")
            return None
            
        if self.user_service.verificar_codigo_email(codigo, codigo_recebido):
            print(Fore.GREEN + "✅ Código correto.")
        else:
           #trava de tela, para dar tempo de o usuário ler a mensagem de erro
            print(Fore.RED + "\n❌ Código incorreto ou expirado! Operação cancelada.")
            self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para voltar ao menu...")
            return False
