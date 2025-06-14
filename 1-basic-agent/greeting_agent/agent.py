from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

LLM_MODEL = "openai/gpt-4o-mini"
GEMINI_MODEL = "gemini-2.0-flash-lite"  

model = LiteLlm(model=LLM_MODEL)

root_agent = Agent(
  name="greeting_agent", # This is the name of the agent. Match the name of folder. It should start with a letter (a-z, A-Z) or an underscore (_), and can only contain letters, digits (0-9), and underscores
  model=GEMINI_MODEL, 
  description="A simple agent that greets the user.",
  instruction="You are a friendly agent that greets the user warmly.",
)