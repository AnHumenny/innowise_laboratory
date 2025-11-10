from colorama import init, Fore, Back, Style

init()

def show_colorama():
    """Demonstrates the capabilities of the Colorama library for working with colored text in the terminal.
    The function displays several text lines with different color combinations:
    - Various text colors (foreground)
    - Various background colors (background)
    - Text styles (bright/bold)
    - Style reset after each line

    Key features:
    - Style.RESET_ALL is required to prevent style "bleeding" to subsequent text
    - Colors only work in supported terminals
    - Requires preliminary initialization: colorama.init()

    Returns:
        None: The function only outputs text, doesn't return any values.
    """

    print(f"{Fore.RED}{Back.YELLOW}Hello World! {Style.RESET_ALL}")
    print(f"{Fore.GREEN}Hello World in Green{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{Style.BRIGHT}Hello World in Bright Blue!{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{Back.CYAN}Hello World with Magenta text and Cyan background{Style.RESET_ALL}")


if __name__ == "__main__":
    show_colorama()