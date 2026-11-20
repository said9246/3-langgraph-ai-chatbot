
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

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

    with st.chat_message("assistant"):

        def stream_response():

            for chunk, metadata in graph.stream(
                {"messages": [{"role": "user", "content": prompt}]},
                config=config,
                stream_mode="messages"
            ):

                # Only chatbot node response
                if metadata.get("langgraph_node") != "chatbot":
                    continue

                content = chunk.content

                if isinstance(content, str):
                    if content:
                        yield content

                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            if block.get("type") == "text":
                                yield block["text"]

        ai_response = st.write_stream(stream_response())

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })
