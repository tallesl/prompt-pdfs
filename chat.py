#! /usr/bin/env python3

"""
Prompts the PDF embeddings stored on ChromaDB using Ollama.
"""

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from _common import initialize_chroma, log, set_signals
import _configuration as configuration


def initialize_ollama(ollama_configuration) -> Ollama:
    """
    Initializes Ollama LLM.
    """
    return Ollama(base_url=ollama_configuration.base_url, model=ollama_configuration.model)

def create_llm_chain(llm: Ollama, prompt_template: PromptTemplate) -> LLMChain:
    """
    Creates the LLM chain with the given LLM and prompt template.
    """
    return prompt_template | llm
    return LLMChain(llm=llm, prompt=prompt_template)


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

    # Initialize ChromaDB
    chroma = initialize_chroma(configuration.chroma)

    # Initialize LLM and prompt template
    llm = initialize_ollama(configuration.ollama)
    prompt_template = PromptTemplate(
        input_variables=configuration.prompt.input_variables,
        template=configuration.prompt.template
    )

    # Create LLM chain
    chain = create_llm_chain(llm, prompt_template)  # TODO discard chain?

    # Chat loop
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
