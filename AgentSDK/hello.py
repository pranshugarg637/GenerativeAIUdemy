from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()
agent = Agent(
    name="Hello World Agent",
    instructions="You are an agent that greets user and helps them answer their questions using emojis and in a funny way",
    model="gpt-5.6",
)

result=Runner.run_sync(agent,"Hey There my name is Pranshu Garg") #user question
print(result.final_output)
