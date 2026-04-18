from colorama import Fore

from services.livro_services import listar_livros_do_usuario
from utils.limpar_tela import limpar_tela
from utils.validador import input_com_prompt_colorido

def exibir_livros(usuario):
    limpar_tela()
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "📋 MEUS LIVROS".center(60))
    print(Fore.CYAN + "=" * 60)

    livros = listar_livros_do_usuario(usuario)

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


def exibir_livros_procurado(livros):
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "📋 LIVROS ENCONTRADOS".center(60))
    print(Fore.CYAN + "=" * 60)

    if not livros:
        print(Fore.RED + "❌ Nenhum livro encontrado.")
        return

    for livro in livros:
        disponibilidade = "Disponivel" if livro["disponivel"] else "Indisponivel"

        print(Fore.LIGHTMAGENTA_EX + "ID: " + Fore.WHITE + f"{livro['id']}")
        print(Fore.LIGHTMAGENTA_EX + "Dono (ID): " + Fore.WHITE + f"{livro['user_id']}")
        print(Fore.LIGHTMAGENTA_EX + "Titulo: " + Fore.WHITE + f"{livro['titulo']}")
        print(Fore.LIGHTMAGENTA_EX + "Autor: " + Fore.WHITE + f"{livro['autor']}")
        print(Fore.LIGHTMAGENTA_EX + "Descricao: " + Fore.WHITE + f"{livro['descricao']}")
        print(Fore.LIGHTMAGENTA_EX + "Status: " + Fore.WHITE + disponibilidade)
        print(Fore.CYAN + "-" * 60)
        
        
