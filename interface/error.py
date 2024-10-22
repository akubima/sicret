from .print import failed as print_failed

def handle_exception(e: Exception) -> None:
    print_failed(f"An error has occurred! [{type(e).__name__}] Detail: \033[4m{str(e)}\033[0m")

def print_message(message: str) -> None:
    print_failed(f"An error has occurred! {message}")
