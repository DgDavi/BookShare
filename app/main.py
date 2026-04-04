from colorama import init

from data.schema import create_tables
from interfaces.menu import menu_inical

init(autoreset=True)

# Criar tabelas se não existirem
create_tables()

# Chama o menu principal do aplicativo
def main():
    menu_inical()


if __name__ == "__main__":
    main()
