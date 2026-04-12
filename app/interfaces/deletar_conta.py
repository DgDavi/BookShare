from colorama import Fore

from data.db import get_db_connection
from repository.usuario_repository import deletar_usuario
from utils.security import hash_senha

def deletar_conta(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    
    
    confirmacao = input(Fore.RED + "Tem certeza que deseja deletar sua conta? (s/n): ")

    if confirmacao.lower() == "s":
        confirmacao_senha = input(Fore.RED + "Digite sua senha para confirmar: ")
        confirmacao_senha = hash_senha(confirmacao_senha)

        cursor.execute("SELECT senha FROM usuarios WHERE id = ?", (usuario.id,))
        senha_armazenada = cursor.fetchone()

        if senha_armazenada and confirmacao_senha == senha_armazenada[0]:
            deletar_usuario(usuario, cursor)
            print(Fore.GREEN + "\nConta deletada com sucesso.")
            conexao.commit()
            cursor.close()
            conexao.close()

            input(Fore.YELLOW + "👉 Pressione Enter para continuar...")
            from interfaces.menu import menu_inical
            menu_inical()
            return True
    
    print(Fore.YELLOW + "\nA operação foi cancelada.")
    input(Fore.YELLOW + "👉 Pressione Enter para continuar...")

    cursor.close()
    conexao.close()
    return False

        

