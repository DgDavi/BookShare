from colorama import Fore

from services.user_services import editar_email, editar_nome, editar_senha
from data.db import get_db_connection
from utils.validador import validar_novo_email, validar_input, validar_nova_senha
from utils.limpar_tela import limpar_tela
from utils.security import hash_senha

def menu_editar(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()

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
        opcao = int(input(Fore.GREEN + "👉 Escolha uma opção: "))
    except ValueError:
        print(Fore.RED + "❌ Digite apenas números de opções válidas!")
        opcao = None

    if opcao == 1:
        print()
        confirmacao_senha = input(Fore.YELLOW + "👉 Digite sua senha para confirmar: ")
        senha_hashed = hash_senha(confirmacao_senha)
        if senha_hashed != usuario.senha_hashed:
            print(Fore.RED + "❌ Você digitou a senha errada. A operação foi cancelada.")
            input(Fore.GREEN + "\nPressione a tecla Enter para seguir... ")
            return

        print()
        novo_nome = validar_input(
            "Digite o novo nome: ",
            lambda n: 3 <= len(n) <= 50,
            Fore.RED + "❌ O nome deve conter entre 3 e 50 caracteres.\n" + Fore.YELLOW + "👉 Tente novamente."
        )

        resultado = editar_nome(usuario, novo_nome, cursor)
        if resultado:
            conexao.commit()
            cursor.close()
            conexao.close()
            print(Fore.GREEN + "\nEmail editado com sucesso!!")
            input(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
            
        
    elif opcao == 2:
        print()
        confirmacao_senha = input(Fore.YELLOW + "👉 Digite sua senha para confirmar: ")
        senha_hashed = hash_senha(confirmacao_senha)
        if senha_hashed != usuario.senha_hashed:
            print(Fore.RED + "❌ Você digitou a senha errada. A operação foi cancelada.")
            input(Fore.GREEN + "\nPressione a tecla Enter para seguir... ")
            return

        print()
        novo_email = validar_input(
            "Digite o novo email: ",
            validar_novo_email,
            "",
            cursor
        )

        resultado = editar_email(usuario, novo_email, cursor)
        if resultado:
                conexao.commit()
                cursor.close()
                conexao.close()
                print(Fore.GREEN + "\nEmail editado com sucesso!!")
                input(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
            

    elif opcao == 3:
        print()
        confirmacao_senha = input(Fore.YELLOW + "👉 Digite sua senha para confirmar: ")
        senha_hashed = hash_senha(confirmacao_senha)
        if senha_hashed != usuario.senha_hashed:
            print(Fore.RED + "❌ Você digitou a senha errada. A operação foi cancelada.")
            input(Fore.GREEN + "\nPressione a tecla Enter para seguir... ")
            return

        print()
        nova_senha = validar_nova_senha()
        nova_senha_hashed = hash_senha(nova_senha)
        
        resultado = editar_senha(usuario, nova_senha_hashed, cursor)
        if resultado:
            conexao.commit()
            cursor.close()
            conexao.close()
            print(Fore.GREEN + "\nSenha editado com sucesso!!")
            input(Fore.GREEN + "Pressione a tecla Enter para seguir... ")


    elif opcao == 0:
        input(Fore.YELLOW + "👉 Pressione Enter para continuar...")
        return