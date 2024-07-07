"""
Generic utilities related to CLI and file manipulation.
"""

# standard library imports
from datetime import datetime
from functools import reduce
from os import listdir, path
from signal import signal, SIGINT, SIGTERM
from sys import exit  # pylint: disable=redefined-builtin
from typing import Iterable


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


def list_files_with_extension(directory: str, extension: str) -> Iterable[str]:
    """
    Lists the files in the given directory with the given extension.
    """

    all_files = listdir(directory)

    selected_filenames = [
        f
        for f in all_files
        if f.endswith(extension)
    ]

    selected_filepaths = [
        path.join(directory, f)
        for f in selected_filenames
    ]

    return selected_filepaths


def get_printable_list(items: Iterable[str]) -> str:
    """
    Returns a printable list of the given filepaths.
    """
    sorted_items = sorted(items)

    concatenated_items = reduce(
        lambda f, concatenated:
        f'{f}\n\t{concatenated}' if concatenated else f,
        sorted_items,
        ''
    )

    printable_items = concatenated_items if concatenated_items else " (none)"

    return printable_items