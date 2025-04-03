import json
import os

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("docs")

USER_AGENT = "docs-app/1.0"
SERPER_URL = "https://google.serper.dev/search"

doc_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
}

async def search_web(query: str) -> dict | None:
    payload = json.dumps({"q": query, "num": 2})

    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_URL, headers=headers, data=payload, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {"organic": []}

async def fetch_url(url: str):
  """
  Returns the docs/text from the webpage
  """
  async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return text
        except httpx.TimeoutException:
            return "Timeout error"

@mcp.tool()
async def get_docs(query: str, library: str):
    """
    Search the docs for a given query and library.
    Supports the following libraries:
    - langchain
    - llama-index
    - openai

    Args:
        query (str): The query to search for (e.g. "Chroma DB")
        library (str): The library to search from (e.g. "langchain")

    Returns:
        str: The docs/Text for the given query from the library.
    """
    if library not in doc_urls:
        return ValueError(f"Library {library} not supported by this tool")

    query = f"site:{doc_urls[library]} {query}"
    results = await search_web(query)
    if results is None or len(results["organic"]) == 0:
        return "No results found"
    
    text = ""
    for result in results["organic"]:
        text += await fetch_url(result["link"])
    return text

if __name__ == "__main__":
    mcp.run(transport="stdio")
