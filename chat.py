#! /usr/bin/env python3

"""
Prompts the PDF embeddings stored on ChromaDB using Ollama.
"""

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from _common import initialize_chroma, load_configuration, log


def initialize_llm() -> Ollama:
    """
    Initializes the LLM with Ollama.
    """
    return Ollama(base_url="http://localhost:11434", model="llama3")  # TODO move values to configuration


def create_prompt_template() -> PromptTemplate:
    """
    Creates a prompt template for the LLM.
    """
    return PromptTemplate(
        input_variables=["question", "context"],
        template="""
        You are a helpful assistant knowledgeable about the contents of the PDFs.
        Here is some context from the PDFs:
        {context}

        Q: {question}
        A:"""
    )


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
    # Load configuration object
    configuration = load_configuration()
    chroma_config = configuration['chroma']

    # Initialize ChromaDB
    chroma = initialize_chroma(chroma_config)

    # Initialize LLM and prompt template
    llm = initialize_llm()
    prompt_template = create_prompt_template()

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
