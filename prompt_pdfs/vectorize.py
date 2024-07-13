#! /usr/bin/env python3

"""
Indexes on a ChromaDB database the embeddings of the files residing in the configured directory and
extension.
"""

# local imports
from . import configuration
from ._internals.hash_store import filter_indexed_files, store_hash
from ._internals.utilities import get_printable_list, log, set_signals, list_files_with_extension
from ._internals.vector_store import initialize_chroma, verify_chroma, index_embedding


def vectorize() -> None:
    """
    Indexes on a ChromaDB database the embeddings of the files residing in the configured directory and extension.
    """

    # configuration values used in this function
    extension: str = configuration.documents.extension  # pylint: disable=no-member
    directory: str = configuration.documents.directory  # pylint: disable=no-member

    # set process signals
    set_signals()

    # initializing and verifying ChromaDB
    chroma = initialize_chroma()
    verify_chroma(chroma)

    # listing new files to be indexed
    log(f'Listing non-indexed {extension} from: {directory}')

    source_filepaths = list_files_with_extension(directory, extension)
    non_indexed_files = filter_indexed_files(source_filepaths)
    printable_filepaths = get_printable_list(non_indexed_files.keys())

    log(f'New files to be indexed:{printable_filepaths}')

    # indexing both embeddings and hash for each file
    for filepath, filehash in non_indexed_files.items():
        index_embedding(chroma, filepath)
        store_hash(filehash)


if __name__ == '__main__':
    vectorize()
