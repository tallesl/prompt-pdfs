#! /usr/bin/env python3

"""
Indexes on a ChromaDB database the embeddings of the files residing in the configured directory and
extension.
"""

# pylint: disable=redefined-outer-name

from functools import reduce
from hashlib import md5
from os import listdir, path
from signal import signal, SIGINT, SIGTERM
from sys import exit  # pylint: disable=redefined-builtin

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import Chroma

from _common import initialize_chroma, log
import _configuration as configuration

def set_signals() -> None:
    """
    Sets signal handlers for SIGINT and SIGTERM.
    """
    signal(SIGINT, lambda _, __: exit(0))
    signal(SIGTERM, lambda _, __: exit(0))


def calculate_file_hash(filepath: str) -> str:
    """
    Calculates the MD5 hash of the file at the given filepath.
    """
    if not path.exists(filepath):
        raise FileNotFoundError(f'File not found: {filepath}')

    hasher = md5()

    with open(filepath, 'rb') as file:
        buffer = file.read()
        hasher.update(buffer)

    return hasher.hexdigest()


def list_indexed_hashes(indexed_hashes_filepath: str) -> set[str]:
    """
    Lists the hashes of the indexed files in the given path.
    """

    log(f'Listing hashes in "{indexed_hashes_filepath}"...')
    if not path.exists(indexed_hashes_filepath):
        return set()

    with open(indexed_hashes_filepath, 'r', encoding='utf-8') as f:
        hashes = set(line.strip() for line in f)
        log(f'{len(hashes)} hashes listed.')
        return hashes


def list_non_indexed_files(indexed_hashes: set[str], documents_configuration) -> set[str]:
    """
    Lists the non-indexed files in the configured directory with the configured extension.
    """

    log(f'Listing non-indexed ("{documents_configuration.extension}" from "{documents_configuration.directory}")...')

    all_files = listdir(documents_configuration.directory)
    selected_filenames = [f for f in all_files if f.endswith(documents_configuration.extension)]
    selected_filepaths = [path.join(documents_configuration.directory, f) for f in selected_filenames]

    selected_files_hashes = {f: calculate_file_hash(f) for f in selected_filepaths}

    non_indexed_hashes = {f: h for f, h in selected_files_hashes.items() if h not in indexed_hashes}
    non_indexed_files = non_indexed_hashes.keys()
    sorted_files = sorted(non_indexed_files)

    concatenated_filepaths = reduce(
        lambda f, concatenated: f'{f}\n\t{concatenated}' if concatenated else f,
        sorted_files,
        ''
    )

    printable_filepaths = concatenated_filepaths if concatenated_filepaths else " (none)"

    log(f'New files to be indexed:{printable_filepaths}')

    return set(sorted_files)


def index_file(chroma: Chroma, indexed_hashes_filepath: str, filepath: str) -> None:
    """
    Generates and indexes the embeddings of the given file.
    """

    log(f'Indexing file embeddings ("{filepath}")...')

    # index file embeddings in Chroma
    loader = PyMuPDFLoader(filepath)
    documents = loader.load()
    chroma.add_documents(documents)

    # index file hash in .txt
    file_hash = calculate_file_hash(filepath)
    with open(indexed_hashes_filepath, 'a', encoding='utf-8') as f:
        f.write(file_hash + '\n')

    log('Embeddings indexed.')


def index_hash(indexed_hashes_filepath: str, filepath: str) -> None:
    """
    Generates and indexes the hash of the given file.
    """

    log(f'Indexing file hash ("{filepath}")...')

    # index file hash in .txt
    file_hash = calculate_file_hash(filepath)
    with open(indexed_hashes_filepath, 'a', encoding='utf-8') as f:
        f.write(file_hash + '\n')

    log('Hash indexed.')


def verify_chroma(chroma: Chroma, chroma_configuration) -> None:
    """
    Verifies ChromaDB content by the searching documents matching the given query.
    """
    log(f'Verifying ChromaDB content ("{chroma_configuration.verification_query}" query)...')

    found_records = chroma.similarity_search(chroma_configuration.verification_query)

    if not found_records:
        log('No embeddings found for the configured verification query.')

    total_records = len(found_records)
    for i, record in enumerate(found_records):
        log(f'Record {i + 1} of {total_records} found: {record.page_content[:200]}...')  # TODO change to 100, move preview size to config, trim and remove new lines before printing


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
        index_file(chroma, configuration.indexed_hashes_filepath, f)

    log('Finished.')
