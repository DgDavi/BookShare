from datetime import datetime, timedelta
from colorama import Fore
from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from repository.livro_repository import LivroRepository

class HistoricoEmprestimos:
    def __init__(self):
        self.validador = Validador()
        self.livro_repo = LivroRepository()

    def exibir(self, usuario):
        """Exibe os empréstimos atuais e suas datas limite."""
        while True:
            limpar_tela()
            print(Fore.CYAN + "="*60)
            print(Fore.CYAN + "📜 SEUS EMPRÉSTIMOS ATUAIS".center(60))
            print(Fore.CYAN + "="*60)
            
            user_id = usuario.id
            livros_emprestados = self.livro_repo.buscar_historico_emprestimos(user_id)
            
            if not livros_emprestados:
                print(Fore.YELLOW + f"\nOlá, {usuario.nome}! Você não tem nenhum livro emprestado no momento.")
            else:
                print(Fore.WHITE + f"\nOlá, {usuario.nome}! Aqui estão os livros que estão com você:\n")
                print(Fore.CYAN + "-"*60)
                
                for livro in livros_emprestados:
                    titulo = livro[0]
                    data_banco = livro[1]
                    
                    try:
                        data_inicio = datetime.strptime(data_banco, "%Y-%m-%d %H:%M:%S")
                        data_fim = data_inicio + timedelta(days=7)
                        
                        data_inicio_pt = data_inicio.strftime("%d/%m/%Y")
                        data_fim_pt = data_fim.strftime("%d/%m/%Y às %H:%M")
                    except:
                        data_inicio_pt = data_banco
                        data_fim_pt = "Não calculada"
                    
                    print(Fore.WHITE + f"📖 Livro: " + Fore.GREEN + f"{titulo}")
                    print(Fore.LIGHTBLACK_EX + f"   Pegou em: {data_inicio_pt}")
                    print(Fore.YELLOW + f"   Devolver até: {data_fim_pt}")
                    print(Fore.CYAN + "-"*60)
            
            print("\n")
            self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para voltar ao menu...")
            return