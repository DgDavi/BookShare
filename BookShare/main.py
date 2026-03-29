from colorama import init

from interfaces.menu import menu_inical

init(autoreset=True)

# Chama o menu principal do aplicativo
def main():
    menu_inical()


if __name__ == "__main__":
    main()
