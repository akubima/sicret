"""
This module contains methods for printing various types of messages
and headers to the terminal. It includes methods for printing separators, headers, warnings,
success messages, failure messages, and informational messages with standardized formats and colors.
"""
from .common import clear_terminal
from .__init__ import default_terminal_line_length
from .format import general as format_general
import time

# This function is used to print a separator line, nothing fancy.
def separator(count: int = default_terminal_line_length) -> None:
    print("|", "-" * count, "|")

# This function is used to print the header of the program, giving the user a brief info about this program.
def header(clear: bool = True) -> None:

    if clear: clear_terminal()

    separator()
    print("\n", "\033[4mSIMPLE CARBON EMISSION TRACKER\033[0m (SICRET)".center(default_terminal_line_length), "\n")
    separator()

# This function prints a standarized warning message template in the terminal.
def warning(message: str, end: str = '\n') -> None:
    print("\033[33m| ---[!] Warning:\033[0m " + message, end=end)

# This function prints a standarized success message template in the terminal.
def success(message: str, end: str = '\n') -> None:
    print("\033[32m| ---[V] Success:\033[0m " + message, end=end)

# This function prints a standarized failed message template in the terminal.
def failed(message: str, end: str = '\n') -> None:
    print("\033[31m| ---[X] Failed:\033[0m " + message, end=end)

# This function prints a standarized info message template in the terminal.
def info(message: str, end: str = '\n') -> None:
    print("\033[34m| ---[i] Info:\033[0m " + message, end=end)

def general(message: str, end: str = '\n'):
    print(format_general(message), end=end)

def animated_print(message: str, delay: float = 0.1):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
