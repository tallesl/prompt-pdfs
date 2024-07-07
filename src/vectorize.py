#! /usr/bin/env python3

"""
Indexes on a ChromaDB database the embeddings of the files residing in the configured directory and
extension.
"""

from typing import Any

from _internals.vector_store import initialize_chroma, verify_chroma, index_embedding
from _internals.hash_store import filter_indexed_files, store_hash
from _internals.utilities import get_printable_list, log, set_signals, list_files_with_extension
import configuration


def vectorize() -> None:
    """
    Indexes on a ChromaDB database the embeddings of the files residing in the configured directory and extension.
    """

    # configuration values used in this function
    chroma_configuration: Any = configuration.chroma
    extension: str = configuration.documents.extension  # pylint: disable=no-member
    directory: str = configuration.documents.directory  # pylint: disable=no-member
    indexed_hashes_filepath = configuration.indexed_hashes_filepath

    # set process signals
    set_signals()

    # initializing and verifying ChromaDB
    chroma = initialize_chroma(chroma_configuration)
    verify_chroma(chroma, chroma_configuration)

    # listing new files to be indexed
    log(f'Listing non-indexed {extension} from: {directory}')

    source_filepaths = list_files_with_extension(directory, extension)
    non_indexed_files = filter_indexed_files(indexed_hashes_filepath, source_filepaths)
    printable_filepaths = get_printable_list(non_indexed_files.keys())

    log(f'New files to be indexed:{printable_filepaths}')

    # indexing both embeddings and hash for each file
    for filepath, filehash in non_indexed_files.items():
        index_embedding(chroma, filepath)
        store_hash(indexed_hashes_filepath, filehash)


if __name__ == '__main__':
    vectorize()
