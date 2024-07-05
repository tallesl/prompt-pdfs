"""
Initializes OllamaEmbeddings and Chroma.
"""
from datetime import datetime
from typing import Callable

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


def log(message: str) -> None:
    """
    Prints the given message with the current time.
    """
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}')


def initialize_chroma(chroma_configuration: Callable) -> Chroma:
    """
    Initializes OllamaEmbeddings and Chroma.
    """

    # initialize OllamaEmbeddings
    log(f'Initializing OllamaEmbeddings ("{chroma_configuration.model}" model)...')
    embedding_function = OllamaEmbeddings(model=chroma_configuration.model)
    log('OllamaEmbeddings initialized.')

    # initialize Chroma
    log(f'Initializing Chroma ("{chroma_configuration.persist_directory}" filepath)...')
    c = Chroma(
        chroma_configuration.collection_name,
        embedding_function,
        chroma_configuration.persist_directory
    )
    log('ChromaDB initialized.')

    return c
