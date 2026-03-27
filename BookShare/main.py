from services.auth_services import cadastrar_usuario

# Menu principal do aplicativo (Por enquanto só funciona o cadastro)
def menu():
    print("----------------------------BOOKSHARE-----------------------------")
    print("1. Cadastrar usuário")
    print("2. Login")
    print("3. Sobre o projeto")
    print("4. Sair")
    print("-----------------------------------------------------------------\n")
    opcao = int(input("Digite o número da opção desejada: "))

    if opcao == 1:
        cadastrar_usuario()


if __name__ == "__main__":
    menu()

