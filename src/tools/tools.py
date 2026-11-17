from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
# from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
import trafilatura
import re

load_dotenv()


tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str):
    "Search the web for the topic"
    results = tavily.search(query=query, max_results=4)
    out=[]

    for r in results['results']:
        out.append(
            f"Title:{r['title']}\n URL:{r['url']}\n snippet:{r['content'][:300]}\n"
        )

    return "\n---\n".join(out)


@tool
def web_scraping_tool(url: str) -> str:
    """Fetch a web page from a URL and return its readable text."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers, timeout=10).text
        text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
        return text[:5000]
    except Exception as e:
        return f"Could not read {url}: {e}"