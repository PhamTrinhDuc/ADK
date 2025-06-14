from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from google.adk.tools import google_search
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

LLM_MODEL = "openai/gpt-4o-mini"
GEMINI_MODEL = "gemini-2.0-flash-lite"  
model = LiteLlm(model=LLM_MODEL)

def get_current_time(): 
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    from datetime import datetime
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    } 

root_agent = Agent(
  name="tool_agent", # This is the name of the agent. Match the name of folder. It should start with a letter (a-z, A-Z) or an underscore (_), and can only contain letters, digits (0-9), and underscores
  model=GEMINI_MODEL,
  description="A simple agent that provides various tools.",
  instruction="You are a helpful agent that provides various tools.",
  # tools=[google_search],
  tools=[get_current_time],
  # tools = [google_search, get_current_time], <-- not allowed
)