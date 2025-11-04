from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return summary results."""
    search = DuckDuckGoSearchRun()
    return search.run(query)
