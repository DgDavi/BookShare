from colorama import Fore

from utils.security import hash_senha, verificar_senha
from model.usuario import Usuario
from utils.limpar_tela import limpar_tela
from repository.usuario_repository import UserRepository
from utils.validador import Validador


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.validador = Validador()

    def cadastrar_usuario(self, nome, email, senha):
        """Valida e cria um novo usuário."""
        email_normalizado = email.strip().lower()
        if not self.validador.validar_email(email_normalizado):
            return None

        if self.user_repo.email_existe(email_normalizado):
            print(Fore.RED + "❌ Email já cadastrado.")
            return None

        senha_hashed = hash_senha(senha)
        usuario = Usuario(nome, email_normalizado, senha_hashed)
        uid = self.user_repo.criar_usuario(usuario)

        if uid:
            usuario.id = uid
            return usuario
        return None
            

    def login_usuario(self, email, senha):
        """Autentica um usuário pelo email e senha."""
        usuario_row = self.user_repo.buscar_por_email(email)
        if not usuario_row:
            return None

        if not verificar_senha(senha, usuario_row[3]):
            return None

        usuario = Usuario(
            nome=usuario_row[1],
            email=usuario_row[2],
            senha_hashed=usuario_row[3],
            id=usuario_row[0]
        )

        return usuario


    def obter_dados_usuario(self, usuario):
        """Busca os dados do usuário para exibição."""
        return self.user_repo.buscar_dados_usuario(usuario)


    def editar_nome_usuario(self, usuario, novo_nome):
        """Atualiza o nome do usuário autenticado."""
        return self.user_repo.editar_nome(usuario, novo_nome)


    def editar_email_usuario(self, usuario, novo_email):
        """Atualiza o email do usuário autenticado."""
        return self.user_repo.editar_email(usuario, novo_email)


    def editar_senha_usuario(self, usuario, nova_senha_hashed):
        """Atualiza a senha do usuário autenticado."""
        return self.user_repo.editar_senha(usuario, nova_senha_hashed)


    def deletar_usuario_com_confirmacao(self, usuario):
        """Remove a conta do usuário autenticado."""
        return self.user_repo.deletar_usuario(usuario)


    def validar_novo_email_unico(self, email):
        """Valida o formato do email e impede duplicidade."""
        email_normalizado = email.strip().lower()
        if not self.validador.validar_email(email_normalizado):
            print(Fore.RED + "❌ Formatação do email incorreta.")
            return False

        if self.user_repo.email_existe(email_normalizado):
            print(Fore.RED + "❌ Email já cadastrado.")
            return False

        return True
    

    def verificar_codigo_email(self, codigo_enviado, codigo_recebido):
        """Compara o código enviado com o código informado."""
        return codigo_enviado == codigo_recebido
