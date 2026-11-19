
import streamlit as st
from app.graph.workflow import graph

st.title("🤖 AI Chatbot")

st.write("Welcome to my LangGraph AI Chatbot!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    config = {
        "configurable": {
            "thread_id": "streamlit_chat"
        }
    }

    response = graph.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config=config
    )

    content = response["messages"][-1].content

    if isinstance(content, list):
        ai_response = "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    else:
        ai_response = content

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    with st.chat_message("assistant"):
        st.write(ai_response)
