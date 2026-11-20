
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.tools.custom_tools import calculator, search_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    streaming=True
)

# Tools
tools = [calculator, search_tool]
llm_with_tools = llm.bind_tools(tools)
