from colorama import Fore

from repository.livro_repository import buscar_livros
from .exibir_livros import exibir_livros_procurado
from data.db import get_db_connection
from utils.validador import input_com_prompt_colorido
from utils.limpar_tela import limpar_tela

def procurar_livros():
    conexao = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    livro_procurado = input_com_prompt_colorido(Fore.YELLOW + "👉 Digite o nome ou autor do livro que está procurando: ")

    livros = buscar_livros(livro_procurado, cursor)

    exibir_livros_procurado(livros)

    cursor.close()
    conexao.close()

    input_com_prompt_colorido(Fore.YELLOW + "\n👉 Pressione Enter para continuar...")
    return


    

