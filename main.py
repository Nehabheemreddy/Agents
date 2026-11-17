from src.tools.tools import web_search, web_scraping_tool

output=web_scraping_tool.invoke("https://news.mit.edu/topic/artificial-intelligence2")
print(output)