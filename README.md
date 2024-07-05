# Prompt PDFs

Yet another LangChain example of prompting PDF file embeddings with a LLM. Everything is performed
local, no external APIs are made.

## Setup

First, make sure to check [_configuration.py](_configuration.py) before starting, specifically the
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

## Generating and Saving Vector Embeddings

To list PDF files from the configured folder, generate and index its embeddings (ChromaDB):

```sh
$ python3 vectorize.py
```

This will generate a folder with the embeddings ("chroma/" by default) and a file with a hash for
each found file ("indexed_hashes.txt" by default).

## Prompting Previously Generated Embeddings

The start a chat with the LLM with the embeddings available:

```sh
$ python3 chat.py
```

## Contributing

Make sure to run [pylint](https://pyling.org) and [mypy](https://mypy-lang.org) on the files before
submitting a pull request. Some convenient command recipes are provided through a
[justfile](justfile) (see [just](https://just.systems) command runner).

## TODO

- Support [FAISS](https://python.langchain.com/v0.2/docs/integrations/vectorstores/faiss/) vector
  store
- Support other [PDF loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf/)
- Support other [LLM integrations](https://python.langchain.com/docs/integrations/llms/)
- Unit tests
