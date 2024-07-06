#! /usr/bin/env python3

"""
Prompts the PDF embeddings stored on ChromaDB using Ollama.
"""

from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.chains import LLMChain

from _internals.vector_store import initialize_chroma
from _internals.utilities import log, set_signals
import configuration


def search_relevant_documents(chroma: Chroma, question: str) -> list:
    """
    Retrieves relevant documents from ChromaDB for the given question.
    """
    return chroma.similarity_search(question)


def invoke_question(chain: LLMChain, relevant_documents: list[Document], question: str) -> str:
    """
    Chats with the PDFs using the LLM chain and returns the answer.
    """
    context = "\n".join([doc.page_content[:200] for doc in relevant_documents])

    if not context.strip():
        return chain.invoke({"question": question, "context": ''})

    return chain.invoke({"question": question, "context": context})


if __name__ == '__main__':
    # set process signals
    set_signals()

    # setting up prompt template object
    prompt_template = PromptTemplate(
        input_variables=configuration.prompt.input_variables,
        template=configuration.prompt.template
    )

    # initializing Ollama
    ollama = Ollama(base_url=configuration.ollama.base_url, model=configuration.ollama.model)

    # setting up a chain of prompt + LLM
    chain = prompt_template | ollama

    # initializing ChromaDB
    chroma = initialize_chroma(configuration.chroma)

    # chat loop
    while True:
        try:
            log('Ask a question: ', '')
            question = input()

            if question.lower() in ['quit', 'q', 'exit']:
                break

            relevant_documents = search_relevant_documents(chroma, question)
            answer = invoke_question(chain, relevant_documents, question)

            log(f'Answer: {answer}')

        except EOFError:
            break
