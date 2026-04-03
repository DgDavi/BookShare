from data.db import get_db_connection

def deletar_conta(email):
    confirmacao = input("Tem certeza que deseja deletar sua conta? (s/n): ")

    if confirmacao.lower() != "s":
        print("Operação cancelada.")
        return

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM usuarios WHERE email = ?", (email,))
    conexao.commit()

    print("Conta deletada com sucesso!")
