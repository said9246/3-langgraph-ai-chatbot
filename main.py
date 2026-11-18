

from langchain_core.messages import HumanMessage
from app.graph.workflow import graph

config = {
    "configurable": {
        "thread_id": "conversation-1"
    }
}

print("AI Chatbot Started!")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot stopped.")
        break

    response = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=config
    )

    print("AI:", response["messages"][-1].text)