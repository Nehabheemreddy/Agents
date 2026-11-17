from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools.tools import web_search, web_scraping_tool

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",  # fast and reliable right now
    max_retries=3,   # retry if Google says "high demand" (503)
    timeout=120,     # give up on a single call after 120 seconds
)


def build_search_agent():
    return create_agent(
        llm,
        tools=[web_search],
        system_prompt=(
            "You are a search assistant. ALWAYS use the web_search tool; never answer from memory. "
            "Return ONLY a list of the results, each with: Title, URL, and a one-line summary. "
            "Do not write an essay."
        ),
    )


def build_reader_agent():
    return create_agent(
        llm,
        tools=[web_scraping_tool],
        system_prompt=(
            "You are a reader. Pick the 2-3 most relevant URLs and call web_scraping_tool on each. "
            "For each page, return its URL followed by the key facts, numbers and quotes from it. "
            "Only use information from the scraped pages."
        ),
    )


writer_chain = ChatPromptTemplate.from_template(
    """You are an expert research writer.
Using ONLY the research below, write a detailed report on: {topic}

Structure:
# Title
## Introduction
## Key Findings
## Conclusion
## Sources (list the URLs)

Research:
{research}"""
) | llm


critic_chain = ChatPromptTemplate.from_template(
    """You are a strict reviewer. Review the report below.

Reply in this format:
Score: X/10
Strengths:
Weaknesses:
Suggestions:

Report:
{report}"""
) | llm
