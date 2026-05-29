from colorama import Fore
import smtplib
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from utils.security import verificar_senha


class Validador:

    def __init__(self):
        """Carrega as variáveis de ambiente usadas nas validações."""
        load_dotenv()

    def validar_email(self, email):
        """Valida o formato do email."""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))


    def validar_senha(self, senha):
        """Valida complexidade mínima da senha."""
        maiuscula = any(c.isupper() for c in senha)
        numero = any(c.isdigit() for c in senha)
        especial = any(not c .isalnum() for c in senha)
        tamanho = len(senha) >= 8
        return maiuscula and numero and especial and tamanho


    def input_com_prompt_colorido(self, mensagem):
        """Lê uma entrada usando o padrão visual do terminal."""
        return input(mensagem + Fore.WHITE)


    def validar_input(self, mensagem, validacao_funcao, mensagem_erro, *args):
        """Repete a entrada até receber um valor válido ou zero."""
        while True:
            valor = self.input_com_prompt_colorido(mensagem)
            if isinstance(valor, str) and valor.strip() == '0':
                return None

            if validacao_funcao(valor, *args):
                return valor

            if mensagem_erro and mensagem_erro.strip():
                print(mensagem_erro)


    def validar_nova_senha(self):
        """Solicita e confirma uma nova senha."""
        while True:
            senha = self.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua nova senha (0 para voltar): ")
            if isinstance(senha, str) and senha.strip() == '0':
                return None
            if not self.validar_senha(senha):
                print(Fore.RED + "❌ A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula, um número e um caractere especial")
                continue

            confirmacao = self.input_com_prompt_colorido(Fore.YELLOW + "👉 Digite sua senha novamente: ")
            if isinstance(confirmacao, str) and confirmacao.strip() == '0':
                return None

            if senha != confirmacao:
                print(Fore.RED + "❌ As senhas não coincidem.")
                print(Fore.YELLOW + "👉 Tente novamente.")
                continue

            return senha


    def validar_novo_email(self, email):
        """Valida o formato de um novo email."""
        if not self.validar_email(email):
            print(Fore.RED + "❌ Formatação do email incorreta.")
            return False
        return True


    def validar_email_login(self, email, cursor):
        """Verifica se o email existe antes do login."""

        cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE email = ?)", (email,))
        if cursor.fetchone()[0] == 0:
            print(Fore.RED + "❌ Email não encontrado.")
            return False
        return True


    def validar_senha_login(self, senha, email, cursor):
        """Compara a senha informada com a senha cadastrada."""
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        if not resultado:
            return False
        senha_original = resultado[0]

        return verificar_senha(senha, senha_original)
    

    def validar_opcao(self, minimo, maximo):
        """Valida uma opção numérica dentro de um intervalo."""
        try:
            opcao = int(input(Fore.GREEN + "👉 Escolha uma opção: " + Fore.WHITE))
        except ValueError:
            return None
        if opcao > maximo or opcao < minimo:
            return None
        
        return opcao 


    def enviar_codigo(self, email_destino, codigo):
        """Envia um código de verificação por email."""
        remetente = os.getenv("EMAIL_REMETENTE", "").strip()
        senha = os.getenv("EMAIL_SENHA", "").replace(" ", "").strip()
        if not remetente or not senha:
            print(Fore.RED + "❌ Variáveis de ambiente EMAIL_REMETENTE ou EMAIL_SENHA não definidas.")
            return False

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = email_destino
        msg['Subject'] = "Código de verificação"

        msg.attach(MIMEText(f"Seu código de verificação é: {codigo}", 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(remetente, senha)
                server.sendmail(remetente, email_destino, msg.as_string())
            print(Fore.GREEN + "✅ Código de verificação enviado com sucesso.")
            return True
        except smtplib.SMTPAuthenticationError:
            print(Fore.RED + "❌ Falha na autenticação SMTP. Verifique EMAIL_REMETENTE e EMAIL_SENHA (use senha de app do Gmail).")
            return False
        except Exception as erro:
            print(Fore.RED + f"❌ Falha ao enviar o email: {erro}")
            return False
