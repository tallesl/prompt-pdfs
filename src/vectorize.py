#! /usr/bin/env python3

"""
Indexes on a ChromaDB database the embeddings of the files residing in the configured directory and
extension.
"""

# pylint: disable=redefined-outer-name

from functools import reduce

from _internals.vector_store import initialize_chroma, verify_chroma, index_embedding
from _internals.hash_store import list_indexed_hashes, index_hash, calculate_file_hash
from _internals.utilities import log, set_signals, list_files_with_extension
import configuration


def vectorize() -> None:
    """
    Indexes on a ChromaDB database the embeddings of the files residing in the configured directory
    and extension.
    """
    # set process signals
    set_signals()

    # initializing and verifying ChromaDB
    chroma = initialize_chroma(configuration.chroma)
    verify_chroma(chroma, configuration.chroma)

    # listing new files to be indexed
    extension: str = configuration.documents.extension
    log(
        f'Listing non-indexed {extension} '
        f'from: {configuration.documents.directory}'
    )

    indexed_hashes = list_indexed_hashes(configuration.indexed_hashes_filepath)
    source_filepaths = list_files_with_extension(
        configuration.documents.directory, extension
    )
    non_indexed_filepaths = list_non_indexed_files(indexed_hashes, source_filepaths)
    printable_filepaths = get_printable_file_list(non_indexed_filepaths)

    log(f'New files to be indexed:{printable_filepaths}')

    # indexing both embeddings and hash for each file
    for f in non_indexed_filepaths:
        index_embedding(chroma, f)
        index_hash(configuration.indexed_hashes_filepath, f)


def list_non_indexed_files(indexed_hashes: set[str], source_filepaths: list[str]) -> set[str]:
    """
    Lists from the given source files the ones that are not in the given indexed hashes.
    """

    source_files_hashes = {
        f: calculate_file_hash(f)
        for f in source_filepaths
    }

    non_indexed_hashes = {
        f: h
        for f, h in source_files_hashes.items()
        if h not in indexed_hashes
    }

    non_indexed_files = non_indexed_hashes.keys()

    return set(non_indexed_files)


def get_printable_file_list(filepaths: set[str]) -> str:
    """
    Returns a printable list of the given filepaths.
    """
    sorted_files = sorted(filepaths)

    concatenated_filepaths = reduce(
        lambda f, concatenated:
        f'{f}\n\t{concatenated}' if concatenated else f,
        sorted_files,
        ''
    )

    printable_filepaths = concatenated_filepaths if concatenated_filepaths else " (none)"

    return printable_filepaths


if __name__ == '__main__':
    vectorize()
