# Prompt PDFs

Yet another LangChain example of prompting PDF file embeddings with a LLM. Everything is performed
local, no external APIs are made.

## Setup

First, make sure to check [_configuration.py](src/configuration.py) before starting, specifically the
directory configuration from where the application will read the PDF files. Note that all
configuration values comes from this file, there are no support for CLI arguments at the moment.

Then, create a new virtual environment and install required packages with pip:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Lastly, make sure you have [Ollama](https://ollama.com/) running ("http://localhost:11434/" by
default).

## Indexing PDFs

To list PDF files from the configured folder, generate and index its embeddings (ChromaDB):

```sh
$ python3 -m prompt_pdfs.vectorize
```

This will generate a folder with the embeddings ("chroma/" by default) and a file with a hash for
each found file ("indexed_hashes.txt" by default).

## Prompting Indexed PDFs

The start a chat with the LLM with the embeddings available:

```sh
$ python3 -m prompt_pdfs.chat
```

## Contributing

Make sure to run [pylint](https://pylint.org) and [mypy](https://mypy-lang.org) on before submitting a pull request and
consider writing an unit test for the change.

Some convenient command recipes are provided through a [justfile](justfile) (see
[just](https://just.systems) command runner):
- `just venv`: generates a new virtual environment with needed packages
- `just tree`: list the files of the repository as a tree
- `just pylint`: lints main and unit tests modules
- `just mypy`: type-checks for main module
- `just pytest`: run tests
- `just vectorize`: runs script that indexes PDFs
- `just chat`: runs script that prompts indexed PDFs
- `just clean`: removes indexed PDFs and starts fresh

## TODO

- Support [FAISS](https://python.langchain.com/v0.2/docs/integrations/vectorstores/faiss/) vector
  store
- Support other [PDF loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf/)
- Support other [LLM integrations](https://python.langchain.com/docs/integrations/llms/)
- Unit tests
