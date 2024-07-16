#! /usr/bin/env python3

"""
Prompts the PDF embeddings stored on ChromaDB using Ollama.
"""

# standard library imports
from typing import Any, Iterable

# third-party imports
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_core.documents import Document
from langchain_core.runnables.base import RunnableSerializable

# local imports
from . import configuration
from ._internals.utilities import log, set_signals
from ._internals.vector_store import initialize_chroma, search_relevant_documents


def chat() -> None:
    """
    Initiates a prompt between the user and the LLM augmented by previously indexed file embeddings.
    """

    # configuration values used in this function
    input_variables: list[str] = configuration.prompt.input_variables  # pylint: disable=no-member
    template: str = configuration.prompt.template  # pylint: disable=no-member
    base_url: str= configuration.ollama.base_url  # pylint: disable=no-member
    model: str= configuration.ollama.model  # pylint: disable=no-member

    # set process signals
    set_signals()

    # setting up prompt template object
    prompt_template = PromptTemplate(
        input_variables=input_variables,
        template=template
    )

    # initializing Ollama
    ollama = Ollama(base_url=base_url, model=model)

    # setting up a chain of prompt + LLM
    chain = prompt_template | ollama

    # initializing ChromaDB
    chroma = initialize_chroma()

    # chat loop
    while True:
        try:
            print('\n--------------------\n')

            log('Ask a question: ', '')
            question = input()
            print()

            if question.lower() in ['quit', 'q', 'exit']:
                break

            relevant_documents = search_relevant_documents(chroma, question)

            log(f'Found {len(relevant_documents)} relevant documents.\n')

            answer = invoke_question(chain, relevant_documents, question)

            log(f'Answer: {answer}')

        except EOFError:
            break


def invoke_question(
    chain: RunnableSerializable[dict[Any, Any], str],
    relevant_documents: Iterable[Document],
    question: str) -> str:
    """
    Chats with the PDFs using the LLM chain and returns the answer.
    """

    context = "\n".join([doc.page_content[:200] for doc in relevant_documents])

    if not context.strip():
        return str(chain.invoke({"question": question, "context": ''}))

    return str(chain.invoke({"question": question, "context": context}))


if __name__ == '__main__':
    chat()
