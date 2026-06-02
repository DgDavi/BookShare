from data.db import get_db_connection

# Função para criar as tabelas do banco de dados
def create_tables():
    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
                )""")


    cursor.execute("""CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                autor TEXT NOT NULL,
                disponivel BOOLEAN NOT NULL DEFAULT 1 CHECK (disponivel IN (0, 1)),
                usuario_emprestimo INTEGER,
                data_emprestimo TEXT,
                FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (usuario_emprestimo) REFERENCES usuarios(id) ON DELETE SET NULL
                )""")
   
    cursor.execute("""CREATE TABLE IF NOT EXISTS mensagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mensagem TEXT NOT NULL,
                data_criacao TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
                )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS fila_emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                data_solicitacao TEXT NOT NULL,
                UNIQUE(livro_id, user_id),
                FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
                )""")
   
    cursor.execute("""CREATE TABLE IF NOT EXISTS historico_emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER,
    usuario_id INTEGER,
    data_emprestimo TEXT,
    data_devolucao TEXT, -- Fica NULL enquanto o livro não for devolvido
    FOREIGN KEY(livro_id) REFERENCES livros(id),
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
)""");
    
    conexao.commit()

    cursor.close()
    conexao.close()
