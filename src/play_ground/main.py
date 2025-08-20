from urllib import response
from agents import (
    Agent,
    Runner,
    function_tool,
    set_tracing_export_api_key,
    trace,
)
from tavily import TavilyClient
from .config import model_config
from dotenv import load_dotenv
from colorama import Fore, init
import requests
from bs4 import BeautifulSoup
import os

init(autoreset=True)  # Automatically reset color after each print
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
Tracing_key = os.getenv("Tracing_key")
tavily_client = TavilyClient(api_key=os.getenv("Tavily_API_KEY"))

@function_tool
def duckduckgo_search(query: str) -> str:
    """Free web search using DuckDuckGo (top 3 results)."""
    print(Fore.GREEN + f">>>: duckduckgo_search called with query: {query}")
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://html.duckduckgo.com/html/?q={query}"
    res = requests.post(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for a in soup.find_all("a", class_="result__a", limit=3):
        title = a.get_text(strip=True)
        link = a["href"]
        results.append(Fore.MAGENTA + f"{title} - {link}")

    return "\n".join(results) or "No results found."

@function_tool
def tavily_search(query: str) -> str:
    """Web search using Tavily."""
    print(Fore.YELLOW + f">>>: tavily_search called with query: {query}")
    response = tavily_client.search(query)

    results = []
    for r in response.get("results", []):
        title = r.get("title", "No title")
        url = r.get("url", "No URL")
        results.append(Fore.CYAN+f"{title} - {url}")

    return "\n".join(results) or "No results found."


agent = Agent(
    name="Agent",
    instructions="""
    You can search the web using the tool 'duckduckgo_search' when you don't know the answer.
    Always use the tool before answering.
    Answer shortly based on the tool's results.
    """,
    tools=[tavily_search],
    # tool_use_behavior="stop_on_first_tool",
    model=model_config,
)


def main():
    set_tracing_export_api_key(Tracing_key)
    with trace(workflow_name="WebSearch", disabled=False):

        conversation_history = []

        while True:
            user_input = input("Enter your input: ")
            if user_input.lower() == 'off':
                break
            conversation_history.append(f"User: {user_input}")
            # Combine conversation history for context
            context = "\n".join(conversation_history)
            run = Runner.run_sync(
                starting_agent=agent,
                input=context,
                # run_config=RunConfig(tracing_disabled=True)
            )
            conversation_history.append(f"Assistant: {run.final_output}")
            print(run.final_output)
