# BookShare

BookShare e um sistema em Python, com interface em terminal, para cadastro de usuarios e gerenciamento de empréstimos de livros. O projeto usa SQLite para persistencia de dados, `colorama` para estilos no terminal e `bcrypt` para armazenamento seguro de senhas.

## Funcionalidades

- Cadastro de usuario
- Login com senha protegida por `bcrypt`
- Exibição dos dados da conta
- Cadastro de livros com titulo, descrição e autor
- Listagem dos livros do usuario
- Busca de livros por titulo ou autor
- Edição de nome, email e senha
- Exclusão de conta
- Deslogar e voltar ao menu inicial

## Tecnologias

- Python
- SQLite
- colorama
- bcrypt

## Estrutura do projeto

```text
BookShare/
|-- app/
|   |-- main.py
|   |-- data/
|   |   |-- db.py
|   |   |-- schema.py
|   |-- interfaces/
|   |-- model/
|   |-- repository/
|   |-- services/
|   |-- utils/
|-- usuarios.db
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

2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

## Como executar

Na raiz do projeto, rode:

```bash
python app/main.py
```

Na primeira execucao, o sistema cria as tabelas do banco SQLite automaticamente, se elas nao existirem.

## Observacoes

- O arquivo `usuarios.db` e o banco local do projeto.
- As senhas sao salvas com `bcrypt`.
- O fluxo principal do sistema e todo via terminal.

## Autor

Projeto BookShare desenvolvido para estudo e pratica de Python, persistencia com SQLite e organizacao em camadas.

## Autores

- Davi Gomes - GitHub: https://github.com/DgDavi
- Lucas Augusto - GitHub: https://github.com/luquetaaasn
