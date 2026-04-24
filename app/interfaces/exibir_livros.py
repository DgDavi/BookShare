from colorama import Fore

from services.livro_services import listar_livros_do_usuario, listar_livros_emprestados
from services.livro_services import tentar_emprestar_livro
from utils.limpar_tela import limpar_tela
from utils.validador import input_com_prompt_colorido

def exibir_livros(usuario):
    limpar_tela()
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "📋 MEUS LIVROS".center(60))
    print(Fore.CYAN + "=" * 60)

    livros = listar_livros_do_usuario(usuario)
    livros_emprestados = listar_livros_emprestados(usuario)

    print(Fore.YELLOW + "\n📚 Livros cadastrados por você\n")
    if not livros:
        print("Você não tem livros cadastrados.")
    else:
        for livro in livros:
            print(Fore.LIGHTMAGENTA_EX + "ID: " + Fore.WHITE + f"{livro['id']}")
            print(Fore.LIGHTMAGENTA_EX + "ID do usuário: "  + Fore.WHITE + f"{livro['user_id']}")
            print(Fore.LIGHTMAGENTA_EX + "Título: " + Fore.WHITE + f"{livro['titulo']}")
            print(Fore.LIGHTMAGENTA_EX + "Descrição: "  + Fore.WHITE + f"{livro['descricao']}")
            print(Fore.CYAN + "-"*60)

    print(Fore.YELLOW + "\n📖 Livros que você pegou emprestado\n")
    if not livros_emprestados:
        print("Você não pegou nenhum livro emprestado.")
    else:
        for livro in livros_emprestados:
            print(Fore.LIGHTMAGENTA_EX + "ID: " + Fore.WHITE + f"{livro['id']}")
            print(Fore.LIGHTMAGENTA_EX + "Dono (ID): " + Fore.WHITE + f"{livro['user_id']}")
            print(Fore.LIGHTMAGENTA_EX + "Título: " + Fore.WHITE + f"{livro['titulo']}")
            print(Fore.LIGHTMAGENTA_EX + "Autor: " + Fore.WHITE + f"{livro['autor']}")
            print(Fore.LIGHTMAGENTA_EX + "Data do empréstimo: " + Fore.WHITE + f"{livro['data_emprestimo']}")
            print(Fore.CYAN + "-"*60)

    input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para voltar...")
    return True


def exibir_livros_procurado(livros, usuario=None):
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

    if usuario is None:
        return

    livro_id_escolhido = input_com_prompt_colorido(
        Fore.GREEN + "👉 Digite o ID do livro para emprestar (0 para cancelar): "
    )

    try:
        livro_id = int(livro_id_escolhido)
    except ValueError:
        print(Fore.RED + "❌ ID inválido.")
        return

    if livro_id == 0:
        return

    sucesso, mensagem = tentar_emprestar_livro(usuario.id, livro_id)
    print((Fore.GREEN if sucesso else Fore.RED) + mensagem)
        
        
