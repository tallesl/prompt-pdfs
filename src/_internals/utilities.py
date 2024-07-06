"""
Initializes OllamaEmbeddings and Chroma.
"""
from datetime import datetime
from signal import signal, SIGINT, SIGTERM
from sys import exit  # pylint: disable=redefined-builtin


def log(message: str, end: str = '\n') -> None:
    """
    Prints the given message with the current time.
    """
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {message}', end=end)


def set_signals() -> None:
    """
    Sets signal handlers for SIGINT and SIGTERM.
    """
    signal(SIGINT, lambda _, __: exit(0))
    signal(SIGTERM, lambda _, __: exit(0))

