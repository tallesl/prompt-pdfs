"""
Initializes OllamaEmbeddings and Chroma.
"""
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from .utilities import log


def initialize_chroma(chroma_configuration) -> Chroma:
    """
    Initializes OllamaEmbeddings and Chroma.
    """

    # initialize OllamaEmbeddings
    log(f'Initializing OllamaEmbeddings with model: {chroma_configuration.model}')
    embedding_function = OllamaEmbeddings(model=chroma_configuration.model)
    log('OllamaEmbeddings initialized.')

    # initialize Chroma
    log(f'Initializing Chroma on directory: {chroma_configuration.persist_directory}')
    c = Chroma(
        chroma_configuration.collection_name,
        embedding_function,
        chroma_configuration.persist_directory
    )
    log('ChromaDB initialized.')

    return c


def verify_chroma(chroma: Chroma, chroma_configuration) -> None:
    """
    Verifies ChromaDB content by the searching documents matching the given query.
    """
    log(f'Verifying ChromaDB content with query: {chroma_configuration.verification_query}')

    found_records = chroma.similarity_search(chroma_configuration.verification_query)

    if not found_records:
        log('No embeddings found for this query.')

    total_records = len(found_records)

    for i, record in enumerate(found_records):
        size = chroma_configuration.verification_preview_size
        preview = record.page_content[:size].replace('\n', ' ').strip()
        log(f'Record {i + 1} of {total_records} found: {preview}')
