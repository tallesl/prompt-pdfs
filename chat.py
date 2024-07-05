#! /usr/bin/env python3

"""
Prompts the PDF embeddings stored on ChromaDB using Ollama.
"""

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from _common import initialize_chroma, log, set_signals
import _configuration as configuration


def get_relevant_documents(question: str) -> list:
    """
    Retrieves relevant documents from ChromaDB for the given question.
    """
    return chroma.similarity_search(question)


def chat_with_pdfs(question: str) -> str:
    """
    Chats with the PDFs using the LLM chain and returns the answer.
    """
    relevant_docs = get_relevant_documents(question)
    context = "\n".join([doc.page_content[:200] for doc in relevant_docs])

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
            question = input("Ask a question (or type 'exit' to quit): ")
            if question.lower() == 'exit':
                break

            answer = chat_with_pdfs(question)
            log(f"Answer: {answer}")

        except KeyboardInterrupt: # TODO colocar sinal no common
            log("Graceful shutdown initiated.")
            break

    log('Finished.')
