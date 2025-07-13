from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,function_tool,WebSearchTool
from agents.run import RunConfig
from dotenv import load_dotenv
from colorama import Fore, init
import requests
from bs4 import BeautifulSoup
from agents import function_tool
import os

init(autoreset=True)  # Automatically reset color after each print
load_dotenv()
KEY = os.getenv('KEY')

@function_tool
def web_search(query: str) -> str:
    """Free web search using DuckDuckGo (top 3 results)."""
    print(f"DEBUG: web_search called with query: {query}")
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://html.duckduckgo.com/html/?q={query}"
    res = requests.post(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for a in soup.find_all("a", class_="result__a", limit=3):
        title = a.get_text(strip=True)
        link = a["href"]
        results.append(f"{title} - {link}")

    return "\n".join(results) or "No results found."

def main():
    agent = Agent(
        name="Agent",
        instructions = 
        """
        You can search the web using the tool 'web_search' when you don't know the answer.
        Always use the tool before answering.
        Answer shortly based on the tool's results.
        """,
        tools=[web_search],
        model=OpenAIChatCompletionsModel(
            model='gemini-2.0-flash',
            openai_client=AsyncOpenAI(api_key=KEY, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
        )
    )
    conversation_history = []

    while True:
        user_input = input("Enter your input: ")
        conversation_history.append(f"User: {user_input}")
        # Combine conversation history for context
        context = "\n".join(conversation_history)
        run = Runner.run_sync(
            starting_agent=agent,
            input=context,
            run_config=RunConfig(tracing_disabled=True)
        )
        conversation_history.append(f"Assistant: {run.final_output}")
        print(Fore.GREEN + run.final_output)