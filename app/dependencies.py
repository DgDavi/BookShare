from utils.validador import Validador
from repository.livro_repository import LivroRepository
from repository.usuario_repository import UserRepository
from services.livro_services import LivroService
from services.user_services import UserService
from interfaces.exibir_livros import ExibirLivros
from interfaces.devolver_livros import DevolverLivro
from interfaces.menu_editar import MenuEditar
from interfaces.deletar_conta import MenuDeletar
from interfaces.exibir_usuario import ExibirUsuario
from interfaces.menu_conta import MenuConta
from interfaces.procurar_livros import ProcurarLivro
from interfaces.menu_livro_cadastro import CadastroLivro
from interfaces.menu_register import Register
from interfaces.menu_login import Login
from interfaces.menu_de_usuario import MenuUsuario
from interfaces.info_menu import InfoMenu
from interfaces.menu import MenuInicial

def build_menu_inicial() -> MenuInicial:
    validador = Validador()

    livro_repo = LivroRepository()
    user_repo = UserRepository()

    livro_service = LivroService(livro_repo, validador)
    user_service = UserService(user_repo, validador)

    exibir_livros   = ExibirLivros(validador, livro_service)
    devolver_livro  = DevolverLivro(validador, livro_service)
    menu_editar     = MenuEditar(user_service, validador)
    menu_deletar    = MenuDeletar(validador, user_service)
    exibir_usuario  = ExibirUsuario(user_service)

    menu_conta = MenuConta(
        exibir_livros, devolver_livro,
        menu_editar, menu_deletar,
        exibir_usuario, validador
    )

    procurar_livro = ProcurarLivro(validador, livro_service, exibir_livros)
    cadastro_livro = CadastroLivro(livro_service, validador)
    menu_usuario   = MenuUsuario(livro_service, menu_conta, procurar_livro, validador, cadastro_livro)
    info_menu      = InfoMenu(validador)
    menu_register  = Register(user_service, validador)
    menu_login     = Login(user_service, validador)

    return MenuInicial(menu_register, menu_usuario, info_menu, validador, menu_login)