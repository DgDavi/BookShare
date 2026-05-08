from colorama import Fore

from utils.limpar_tela import limpar_tela
from utils.validador import Validador


class InfoMenu:
    def __init__(self, validador: Validador):
        self.validador = validador

    # Menu de informações sobre o projeto
    def exibir(self):
        """
        Exibe informações institucionais e objetivo do projeto BookShare.

        Returns:
            None: Mostra conteúdo informativo e retorna ao menu inicial.
        """
        limpar_tela()

        print(Fore.CYAN + "="*60)
        print(Fore.CYAN + "📚 SOBRE O PROJETO".center(60))
        print(Fore.CYAN + "="*60)

        print()
        print("""O BookShare é um aplicativo de compartilhamento de livros desenvolvido como parte da disciplina de Projeto Interdisciplinar para Sistemas de Informação I na Universidade Federal Rural de Pernambuco (UFRPE). O projeto foi idealizado e criado por Davi Gomes e Lucas Augusto com o objetivo de aplicar, na prática, conceitos aprendidos ao longo do curso, unindo tecnologia e impacto social.

    A proposta do BookShare é permitir que usuários cadastrem seus livros, procurem por títulos disponíveis e compartilhem suas leituras com outros membros da comunidade. Dessa forma, o sistema busca promover a troca de conhecimento, incentivar o hábito da leitura e facilitar o acesso a diferentes obras de maneira colaborativa.

    Mais do que um simples sistema, o BookShare representa a ideia de que o conhecimento deve ser acessível e compartilhado, fortalecendo a conexão entre pessoas por meio da leitura.

    🔗 LinkedIn dos criadores:
    Davi Gomes: https://www.linkedin.com/in/davigomes1/
    Lucas Augusto: https://www.linkedin.com/in/lucas-augusto-a4124a404/

    💻 GitHub dos criadores:
    Davi Gomes: https://github.com/DgDavi
    Lucas Augusto: https://github.com/luquetaaasn""")

        print()
        self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para voltar ao menu principal...")
        return
