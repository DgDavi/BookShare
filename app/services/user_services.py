from colorama import Fore

from data.db import get_db_connection
from model.usuario import Usuario
from utils.limpar_tela import limpar_tela
from utils.security import hash_senha
from repository.usuario_repository import UserRepository
from utils.validador import Validador


class UserService:
    def __init__(self, user_repo: UserRepository, validador: Validador):
        self.user_repo = user_repo
        self.validador = validador

    def cadastrar_usuario(self):
        """
        Realiza o cadastro de um novo usuário via terminal.

        Returns:
            Usuario | None: Retorna o usuário criado em caso de sucesso.
            Caso o cadastro não seja concluído, retorna None.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        limpar_tela()
        print(Fore.YELLOW + "📋 CADASTRO DE USUÁRIO\n" + Fore.CYAN + "-"*30)
        print()

        
        nome = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite seu nome: ",
            lambda n: 3 <= len(n) <= 50,
            Fore.RED + "❌ O nome deve conter entre 3 e 50 caracteres.\n" + Fore.YELLOW + "👉 Tente novamente."
        )
            

        email = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite seu email: ",
            self.validador.validar_novo_email,
            "",
            cursor
        )


        senha = self.validador.validar_nova_senha()
        senha_hashed = hash_senha(senha)
        

        usuario = Usuario(nome, email, senha_hashed)
        usuario_criado = self.user_repo.criar_usuario(usuario, cursor)

        if usuario_criado:
            print(Fore.GREEN + "\nUsuário cadastrado com sucesso!")
            self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")
        
            conexao.commit()
            cursor.close()
            conexao.close()

            return usuario
        
        return None


    def login_usuario(self):
        """
        Autentica um usuário com email e senha informados no terminal.

        Returns:
            Usuario | None: Retorna a instância autenticada quando o login é válido.
            Se falhar, retorna None.
        """
        conexao  = get_db_connection()
        cursor = conexao.cursor()

        limpar_tela()
        print(Fore.YELLOW + "📋 LOGIN DE USUÁRIO\n" + Fore.CYAN + "-"*30)
        print()


        email = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite seu email: ",
            self.validador.validar_email_login,
            "",
            cursor
        )


        senha = self.validador.validar_input(
            Fore.YELLOW + "👉 Digite sua senha: ",
            self.validador.validar_senha_login,
            Fore.RED + "❌ Senha incorreta.",
            email,
            cursor
        )

        cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,))
        usuario_login = cursor.fetchone()

        if not usuario_login:
            cursor.close()
            conexao.close()
            return None

        usuario = Usuario(
            nome=usuario_login[1],
            email=usuario_login[2],
            senha_hashed=usuario_login[3],
            id=usuario_login[0]
        )

        cursor.close()
        conexao.close()
        print(Fore.GREEN + "\nLogin realizado com sucesso!")
        self.validador.input_com_prompt_colorido(Fore.GREEN + "Pressione a tecla Enter para seguir... ")

        return usuario


    def obter_dados_usuario(self, usuario):
        """
        Busca os dados do usuário para exibição na interface.

        Args:
            usuario (Usuario): Usuário autenticado no sistema.

        Returns:
            sqlite3.Row | tuple | None: Registro com os dados do usuário.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            return self.user_repo.buscar_dados_usuario(usuario, cursor)
        finally:
            cursor.close()
            conexao.close()


    def editar_nome_usuario(self, usuario, novo_nome):
        """
        Edita o nome do usuário autenticado.

        Args:
            usuario (Usuario): Usuário autenticado.
            novo_nome (str): Novo nome a ser atribuído.

        Returns:
            bool: True se editado com sucesso, False caso contrário.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            resultado = self.user_repo.editar_nome(usuario, novo_nome, cursor)
            conexao.commit()
            return resultado
        finally:
            cursor.close()
            conexao.close()


    def editar_email_usuario(self, usuario, novo_email):
        """
        Edita o email do usuário autenticado.

        Args:
            usuario (Usuario): Usuário autenticado.
            novo_email (str): Novo email a ser atribuído.

        Returns:
            bool: True se editado com sucesso, False caso contrário.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            resultado = self.user_repo.editar_email(usuario, novo_email, cursor)
            conexao.commit()
            return resultado
        finally:
            cursor.close()
            conexao.close()


    def editar_senha_usuario(self, usuario, nova_senha_hashed):
        """
        Edita a senha do usuário autenticado.

        Args:
            usuario (Usuario): Usuário autenticado.
            nova_senha_hashed (str): Nova senha já com hash aplicado.

        Returns:
            bool: True se editada com sucesso, False caso contrário.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            resultado = self.user_repo.editar_senha(usuario, nova_senha_hashed, cursor)
            conexao.commit()
            return resultado
        finally:
            cursor.close()
            conexao.close()


    def deletar_usuario_com_confirmacao(self, usuario):
        """
        Deleta a conta do usuário autenticado.

        Args:
            usuario (Usuario): Usuário autenticado.

        Returns:
            bool: True se deletado com sucesso, False caso contrário.
        """
        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            self.user_repo.deletar_usuario(usuario, cursor)
            conexao.commit()
            return True
        finally:
            cursor.close()
            conexao.close()


    def validar_novo_email_unico(self, email):
        """
        Valida se um novo email é único no sistema (não cadastrado).

        Args:
            email (str): Email a ser validado.

        Returns:
            bool: True se email é válido e único, False caso contrário.
        """
        if not self.validador.validar_email(email):
            print(Fore.RED + "❌ Formatação do email incorreta.")
            return False

        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
            if cursor.fetchone()[0] == 1:
                print(Fore.RED + "❌ Email já cadastrado.")
                return False
            return True
        finally:
            cursor.close()
            conexao.close()
