from colorama import Fore
from datetime import datetime
from utils.limpar_tela import limpar_tela
from utils.validador import Validador
from repository.mensagem_repository import MensagemRepository


class CaixaEntrada:
    def __init__(self):
        self.validador = Validador()
        self.msg_repo = MensagemRepository()

    def exibir(self, usuario):
        """Exibe as notificações e avisos do usuário logado."""
        while True:
            limpar_tela()
            print(Fore.CYAN + "="*60)
            print(Fore.CYAN + "📩 CAIXA DE ENTRADA".center(60))
            print(Fore.CYAN + "="*60)
            
            
            user_id = usuario.id 
            
            # Busca as mensagens e guarda em "mensagens"
            mensagens = self.msg_repo.buscar_mensagens_usuario(user_id)
            
            if not mensagens:
                print(Fore.YELLOW + f"\nOlá, {usuario.nome}! Você não tem nenhuma mensagem ou aviso por enquanto.")
            else:
                print(Fore.WHITE + f"\nOlá, {usuario.nome}! Veja seus avisos recentes:\n")
                print(Fore.CYAN + "-"*60)
                
                for msg in mensagens:
                    texto = msg[2]
                    data_banco = msg[3] 
                    
                    try:
                        
                        data_dt = datetime.strptime(data_banco, "%Y-%m-%d %H:%M:%S")
                        data_formatada = data_dt.strftime("%d/%m/%Y às %H:%M")
                    except:
                        data_formatada = data_banco 
                    
                    print(Fore.LIGHTBLACK_EX + f"[{data_formatada}] " + Fore.WHITE + f"{texto}")
                    print(Fore.CYAN + "-"*60)
            
            print("\n")
            self.validador.input_com_prompt_colorido(Fore.YELLOW + "👉 Pressione Enter para voltar ao menu...")
            return