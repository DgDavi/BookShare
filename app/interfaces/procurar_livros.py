from colorama import Fore

from .exibir_livros import exibir_livros_procurado
from services.livro_services import buscar_livros_por_termo
from utils.validador import input_com_prompt_colorido
from utils.limpar_tela import limpar_tela

def procurar_livros(usuario):
    """
    Exibe a tela de busca e apresenta os livros encontrados.

    Args:
        usuario (Usuario): Usuário autenticado que está pesquisando livros.

    Returns:
        None: Fluxo de interface com entrada e saída pelo terminal.
    """
    limpar_tela()
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "🔎 PROCURAR LIVRO".center(60))
    print(Fore.CYAN + "=" * 60)
    print()

    livro_procurado = input_com_prompt_colorido(Fore.YELLOW + "👉 Digite o nome ou autor do livro que está procurando: ")

    livros = buscar_livros_por_termo(livro_procurado)

    limpar_tela()

    exibir_livros_procurado(livros, usuario)

    input_com_prompt_colorido(Fore.YELLOW + "\n👉 Pressione Enter para continuar...")
    return


    

