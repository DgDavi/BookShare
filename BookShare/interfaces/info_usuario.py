from data.db import get_db_connection


def mostrar_dados(email):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()

    if usuario:
        print("\n--- SEUS DADOS ---")
        print(f"Nome: {usuario[0]}")
        print(f"Email: {usuario[1]}")
        print(f"Senha: {usuario[2]}")
    else:
        print("Usuário não encontrado.")
