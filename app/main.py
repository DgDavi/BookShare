from colorama import init
from data.schema import create_tables
from dependencies import build_menu_inicial

def main():
    create_tables()
    init(autoreset=True)
    build_menu_inicial().exibir()

if __name__ == "__main__":
    main()