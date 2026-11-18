
import os
from app.rag.rag_service import initialize_rag
from app.llm.model import llm


pdf_path = "data/mydata.pdf"


rag_chain = initialize_rag(pdf_path)


def rag_node(state):
    messages = state["messages"]

    question = messages[-1].content

    history = "\n".join(
        f"{message.type}: {message.content}"
        for message in messages[:-1]
    )

    prompt = f"""
    Convert the user's latest question into a standalone question.

    Previous conversation:
    {history}

    Latest question:
    {question}

    Return only the standalone question.
    """

    response = llm.invoke(prompt)
    standalone_question = response.text.strip()

    response = rag_chain({
        "question": standalone_question
    })

    return {"messages": [response]}
