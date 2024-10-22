"""
This module provides common utility functions for the user interface.
"""
import os
import interface.format as iface_format

def clear_terminal() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def input_general(message: str):
    return input(f'{iface_format.general(f'\033[96m[INPUT]\033[0m {message}')} -> ')