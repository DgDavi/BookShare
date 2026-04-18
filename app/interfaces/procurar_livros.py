from colorama import Fore

from .exibir_livros import exibir_livros_procurado
from services.livro_services import buscar_livros_por_termo
from utils.validador import input_com_prompt_colorido
from utils.limpar_tela import limpar_tela

def procurar_livros():
    limpar_tela()
    livro_procurado = input_com_prompt_colorido(Fore.YELLOW + "👉 Digite o nome ou autor do livro que está procurando: ")

    livros = buscar_livros_por_termo(livro_procurado)

    exibir_livros_procurado(livros)

    input_com_prompt_colorido(Fore.YELLOW + "\n👉 Pressione Enter para continuar...")
    return


    

