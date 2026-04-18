from colorama import Fore

from data.db import get_db_connection
from utils.validador import validar_input
from model.livro import Livro
from utils.limpar_tela import limpar_tela
from repository.livro_repository import criar_livro, buscar_livros_usuario, buscar_livros

def cadastrar_livro(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    limpar_tela()
    print(Fore.YELLOW + "📋 CADASTRO DE LIVROS\n" + Fore.CYAN + "-"*30)
    print()

    titulo = validar_input(
        Fore.YELLOW + "👉 Digite o nome do livro: ",
        lambda n: 3 <= len(n) <= 40,
        Fore.YELLOW + "👉 O nome deve conter entre 3 e 40 caracteres."
    )

    descricao = validar_input(
        Fore.YELLOW + "👉 Digite a descrição do livro: ",
        lambda n:3 <= len(n) <= 200,
        Fore.YELLOW + "👉 A descrição deve conter entre 3 e 200 caracteres."
    )

    autor = validar_input(
        Fore.YELLOW + "👉 Digite o autor do livro: ",
        lambda n: 3 <= len(n) <= 40,
        Fore.YELLOW + "👉 O nome do autor deve conter entre 3 e 40 caracteres."
    )

    livro = Livro(titulo=titulo, descricao=descricao, autor=autor, user_id=usuario.id)
    livro_criado = criar_livro(livro, cursor)

    if livro_criado:
        conexao.commit()
        cursor.close()
        conexao.close()
        return livro_criado

    cursor.close()
    conexao.close()
    return None


def listar_livros_do_usuario(usuario):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        return buscar_livros_usuario(usuario, cursor)
    finally:
        cursor.close()
        conexao.close()


def buscar_livros_por_termo(termo):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        termo_normalizado = termo.strip().lower()
        return buscar_livros(termo_normalizado, cursor)
    finally:
        cursor.close()
        conexao.close()

