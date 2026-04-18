from colorama import Fore

from repository.livro_repository import buscar_livros
from data.db import get_db_connection
from utils.limpar_tela import limpar_tela
from utils.validador import input_com_prompt_colorido

def exibir_livros(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "📋 MEUS LIVROS".center(60))
    print(Fore.CYAN + "=" * 60)

    livros = buscar_livros(usuario, cursor)

    if not livros:
        print("Você não tem livros cadastrados.")
    else:
        for livro in livros:
            print(Fore.LIGHTMAGENTA_EX + "ID: " + Fore.WHITE + f"{livro['id']}")
            print(Fore.LIGHTMAGENTA_EX + "ID do usuário: "  + Fore.WHITE + f"{livro['user_id']}")
            print(Fore.LIGHTMAGENTA_EX + "Título: " + Fore.WHITE + f"{livro['titulo']}")
            print(Fore.LIGHTMAGENTA_EX + "Descrição: "  + Fore.WHITE + f"{livro['descricao']}")
            print(Fore.CYAN + "-"*60)

    input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para voltar...")
    return True

