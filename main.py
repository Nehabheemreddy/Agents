# from src.tools.tools import web_search, web_scraping_tool

# output=web_scraping_tool.invoke("https://news.mit.edu/topic/artificial-intelligence2")
# print(output)

from src.pipeline.pipeline import run_research_pipeline

Topic="The impact of AI on the job market in 2026"
run_research_pipeline(Topic)