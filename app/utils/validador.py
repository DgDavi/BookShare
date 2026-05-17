from colorama import Fore
from email_validator import validate_email, EmailNotValidError

from utils.security import verificar_senha

class Validador:

    def validar_email(self, email):
        try:
            info_email = validate_email(email, check_deliverability=True)
            return True, info_email.normalized
        except EmailNotValidError:
            return False, None


    def validar_senha(self, senha):
        maiuscula = any(c.isupper() for c in senha)
        numero = any(c.isdigit() for c in senha)
        especial = any(not c .isalnum() for c in senha)
        tamanho = len(senha) >= 8
        return maiuscula and numero and especial and tamanho


    def input_com_prompt_colorido(self, mensagem):
        return input(mensagem + Fore.WHITE)


    def validar_input(self, mensagem, validacao_funcao, mensagem_erro, *args):
        while True:
            valor = self.input_com_prompt_colorido(mensagem)
            resultado = validacao_funcao(valor, *args)
            if isinstance(resultado, tuple):
                valido, valor_validado = resultado
                if valido:
                    return valor_validado
            elif resultado:
                return valor

            if mensagem_erro and mensagem_erro.strip():
                print(mensagem_erro)


    def validar_nova_senha(self):
        while True:
            senha = self.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua nova senha: ")
            if not self.validar_senha(senha):
                print(Fore.RED + "❌ A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula, um número e um caractere especial")
                continue

            confirmacao = self.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua senha novamente: ")

            if senha != confirmacao:
                print(Fore.RED + "❌ As senhas não coincidem.")
                print(Fore.YELLOW + "👉 Tente novamente.")
                continue

            return senha


    def validar_novo_email(self, email):
        valido, _ = self.validar_email(email)

        if not valido:
            print(Fore.RED + "❌ Formatação do email incorreta.")
            return False
        return True


    def validar_email_login(self, email, cursor):

        cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
        if cursor.fetchone()[0] == 0:
            print(Fore.RED + "❌ Email não encontrado.")
            return False
        return True


    def validar_senha_login(self, senha, email, cursor):
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        if not resultado:
            return False
        senha_original = resultado[0]

        return verificar_senha(senha, senha_original)
    

    def validar_opcao(self, mensagem, minimo, maximo):
        print(mensagem)
        try:
            opcao = int(input("Digite a sua opção: "))
        except ValueError:
            return None
        if opcao > maximo or opcao < minimo:
            return None
        
        return opcao 
