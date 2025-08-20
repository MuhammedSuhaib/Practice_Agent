import os
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("Tavily_API_KEY"))
response = tavily_client.search("fastest Growing Religion")
print(response["results"][0]["content"])
print('.~.'*50,)
for r in response["results"]:
    print(r["content"], "\n")
