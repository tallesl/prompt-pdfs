"""
Manages storing and indexing file embeddings.
"""

# standard library imports
from typing import Iterable

# third-party imports
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# local imports
from ..configuration import chroma_configuration, ollama
from .utilities import log


def initialize_chroma() -> Chroma:
    """
    Initializes OllamaEmbeddings and Chroma.
    """

    # configuration values used in this function
    base_url: str = ollama.base_url  # pylint: disable=no-member
    model: str = ollama.model  # pylint: disable=no-member
    collection_name: str = chroma_configuration.collection_name  # pylint: disable=no-member
    persist_directory: str = chroma_configuration.persist_directory  # pylint: disable=no-member

    # initialize OllamaEmbeddings
    log(f'Initializing OllamaEmbeddings with model: {model}')
    embedding_function = OllamaEmbeddings(base_url=base_url, model=model)  # TODO bug
    log('OllamaEmbeddings initialized.')

    # initialize Chroma
    log(f'Initializing Chroma on directory: {persist_directory}')
    c = Chroma(collection_name, embedding_function, persist_directory)
    log('ChromaDB initialized.')

    return c


def verify_chroma(chroma: Chroma) -> None:
    """
    Verifies ChromaDB content by the searching documents matching the given query.
    """

    # configuration values used in this function
    verification_query: str = chroma_configuration.verification_query  # pylint: disable=no-member
    verification_preview_size: int = chroma_configuration.verification_preview_size  # pylint: disable=no-member

    # searching embeddings by the configured query
    log(f'Verifying ChromaDB content with query: {verification_query}')
    found_records = search_relevant_documents(chroma, verification_query)

    # if no embeddings were found for this query
    if not found_records:
        log('No embeddings found for this query.')
        return

    # previewing the found embeddings, if any
    total_records = len(found_records)
    for i, record in enumerate(found_records):
        preview = record.page_content[:verification_preview_size].replace('\n', ' ').strip()
        log(f'Record {i + 1} of {total_records} found: {preview}')


def index_embedding(chroma: Chroma, filepath: str) -> None:
    """
    Generates and indexes the embedding of the given file.
    """

    log(f'Indexing embeddings of: {filepath}')
    loader = PyMuPDFLoader(filepath)
    documents = loader.load()
    chroma.add_documents(documents)
    log('Embeddings indexed.')


def search_relevant_documents(chroma: Chroma, query: str) -> Iterable[Document]:
    """
    Retrieves relevant documents from ChromaDB for the given question.
    """

    return chroma.similarity_search(query)
