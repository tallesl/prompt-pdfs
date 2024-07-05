"""
Shared configuration objects.
"""
from os import path
from typing import Any


chroma: Any = lambda: None
chroma.model = 'llama3'
chroma.collection_name = 'pdf_documents'
chroma.persist_directory = './chroma'
chroma.verification_query = 'Scrum'

documents: Any = lambda: None
documents.directory = path.expanduser('~/Downloads')
documents.extension = '.pdf'

indexed_hashes_filepath = './indexed_hashes.txt'

ollama: Any = lambda: None
ollama.base_url = 'http://localhost:11434'
ollama.model = 'llama3'
