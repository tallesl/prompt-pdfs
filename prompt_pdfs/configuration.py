"""
Application-wide configuration values.
"""

# standard library imports
from os import path
from typing import Any


chroma_configuration: Any = lambda: None
chroma_configuration.collection_name = 'pdf_documents'
chroma_configuration.persist_directory = './chroma'
chroma_configuration.verification_query = 'Scrum'
chroma_configuration.verification_preview_size = 100

documents: Any = lambda: None
documents.directory = path.expanduser('~/Downloads')
documents.extension = '.pdf'

hash_indexing: Any = lambda: None
hash_indexing.filepath = './indexed_hashes.txt'
hash_indexing.algorithm = 'md5'

ollama: Any = lambda: None
ollama.base_url = 'http://localhost:11434'
ollama.model = 'llama3'

prompt: Any = lambda: None
prompt.input_variables = ['question', 'context']
prompt.template = """
    You are a helpful assistant knowledgeable about the contents of the PDFs.
    Here is some context from the PDFs:
    {context}

    Q: {question}
    A:
"""
