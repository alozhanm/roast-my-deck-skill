"""Terminal output formatting utilities."""

from colorama import Fore, Style, init

init(autoreset=True)

# Constants
BANNER = r"""
 ____  ___   __   ____  ____    __  __ _  _  ____  ____  ____  ___  __ _
(  _ \/ _ \ / _\ / ___)(_  _)  (  )(  ( \/ )(_  _)/ ___)(  _ \/ __)(  / )
 )   /\__  /    \\___ \  )(     )( /    / /__) )(  \___ \ )   /\__ \ )  (
(__\_)(___/\_/\_/(____/ (__)   (__)\_)__)\_____)(__)(____(___/ (___/(__\_)

         roast-my-deck 🔥  |  brutally honest. powered by Claude AI.
"""
DIVIDER = "─" * 60
SECTION_ROAST = "THE ROAST:"
SECTION_FIXES = "OK FINE, HERE'S HOW TO FIX IT:"


def print_header() -> None:
    """Print the application banner to stdout."""
    print(Fore.RED + BANNER)
    print(Fore.WHITE + DIVIDER)


def print_roast(response: str) -> None:
    """Format and print the Claude roast response with dividers.

    Args:
        response: Full response string from Claude.
    """
    print()
    for line in response.splitlines():
        if line.strip() == SECTION_ROAST:
            print(Fore.RED + Style.BRIGHT + DIVIDER)
            print(Fore.RED + Style.BRIGHT + line)
            print(Fore.RED + Style.BRIGHT + DIVIDER)
        elif line.strip() == SECTION_FIXES:
            print()
            print(Fore.YELLOW + Style.BRIGHT + DIVIDER)
            print(Fore.YELLOW + Style.BRIGHT + line)
            print(Fore.YELLOW + Style.BRIGHT + DIVIDER)
        elif line.strip().startswith(("1.", "2.", "3.")):
            print(Fore.CYAN + line)
        else:
            print(Fore.WHITE + line)
    print()
    print(Fore.WHITE + DIVIDER)


def print_success(msg: str) -> None:
    """Print a green success message.

    Args:
        msg: Message to display.
    """
    print(Fore.GREEN + Style.BRIGHT + f"✓ {msg}")


def print_error(msg: str) -> None:
    """Print a red error message.

    Args:
        msg: Error message to display.
    """
    print(Fore.RED + Style.BRIGHT + f"✗ {msg}")


def print_warning(msg: str) -> None:
    """Print a yellow warning message.

    Args:
        msg: Warning message to display.
    """
    print(Fore.YELLOW + f"⚠ {msg}")
