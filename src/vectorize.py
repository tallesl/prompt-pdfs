#! /usr/bin/env python3

"""
Indexes on a ChromaDB database the embeddings of the files residing in the configured directory and
extension.
"""

# pylint: disable=redefined-outer-name

from functools import reduce
from os import listdir, path

from _internals.vector_store import initialize_chroma, verify_chroma, index_embedding
from _internals.hash_store import list_indexed_hashes, index_hash, calculate_file_hash
from _internals.utilities import log, set_signals, list_files_with_extension
import configuration


def list_non_indexed_files(indexed_hashes: set[str], documents_configuration) -> set[str]:
    """
    Lists the non-indexed files in the configured directory with the configured extension.
    """

    log(
        f'Listing non-indexed {documents_configuration.extension} '
        f'from: {documents_configuration.directory}'
    )

    selected_filepaths = list_files_with_extension(
        documents_configuration.directory, documents_configuration.extension
    )

    selected_files_hashes = {
        f: calculate_file_hash(f)
        for f in selected_filepaths
    }

    non_indexed_hashes = {
        f: h
        for f, h in selected_files_hashes.items()
        if h not in indexed_hashes
    }

    non_indexed_files = non_indexed_hashes.keys()

    sorted_files = sorted(non_indexed_files)

    concatenated_filepaths = reduce(
        lambda f, concatenated:
            f'{f}\n\t{concatenated}' if concatenated else f,
        sorted_files,
        ''
    )

    printable_filepaths = concatenated_filepaths if concatenated_filepaths else " (none)"

    log(f'New files to be indexed:{printable_filepaths}')

    return set(sorted_files)


if __name__ == '__main__':
    # set process signals
    set_signals()

    # initializing and verifying ChromaDB
    chroma = initialize_chroma(configuration.chroma)
    verify_chroma(chroma, configuration.chroma)

    # listing new files to be indexed
    indexed_hashes = list_indexed_hashes(configuration.indexed_hashes_filepath)
    non_indexed_files = list_non_indexed_files(indexed_hashes, configuration.documents)

    # indexing files
    for f in non_indexed_files:
        index_hash(configuration.indexed_hashes_filepath, f)
        index_embedding(chroma, f)
