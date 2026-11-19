from langchain.tools import tool
from ddgs import DDGS

# calculator tools 

@tool
def calculator(expression: str) -> str:
    """Perform mathematical calculations."""
    return str(eval(expression))


# Search tools 

@tool
def search_tool(query: str) -> str:
    """Search the internet for information."""
    results = DDGS().text(query, max_results=5)
    return str(results)



