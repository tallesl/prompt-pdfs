"""
Manages storing and indexing file embeddings.
"""

from typing import Any, Iterable

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from .utilities import log


def initialize_chroma(chroma_configuration: Any) -> Chroma:
    """
    Initializes OllamaEmbeddings and Chroma.
    """

    model: str = chroma_configuration.model
    collection_name: str = chroma_configuration.collection_name
    persist_directory: str = chroma_configuration.persist_directory

    # initialize OllamaEmbeddings
    log(f'Initializing OllamaEmbeddings with model: {model}')
    embedding_function = OllamaEmbeddings(model=model)
    log('OllamaEmbeddings initialized.')

    # initialize Chroma
    log(f'Initializing Chroma on directory: {persist_directory}')
    c = Chroma(collection_name, embedding_function, persist_directory)
    log('ChromaDB initialized.')

    return c


def verify_chroma(chroma: Chroma, chroma_configuration: Any) -> None:
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
