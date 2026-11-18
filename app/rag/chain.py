from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_template("""
Answer the question using the provided context.

Context:
{context}

Question:
{question}

If the answer is not available in the context,
say: I don't know based on the provided documents.
""")

from app.llm.model import llm

def create_rag_chain(retriever):
    def rag_response(inputs):
        documents = retriever.invoke(inputs["question"])

        context = "\n\n".join(
            doc.page_content for doc in documents
        )

        prompt = rag_prompt.invoke({
            "context": context,
            "question": inputs["question"]
        })

        return llm.invoke(prompt)

    return rag_response