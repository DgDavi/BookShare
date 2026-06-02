from datetime import datetime, timedelta
from colorama import Fore
from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from services.livro_services import LivroService # Importa o Service como você faz nas outras views

class HistoricoEmprestimos:
    def __init__(self):
        self.validador = Validador()
        self.livro_service = LivroService() 

    def exibir(self, usuario):
        """Exibe o histórico completo de empréstimos (antigos e atuais)."""
        while True:
            limpar_tela()
            print(Fore.CYAN + "="*60)
            print(Fore.CYAN + "📜 SEU HISTÓRICO DE EMPRÉSTIMOS".center(60))
            print(Fore.CYAN + "="*60)
            
            user_id = usuario.id
            
            historico = self.livro_service.buscar_historico_usuario(user_id)
            
            if not historico:
                print(Fore.YELLOW + f"\nOlá, {usuario.nome}! Você ainda não tem nenhum registro de empréstimo no histórico.")
            else:
                print(Fore.WHITE + f"\nOlá, {usuario.nome}! Aqui está o seu histórico completo:\n")
                print(Fore.CYAN + "-"*60)
                
                for registro in historico:
                    
                    titulo = registro[0]
                    autor = registro[1]
                    data_emp_banco = registro[2]
                    data_dev_banco = registro[3]
                    
                    try:
                        data_inicio = datetime.strptime(data_emp_banco, "%Y-%m-%d %H:%M:%S")
                        data_inicio_pt = data_inicio.strftime("%d/%m/%Y às %H:%M")
                    except:
                        data_inicio_pt = data_emp_banco

                    # Lógica para definir o Status (Se foi devolvido ou se ainda está ativo)
                    if data_dev_banco:
                        try:
                            data_fim = datetime.strptime(data_dev_banco, "%Y-%m-%d %H:%M:%S")
                            data_fim_pt = data_fim.strftime("%d/%m/%Y às %H:%M")
                        except:
                            data_fim_pt = data_dev_banco
                        status = Fore.GREEN + f"✅ Devolvido em: {data_fim_pt}"
                    else:
                        
                        try:
                            data_limite = data_inicio + timedelta(days=7)
                            prazo_pt = data_limite.strftime("%d/%m/%Y")
                        except:
                            prazo_pt = "Não calculada"
                        status = Fore.YELLOW + f"📖 Empréstimo Ativo (Devolver até {prazo_pt})"
                    
                    print(Fore.WHITE + f"📖 Livro: " + Fore.CYAN + f"{titulo} " + Fore.LIGHTBLACK_EX + f"({autor})")
                    print(Fore.LIGHTBLACK_EX + f"   Retirado em: {data_inicio_pt}")
                    print(f"   Status: {status}")
                    print(Fore.CYAN + "-"*60)
            
            print("\n")
            self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para voltar ao menu...")
            return
