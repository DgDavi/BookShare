from colorama import init
from data.schema import create_tables
from dotenv import load_dotenv
from interfaces.menu import MenuInicial

def main():
    create_tables()
    init(autoreset=True)
    load_dotenv()
    menu = MenuInicial()
    menu.exibir()
    

if __name__ == "__main__":
    main()