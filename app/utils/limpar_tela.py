import os

def limpar_tela():
    # Limpa a tela do terminal
    os.system('cls' if os.name == 'nt' else 'clear')



# Vou implmentar no código
def obter_opcao(mensagem, min, max):
    print(mensagem)
    try:
        opcao = int(input("Digite a sua opção: "))
    except ValueError:
        print('Opção inválida.')
        return False
    if opcao > max or opcao < min:
        print('Opção inválida.')
        return False
    
    return opcao 
    
