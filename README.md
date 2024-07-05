# Prompt PDFs

Yet another LangChain example of prompting PDF files embeddings with a LLM.

## Configuration

No CLI arguments are parsed, all configuration values resides on [_configuration.py](_configuration.py).

## Building and Running

Simply create a new virtual environment and install requirements with pip:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Searching for PDF files, generating and indexing embeddings (with ChromaDB):

```sh
$ python3 vectorize.py
```

Prompting the embeddings with an LLM (with Ollama):

```sh
$ python3 chat.py
```
