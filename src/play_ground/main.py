from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv
from colorama import Fore, init
init(autoreset=True) # Automatically reset color after each print
import os
load_dotenv()
KEY = os.getenv('KEY')
def main():
    while True:
        agent = Agent(name="Test Agent",instructions='You are a liar whenever someone ask a question u have to reply wrong answers always tell lie ',model= OpenAIChatCompletionsModel(model='gemini-2.0-flash',openai_client=AsyncOpenAI(api_key=KEY,base_url='https://generativelanguage.googleapis.com/v1beta/openai/')))
        run = Runner.run_sync(starting_agent=agent, input=input("Enter your input: "),run_config=RunConfig(tracing_disabled=True))
        print(Fore.GREEN + run.final_output)
    