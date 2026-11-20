
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver

from app.llm.model import llm, llm_with_tools
from app.graph.rag_node import rag_node
from app.tools.tool_node import tool_node


def router(state: MessagesState):
    messages = state["messages"][-6:]

    conversation = "\n".join(
        f"{message.type}: {message.content}"
        for message in messages
    )

    prompt = f"""
    You are a routing classifier.

    Decide whether the user needs information from uploaded documents.

    Return RAG when:
    - User mentions PDF, document, file, or uploaded content.
    - User asks about information contained in uploaded documents.
    - User asks questions like "According to my PDF..."
    - User asks a follow-up about previously discussed PDF content.
    - User uses references like "it", "its", or "that" related to PDF content.

    Return CHAT when:
    - User asks a general question unrelated to uploaded documents.
    - User starts a normal conversation.

    Conversation:
    {conversation}

    Return only CHAT or RAG.
    """

    response = llm.invoke(prompt)

    decision = str(response.content).strip().upper()

    return "rag" if "RAG" in decision else "chatbot"


def chatbot(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def tools_router(state: MessagesState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)
builder.add_node("rag", rag_node)
builder.add_node("tools", tool_node)

builder.add_conditional_edges(
    START,
    router,
    {
        "rag": "rag",
        "chatbot": "chatbot"
    }
)

builder.add_conditional_edges(
    "chatbot",
    tools_router,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge("tools", "chatbot")
builder.add_edge("rag", END)

memory = InMemorySaver()

graph = builder.compile(checkpointer=memory)
