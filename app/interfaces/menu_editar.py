from colorama import Fore

from model.usuario import editar_email, editar_nome
from data.db import get_db_connection
from utils.validador import validar_email_cadastro, validar_input
from utils.limpar_tela import limpar_tela

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
            novo_email = validar_input(
                "Digite o novo email: ",
                lambda e: validar_email_cadastro(e, cursor),
                ""
            )

            resultado = editar_email(usuario, novo_email, cursor)
            if resultado:
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    print(Fore.GREEN + "\nEmail editado com sucesso!!")
                    input(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
            

    elif opcao == 3:
        print("A fazer")

    elif opcao == 0:
        from interfaces.menu_conta import menu_conta
        menu_conta(usuario)