from colorama import init

from data.schema import create_tables, create_tables_livros
from interfaces.menu import menu_inical


def main():
    create_tables()
    create_tables_livros()

    init(autoreset=True)

    menu_inical()


if __name__ == "__main__":
    main()
