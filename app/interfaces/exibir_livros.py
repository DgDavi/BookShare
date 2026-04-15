from repository.livro_repository import buscar_livros

def exibir_livros(usuario, cursor):
    print("\n=== MEUS LIVROS ===")

    livros = buscar_livros(usuario, cursor)

    if not livros:
        print("Você não tem livros cadastrados.")
    else:
        for livro in livros:
            print(f"ID: {livro[0]}")
            print(f"Título: {livro[2]}")
            print(f"Descrição: {livro[3]}")
            print("------")
