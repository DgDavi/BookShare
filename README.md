# BookShare

BookShare é um sistema em Python, com interface em terminal, para cadastro de usuários e gerenciamento de empréstimos de livros. O projeto usa SQLite para persistência de dados, `colorama` para estilos no terminal, `bcrypt` para armazenamento seguro de senhas e `python-dotenv` para configuração por variáveis de ambiente.

## Funcionalidades

- Cadastro de usuário
- Login com senha protegida por `bcrypt`
- Exibição dos dados da conta
- Cadastro de livros com título, descrição e autor
- Busca de livros por título ou autor
- Empréstimo de livro com validações de disponibilidade
- Limite de 1 livro emprestado por usuário
- Fila de empréstimo para livros indisponíveis
- Caixa de entrada para mensagens e avisos do sistema
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
- python-dotenv

## Estrutura do projeto

```text
BookShare/
|-- Fluxogramas/
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
|   |   |-- menu_login.py
|   |   |-- menu_register.py
|   |   |-- procurar_livros.py
|   |-- model/
|   |   |-- __init__.py
|   |   |-- livro.py
|   |   |-- usuario.py
|   |-- repository/
|   |   |-- mensagem_repository.py
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

## Configurar o venv

O projeto já foi pensado para rodar em um ambiente virtual separado. Isso evita conflito com outras dependências instaladas na máquina.

Para criar o ambiente virtual na raiz do projeto, execute:

```bash
python -m venv venv
```

Para ativar no Windows:

```bash
venv\Scripts\activate
```

Para ativar no Linux ou macOS:

```bash
source venv/bin/activate
```

Quando terminar de usar o projeto, você pode sair do ambiente com:

```bash
deactivate
```

## Configurar o .env

O projeto usa variáveis de ambiente para o envio de código de verificação por email. Crie um arquivo chamado `.env` na raiz do projeto com os dados abaixo:

```env
EMAIL_REMETENTE=seu_email@gmail.com
EMAIL_SENHA=sua_senha_de_app
```

Se você não for usar o fluxo de envio de email, essas variáveis podem ficar vazias, mas o arquivo `.env` deve existir quando a funcionalidade for testada.

## Instalação

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Na raiz do projeto, rode:

```bash
python app/main.py
```

Na primeira execução, o sistema cria as tabelas do banco SQLite automaticamente, se elas não existirem.

## Prints do projeto rodando

- Estrutura do projeto:
<img width="1163" height="844" alt="Image" src="https://github.com/user-attachments/assets/637ebb6b-a231-4e2e-af2b-32c734792362" />


- Menu Inicial:
<img width="572" height="270" alt="Image" src="https://github.com/user-attachments/assets/f1f7ed1d-49b1-4d87-a04e-1f73d35cfc92" />


- Menu de Cadastro:
<img width="664" height="217" alt="Image" src="https://github.com/user-attachments/assets/ae5df0dc-abea-46c5-8b14-06bbe06bd134" />


- Menu de Usuário Logado:
<img width="617" height="302" alt="Image" src="https://github.com/user-attachments/assets/75b9bf10-0944-48d3-bd2a-0a1c67ab42a1" />


- Menu Conta:
<img width="627" height="375" alt="Image" src="https://github.com/user-attachments/assets/b771307f-92b9-4d5f-83ec-dd1a44860e86" />


- Menu de Procurar Livros:
<img width="577" height="413" alt="Image" src="https://github.com/user-attachments/assets/635da66b-d059-4b50-8459-07f9688bc536" />


- Caixa de Entrada:
<img width="1329" height="321" alt="Image" src="https://github.com/user-attachments/assets/29cf61d9-b7e5-4ed0-8518-990c2eaf6ee6" />


## Observações

- O arquivo `usuarios.db` é o banco local do projeto.
- As senhas são salvas com `bcrypt`.
- A validação de email é feita por expressão regular.
- O envio de código por email depende das variáveis `EMAIL_REMETENTE` e `EMAIL_SENHA` no arquivo `.env`.
- O fluxo principal do sistema é todo via terminal.

## Roadmap

As próximas evoluções planejadas para o projeto são:

  2VA:
- Paginação na busca de livros, para não carregar todos os livros de uma vez.
- Fila de empréstimo para livros com mais de um interessado.
- Histórico de empréstimos.
- Aba de avisos para exibir quando o livro for emprestado.
- Melhorar o funcionamento da data limite para o empréstimo.
- Criar uma opção de voltar para quando o usuário estiver em um fluxo de entrada poder sair.
- Punição para caso a devolução não seja efetuada


3VA:
- Fluxo de pedido de empréstimo: o dono do livro recebe uma solicitação e decide se autoriza o empréstimo
- Melhorar o design do sistema com a biblioteca rich
- Permitir doações (Troca de dono)
- Permitir envio de fotos do livro que está sendo cadastrado (via JSON)
- Sistema de avaliação
- Perfil publico de usuário


## Autores

- Davi Gomes - GitHub: https://github.com/DgDavi
- Lucas Augusto - GitHub: https://github.com/luquetaaasn
