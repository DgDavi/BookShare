from services.auth_services import cadastrar_usuario, login_usuario

# Menu principal do aplicativo (Por enquanto só funciona o cadastro)
def menu():
    print("----------------------------BOOKSHARE-----------------------------")
    print("1. Cadastrar usuário")
    print("2. Login")
    print("3. Sobre o projeto")
    print("0. Sair")
    opcao = int(input("\nDigite o número da opção desejada: "))

    # Chama a função de cadastro de usuário
    if opcao == 1:
        cadastrar_usuario()

    elif opcao == 2:
        login_usuario()

    elif opcao == 3:
        print("A fazer")

    elif opcao == 0:
        print("Saindo do aplicativo...")
        exit()

    else:
        print("Opção inválida. Tente novamente.")
        menu()


if __name__ == "__main__":
    menu()

