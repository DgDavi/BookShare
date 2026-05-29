import math
from datetime import datetime, timedelta

from model.livro import Livro
from repository.livro_repository import LivroRepository
from repository.usuario_repository import UserRepository
from utils.validador import Validador

class LivroService:
    def __init__(self):
        self.livro_repo = LivroRepository()
        self.validador = Validador()
        self.user_repo = UserRepository()

    def cadastrar_livro(self,nome, descricao, autor, usuario):
        """Cria e salva um novo livro do usuário."""
        livro = Livro(titulo=nome, descricao=descricao, autor=autor, user_id=usuario.id)
        livro_criado = self.livro_repo.criar_livro(livro)

        if livro_criado:
            return livro_criado
        return None


    def listar_livros_do_usuario(self, usuario):
        """Lista os livros cadastrados por um usuário."""
        return self.livro_repo.buscar_livros_usuario(usuario)


    def listar_livros_emprestados(self, usuario):
        """Lista os livros emprestados para um usuário."""
        return self.livro_repo.buscar_livros_emprestados(usuario.id)


    def buscar_livros_por_termo(self, termo, pagina=1):
        """Busca livros por termo com paginação."""
        itens_por_pagina = 5
        pagina = max(1, pagina)
        offset = (pagina - 1) * itens_por_pagina
    
        termo_normalizado = termo.strip().lower()
        livros = self.livro_repo.buscar_livros(termo_normalizado, itens_por_pagina, offset)

        total = self.livro_repo.contar_livros(termo_normalizado)

        total_paginas = math.ceil(total / itens_por_pagina)

        return {
            "livros": livros,
            "pagina": pagina,
            "total_paginas": total_paginas, 
            "total_livros": total
        }


    def emprestar_livro(self, livro_id, usuario_id):
        """Registra o empréstimo de um livro."""
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.livro_repo.emprestar_livro_repo(livro_id, usuario_id, data_atual)


    def devolver_livro(self, livro_id):
        """Registra a devolução de um livro."""
        self.livro_repo.devolver_livro_repo(livro_id)


    def livro_atrasado(data_emprestimo):
        """Verifica se o empréstimo já passou do prazo de 7 dias."""
        if not data_emprestimo:
            return False

        data = datetime.strptime(data_emprestimo, "%Y-%m-%d %H:%M:%S")
        limite = data + timedelta(days=7)

        return datetime.now() > limite


    def atualizar_status_livros(self):
        """Atualiza o status dos empréstimos vencidos."""
        return self.livro_repo.atualizar_status_livro()


    def tentar_emprestar_livro(self, usuario_id, livro_id):
        """Aplica as regras de negócio e tenta realizar o empréstimo."""
        self.atualizar_status_livros()

        status = self.user_repo.obter_status_por_id(usuario_id)
        if status and status.get("bloqueado_atraso"):
            return False, "❌ Você está bloqueado de novos empréstimos até devolver os livros atrasados."

        suspenso_ate = status.get("suspenso_ate") if status else None
        if suspenso_ate:
            try:
                suspenso_dt = datetime.strptime(suspenso_ate, "%Y-%m-%d %H:%M:%S")
                if datetime.now() < suspenso_dt:
                    return False, f"❌ Sua conta está suspensa até {suspenso_dt.strftime('%d/%m/%Y')}."
            except Exception:
                pass

        livro = self.livro_repo.buscar_livro_por_id(livro_id)
        if not livro:
            return False, "❌ Livro não encontrado."

        if livro["user_id"] == usuario_id:
            return False, "❌ Você não pode pegar emprestado o próprio livro."

        if livro["disponivel"] == 0:
            if self.livro_repo.usuario_ja_esta_na_fila(livro_id, usuario_id):
                posicao = self.livro_repo.posicao_na_fila(livro_id, usuario_id)
                return False, f"⏳ Livro indisponível no momento. Você já está na fila na posição {posicao}."

            posicao = self.livro_repo.adicionar_usuario_na_fila(livro_id, usuario_id)
            return False, f"⏳ Livro indisponível no momento. Você entrou na fila de empréstimo na posição {posicao}."

        if self.livro_repo.usuario_tem_emprestimo_ativo(usuario_id):
            return False, "❌ Você já possui um empréstimo ativo."

        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.livro_repo.emprestar_livro_repo(livro_id, usuario_id, data_atual)

        return True, "✅ Empréstimo realizado por 7 dias."


    def tentar_devolver_livro(self, usuario_id, livro_id):
        """Valida o empréstimo e tenta devolver o livro."""

        livro = self.livro_repo.buscar_livro_por_id(livro_id)
        if not livro:
            return False, "❌ Livro não encontrado."

        if livro["usuario_emprestimo"] != usuario_id:
            return False, "❌ Esse livro não está emprestado para você."

        if livro["disponivel"] == 1:
            return False, "❌ Esse livro já está disponível."

        self.livro_repo.devolver_livro_repo(livro_id)

        return True, "✅ Livro devolvido com sucesso."
