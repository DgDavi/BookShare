from colorama import Fore

from services.user_services import UserService
from utils.validador import Validador
from utils.limpar_tela import limpar_tela
from utils.security import verificar_senha, hash_senha

class MenuEditar:
    def __init__(self, user_service: UserService, validador: Validador):
        self.user_service = user_service
        self.validador = validador

    def exibir(self, usuario):
        """
        Exibe o menu de edição de dados cadastrais do usuário.

        Args:
            usuario (Usuario): Usuário autenticado que terá dados alterados.

        Returns:
            None: Executa o fluxo de edição e retorna ao menu anterior.
        """
        limpar_tela()
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "📋 EDITAR DADOS".center(60))
        print(Fore.CYAN + "=" * 60)
        print()
        print(Fore.LIGHTMAGENTA_EX + "[1]" + Fore.WHITE + " Nome")
        print(Fore.LIGHTMAGENTA_EX + "[2]" + Fore.WHITE + " Email")
        print(Fore.LIGHTMAGENTA_EX + "[3]" + Fore.WHITE + " Senha")
        print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Voltar")
        print(Fore.CYAN + "-"*60)
        
        try:
            opcao = int(self.validador.input_com_prompt_colorido(Fore.GREEN + "👉 Escolha uma opção: "))
        except ValueError:
            print(Fore.RED + "❌ Digite apenas números de opções válidas!")
            opcao = None

        if opcao == 1:
            print()
            confirmacao_senha = self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua senha para confirmar: ")
            if not verificar_senha(confirmacao_senha, usuario.senha_hashed):
                print(Fore.RED + "❌ Você digitou a senha errada. A operação foi cancelada.")
                self.validador.input_com_prompt_colorido(Fore.GREEN + "\nPressione a tecla Enter para seguir... ")
                return

            print()
            novo_nome = self.validador.validar_input(
                Fore.YELLOW + "👉 Digite o novo nome: ",
                lambda n: 3 <= len(n) <= 50,
                Fore.RED + "❌ O nome deve conter entre 3 e 50 caracteres.\n" + Fore.YELLOW + "👉 Tente novamente."
            )

            resultado = self.user_service.editar_nome_usuario(usuario, novo_nome)
            if resultado:
                print(Fore.GREEN + "\nNome editado com sucesso!!")
                self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
                
            
        elif opcao == 2:
            print()
            confirmacao_senha = self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua senha para confirmar: ")
            if not verificar_senha(confirmacao_senha, usuario.senha_hashed):
                print(Fore.RED + "❌ Você digitou a senha errada. A operação foi cancelada.")
                self.validador.input_com_prompt_colorido(Fore.GREEN + "\nPressione a tecla Enter para seguir... ")
                return

            print()
            novo_email = self.validador.validar_input(
                Fore.YELLOW + "👉 Digite o novo email: ",
                self.user_service.validar_novo_email_unico,
                "",
            )

            resultado = self.user_service.editar_email_usuario(usuario, novo_email)
            if resultado:
                    print(Fore.GREEN + "\nEmail editado com sucesso!!")
                    self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
                

        elif opcao == 3:
            print()
            confirmacao_senha = self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua senha para confirmar: ")
            if not verificar_senha(confirmacao_senha, usuario.senha_hashed):
                print(Fore.RED + "❌ Você digitou a senha errada. A operação foi cancelada.")
                self.validador.input_com_prompt_colorido(Fore.GREEN + "\nPressione a tecla Enter para seguir... ")
                return

            print()
            nova_senha = self.validador.validar_nova_senha()
            nova_senha_hashed = hash_senha(nova_senha)
            
            resultado = self.user_service.editar_senha_usuario(usuario, nova_senha_hashed)
            if resultado:
                print(Fore.GREEN + "\nSenha editada com sucesso!!")
                self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")


        elif opcao == 0:
            return
