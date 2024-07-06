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
