# BookShare

BookShare é um sistema em Python, com interface em terminal, para cadastro de usuários e gerenciamento de empréstimos de livros. O projeto usa SQLite para persistência de dados, `colorama` para estilos no terminal e `bcrypt` para armazenamento seguro de senhas.

## Funcionalidades

- Cadastro de usuário
- Login com senha protegida por `bcrypt`
- Exibição dos dados da conta
- Cadastro de livros com título, descrição e autor
- Busca de livros por título ou autor
- Empréstimo de livro com validações de disponibilidade
- Limite de 1 livro emprestado por usuário
- Devolução de livro pela interface de conta
- Exibição dos livros cadastrados e dos livros emprestados
- Atualização de status para manter disponibilidade correta dos livros
- Edição de nome, email e senha
- Exclusão de conta
- Logout e retorno ao menu inicial

## Tecnologias

- Python
- SQLite
- colorama
- bcrypt

## Estrutura do projeto

```text
BookShare/
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- data/
|   |   |-- __init__.py
|   |   |-- db.py
|   |   |-- schema.py
|   |-- interfaces/
|   |   |-- __init__.py
|   |   |-- deletar_conta.py
|   |   |-- devolver_livros.py
|   |   |-- exibir_livros.py
|   |   |-- exibir_usuario.py
|   |   |-- info_menu.py
|   |   |-- menu.py
|   |   |-- menu_conta.py
|   |   |-- menu_de_usuario.py
|   |   |-- menu_editar.py
|   |   |-- procurar_livros.py
|   |-- model/
|   |   |-- __init__.py
|   |   |-- livro.py
|   |   |-- usuario.py
|   |-- repository/
|   |   |-- livro_repository.py
|   |   |-- usuario_repository.py
|   |-- services/
|   |   |-- __init__.py
|   |   |-- livro_services.py
|   |   |-- user_services.py
|   |-- utils/
|   |   |-- __init__.py
|   |   |-- limpar_tela.py
|   |   |-- security.py
|   |   |-- validador.py
|-- requirements.txt
|-- README.md
```

## Requisitos

- Python 3.10 ou superior
- `pip`

## Instalação

1. Crie e ative um ambiente virtual, se quiser isolar o projeto:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux:

```bash
.venv\bin\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Na raiz do projeto, rode:

```bash
python app/main.py
```

Na primeira execução, o sistema cria as tabelas do banco SQLite automaticamente, se elas não existirem.

## Observações

- O arquivo `usuarios.db` é o banco local do projeto.
- As senhas são salvas com `bcrypt`.
- O fluxo principal do sistema é todo via terminal.

## Release

As próximas evoluções planejadas para o projeto são:

  2VA:
- Paginação na busca de livros, para não carregar todos os livros de uma vez.
- Validação de email por código.
- Fila de empréstimo para livros com mais de um interessado.
- Histórico de empréstimos.
- Aba de avisos para exibir quando o livro for emprestado.
- Melhorar o funcionamento da data limite para o empréstimo.


  3VA:
- Criação de uma aba de mensagens entre usuários.
- Fluxo de pedido de empréstimo: o dono do livro recebe uma solicitação e decide se autoriza o empréstimo.


## Autores

- Davi Gomes - GitHub: https://github.com/DgDavi
- Lucas Augusto - GitHub: https://github.com/luquetaaasn
