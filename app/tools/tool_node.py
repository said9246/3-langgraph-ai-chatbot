from langgraph.prebuilt import ToolNode
from app.tools.custom_tools import calculator, search_tool

tools = [calculator, search_tool]

tool_node = ToolNode(tools) 