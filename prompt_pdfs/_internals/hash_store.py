"""
Manages storing and indexing file hashes.
"""

# pylint: disable=redefined-outer-name

# standard library imports
from hashlib import md5
from os import path
from typing import Iterable

# local imports
from ..configuration import hash_indexing
from .utilities import log


def filter_indexed_files(source_filepaths: Iterable[str]) -> dict[str, str]:
    """
    Lists from the given source files the ones that are not in the given indexed hashes.
    """

    # calculating the hash for each given source filepath
    source_files_hashes = {
        f: calculate_file_hash(f)
        for f in source_filepaths
    }

    # listing indexed hashes currently present in file
    indexed_hashes = list_indexed_hashes()

    # finding the source filepaths hashes that does are not present on the file
    non_indexed = {
        f: h
        for f, h in source_files_hashes.items()
        if h not in indexed_hashes
    }

    return non_indexed


def list_indexed_hashes() -> Iterable[str]:
    """
    Lists the hashes of the indexed files in the given path.
    """

    # configuration values used in this function
    filepath: str = hash_indexing.filepath  # pylint: disable=no-member

    log(f'Listing hashes in: {filepath}')

    # if there is no file, return empty list of hashes
    if not path.exists(filepath):
        return set()

    # if the file exists, read its contents and returns it (each line it's a hash)
    with open(filepath, 'r', encoding='utf-8') as f:
        hashes = set(line.strip() for line in f)
        log(f'{len(hashes)} hashes listed.')
        return hashes


def store_hash(filehash: str) -> None:
    """
    Registers the given file hash as indexed.
    """

    # configuration values used in this function
    filepath: str = hash_indexing.filepath  # pylint: disable=no-member

    log(f'Indexing hash: {filehash}')

    # appending the given hash to the end of the file
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f'{filehash}\n')

    log('Hash indexed.')


def calculate_file_hash(filepath: str) -> str:
    """
    Calculates the MD5 hash of the file at the given filepath.
    """
    hasher = md5()

    with open(filepath, 'rb') as file:
        buffer = file.read()
        hasher.update(buffer)

    return hasher.hexdigest()
