from colorama import init
from data.schema import create_tables
from interfaces.menu import MenuInicial

def main():
    create_tables()
    init(autoreset=True)
    menu = MenuInicial()
    menu.exibir()
    

if __name__ == "__main__":
    main()