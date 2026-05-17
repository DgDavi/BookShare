from colorama import Fore

from services.user_services import UserService
from utils.security import verificar_senha
from utils.validador import Validador

class MenuDeletar:
    def __init__(self):
        self.validador = Validador()
        self.user_service = UserService()

        
    def deletar_conta(self, usuario):
        confirmacao = self.validador.input_com_prompt_colorido(Fore.RED + "\nTem certeza que deseja deletar sua conta? (s): ")

        if confirmacao.lower() == "s":
            confirmacao_senha = self.validador.input_com_prompt_colorido(Fore.RED + "Digite sua senha para confirmar: ")

            if verificar_senha(confirmacao_senha, usuario.senha_hashed):
                self.user_service.deletar_usuario_com_confirmacao(usuario)
                print(Fore.GREEN + "\nConta deletada com sucesso.")

                self.validador.input_com_prompt_colorido(Fore.GREEN + "👉 Pressione Enter para continuar...")
                return True
        
        print(Fore.YELLOW + "\nA operação foi cancelada.")
        self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")

        return False

            

