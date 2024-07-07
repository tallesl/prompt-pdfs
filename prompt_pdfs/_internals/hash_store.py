"""
Manages storing and indexing file hashes.
"""

# pylint: disable=redefined-outer-name

# standard library imports
from hashlib import md5
from os import path
from typing import Iterable

# local imports
from .utilities import log


def filter_indexed_files(indexed_hashes_filepath: str, source_filepaths: Iterable[str]) -> dict[str, str]:
    """
    Lists from the given source files the ones that are not in the given indexed hashes.
    """

    indexed_hashes = list_indexed_hashes(indexed_hashes_filepath)

    source_files_hashes = {
        f: calculate_file_hash(f)
        for f in source_filepaths
    }

    non_indexed = {
        f: h
        for f, h in source_files_hashes.items()
        if h not in indexed_hashes
    }

    return non_indexed


def list_indexed_hashes(indexed_hashes_filepath: str) -> Iterable[str]:
    """
    Lists the hashes of the indexed files in the given path.
    """

    log(f'Listing hashes in: {indexed_hashes_filepath}')
    if not path.exists(indexed_hashes_filepath):
        return set()

    with open(indexed_hashes_filepath, 'r', encoding='utf-8') as f:
        hashes = set(line.strip() for line in f)
        log(f'{len(hashes)} hashes listed.')
        return hashes


def store_hash(indexed_hashes_filepath:str, filehash: str) -> None:
    """
    Registers the given file hash as indexed.
    """

    log(f'Indexing hash: {filehash}')

    with open(indexed_hashes_filepath, 'a', encoding='utf-8') as f:
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
