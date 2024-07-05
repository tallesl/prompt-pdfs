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

indexed_hashes_filepath = './indexed_hashes.txt'

documents: Any = lambda: None
documents.directory = path.expanduser('~/Downloads')
documents.extension = '.pdf'
