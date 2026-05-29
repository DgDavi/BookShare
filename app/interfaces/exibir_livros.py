from colorama import Fore

from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from services.livro_services import LivroService


class ExibirLivros:
    def __init__(self):
        self.validador = Validador()
        self.livro_service = LivroService()

    def exibir(self, usuario):
        """Exibe livros cadastrados e livros emprestados do usuário."""
        limpar_tela()
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "📋 MEUS LIVROS".center(60))
        print(Fore.CYAN + "=" * 60)

        livros = self.livro_service.listar_livros_do_usuario(usuario)
        livros_emprestados = self.livro_service.listar_livros_emprestados(usuario)

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

        self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para voltar...")
        return True


    def exibir_livros_procurado(self, livros, usuario=None):
        """Exibe os livros retornados na busca."""
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

        return


