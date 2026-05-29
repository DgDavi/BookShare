from colorama import Fore

from .exibir_livros import ExibirLivros
from services.livro_services import LivroService
from utils.validador import Validador
from utils.limpar_tela import limpar_tela
from repository.usuario_repository import UserRepository

class ProcurarLivro:
    def __init__(self):
        self.validador = Validador()
        self.livro_service = LivroService()
        self.exibir_livros = ExibirLivros()
        self.user_repo = UserRepository()

    def procurar_livros(self, usuario):
        """
        Exibe a tela de busca e apresenta os livros encontrados.

        Args:
            usuario (Usuario): Usuário autenticado que está pesquisando livros.

        Returns:
            None: Fluxo de interface com entrada e saída pelo terminal.
        """
        # Verifica se a conta está suspensa antes de permitir buscar
        status = self.user_repo.obter_status_por_id(usuario.id)
        suspenso_ate = status.get("suspenso_ate") if status else None
        if suspenso_ate:
            try:
                from datetime import datetime
                suspenso_dt = datetime.strptime(suspenso_ate, "%Y-%m-%d %H:%M:%S")
                if datetime.now() < suspenso_dt:
                    limpar_tela()
                    print(Fore.RED + f"❌ Sua conta está suspensa até {suspenso_dt.strftime('%d/%m/%Y')}. Não é possível buscar livros.")
                    input(Fore.YELLOW + "👉 Pressione Enter para continuar...")
                    return
            except Exception:
                pass

        limpar_tela()
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "🔎 PROCURAR LIVRO".center(60))
        print(Fore.CYAN + "=" * 60)

        livro_procurado = self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite o nome ou autor do livro que está procurando: ")
        pagina_atual = 1

        while True:
            resultado = self.livro_service.buscar_livros_por_termo(livro_procurado, pagina_atual)

            limpar_tela()

            self.exibir_livros.exibir_livros_procurado(resultado["livros"], usuario)

            print(Fore.CYAN + f"\n📄 Página {resultado['pagina']} de {resultado['total_paginas']}")

            if resultado["total_paginas"] <= 1:
                self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
                return

            print(Fore.LIGHTMAGENTA_EX + "\n[N]" + Fore.WHITE + " Próxima página")
            print(Fore.LIGHTMAGENTA_EX + "[P]" + Fore.WHITE + " Página anterior")
            print(Fore.LIGHTMAGENTA_EX + "[0]" + Fore.WHITE + " Voltar")

            opcao = self.validador.input_com_prompt_colorido(
                Fore.GREEN + "👉 Escolha uma opção ou digite o ID do livro desejado: "
            ).strip().lower()

            if opcao == "0" or opcao == "":
                return

            if opcao == "n" and pagina_atual < resultado["total_paginas"]:
                pagina_atual += 1
            elif opcao == "p" and pagina_atual > 1:
                pagina_atual -= 1
            else:
                try:
                    livro_id = int(opcao)
                except ValueError:
                    print(Fore.RED + "❌ Opção inválida.")
                    self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
                    continue

                sucesso, mensagem = self.livro_service.tentar_emprestar_livro(usuario.id, livro_id)
                print((Fore.GREEN if sucesso else Fore.RED) + mensagem)
                self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para continuar...")
                return
