#! /usr/bin/env python3

"""
Indexes on a ChromaDB database the embeddings of the files residing in the configured directory and
extension.
"""

# pylint: disable=redefined-outer-name

from hashlib import md5
from os import path

from .utilities import log


def list_indexed_hashes(indexed_hashes_filepath: str) -> set[str]:
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


def index_hash(indexed_hashes_filepath:str, filepath: str) -> None:
    """
    Generates and indexes the hash of the given file.
    """

    log(f'Indexing hash of: {filepath}')

    # index file hash in .txt
    file_hash = calculate_file_hash(filepath)
    with open(indexed_hashes_filepath, 'a', encoding='utf-8') as f:
        f.write(f'{file_hash}\n')

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
