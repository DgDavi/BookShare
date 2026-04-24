from colorama import Fore

from services.livro_services import listar_livros_emprestados, tentar_devolver_livro
from utils.limpar_tela import limpar_tela
from utils.validador import input_com_prompt_colorido


def devolver_livros(usuario):
    limpar_tela()

    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "📤 DEVOLVER LIVRO".center(60))
    print(Fore.CYAN + "=" * 60)

    livros_emprestados = listar_livros_emprestados(usuario)

    if not livros_emprestados:
        print(Fore.YELLOW + "\nVocê não tem livros emprestados no momento.")
        input_com_prompt_colorido(Fore.YELLOW + "\n👉 Pressione Enter para voltar...")
        return

    print(Fore.YELLOW + "\nSelecione o ID do livro que deseja devolver:\n")

    for livro in livros_emprestados:
        print(Fore.LIGHTMAGENTA_EX + "ID: " + Fore.WHITE + f"{livro['id']}")
        print(Fore.LIGHTMAGENTA_EX + "Dono (ID): " + Fore.WHITE + f"{livro['user_id']}")
        print(Fore.LIGHTMAGENTA_EX + "Título: " + Fore.WHITE + f"{livro['titulo']}")
        print(Fore.LIGHTMAGENTA_EX + "Autor: " + Fore.WHITE + f"{livro['autor']}")
        print(Fore.LIGHTMAGENTA_EX + "Data do empréstimo: " + Fore.WHITE + f"{livro['data_emprestimo']}")
        print(Fore.CYAN + "-" * 60)

    livro_id_escolhido = input_com_prompt_colorido(
        Fore.GREEN + "👉 Digite o ID do livro para devolver (0 para cancelar): "
    )

    try:
        livro_id = int(livro_id_escolhido)
    except ValueError:
        print(Fore.RED + "❌ ID inválido.")
        input_com_prompt_colorido(Fore.YELLOW + "\n👉 Pressione Enter para continuar...")
        return

    if livro_id == 0:
        return

    sucesso, mensagem = tentar_devolver_livro(usuario.id, livro_id)
    print((Fore.GREEN if sucesso else Fore.RED) + mensagem)
    input_com_prompt_colorido(Fore.YELLOW + "\n👉 Pressione Enter para continuar...")