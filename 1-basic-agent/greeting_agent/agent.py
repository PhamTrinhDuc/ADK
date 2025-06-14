from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent

LLM_MODEL = "openai/gpt-4o-mini"
model = LiteLlm(model=LLM_MODEL)

root_agent = Agent(
  name="greeting_agent", # This is the name of the agent. Match the name of folder. It should start with a letter (a-z, A-Z) or an underscore (_), and can only contain letters, digits (0-9), and underscores
  model=model, 
  description="A simple agent that greets the user.",
  instruction="You are a friendly agent that greets the user warmly.",
)