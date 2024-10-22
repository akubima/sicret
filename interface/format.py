"""
This module contains functions which provides methods to format
messages for the user interface.
"""

# This function is used to format to a standarized message format.
def general (message: str, level: int = 1) -> str:
    return "| " + "---" * level + message