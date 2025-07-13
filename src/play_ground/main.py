from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,function_tool
from agents.run import RunConfig
from dotenv import load_dotenv
from colorama import Fore, init
init(autoreset=True)  # Automatically reset color after each print
import os
load_dotenv()
KEY = os.getenv('KEY')

@function_tool
def fun():
    "this is a tool"
    pass

def main():
    agent = Agent(
        name="Test Agent",
        instructions='You are a liar. Whenever someone asks a question, you always reply with wrong answers—you always lie. ',
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
