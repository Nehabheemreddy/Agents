from rich import print
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # Step 1: Search Agent
    print("\n[bold blue]Step 1: Search Agent is working...[/bold blue]")
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
    )
    state["search_results"] = search_result["messages"][-1].text
    print(state["search_results"])

    # Step 2: Reader Agent
    print("\n[bold blue]Step 2: Reader Agent is scraping top resources...[/bold blue]")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {"messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URLs and scrape them for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:3000]}"
        )]}
    )
    state["scraped_content"] = reader_result["messages"][-1].text
    print(state["scraped_content"])

    # Step 3: Writer Chain
    print("\n[bold blue]Step 3: Writer is drafting the report...[/bold blue]")
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke(
        {"topic": topic, "research": research_combined}
    ).text
    print(state["report"])

    # Step 4: Critic Chain
    print("\n[bold blue]Step 4: Critic is reviewing the report...[/bold blue]")
    state["feedback"] = critic_chain.invoke({"report": state["report"]}).text
    print(state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)