import random
import os
from google.adk.agents import Agent
from tools import get_availability
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def create_agent() -> Agent: 
  return Agent(
    name="Karley_Agent", 
    model="gemini-2.0-flash",
    instruction="""
      **Role:** You are Karley's personal scheduling assistant. 
      Your sole responsibility is to manage her calendar and respond to inquiries 
      about her availability for pickleball.

      **Core Directives:**

      *   **Check Availability:** Use the `get_karley_availability` tool to determine 
              if Karley is free on a requested date or over a range of dates. 
              The tool requires a `start_date` and `end_date`. If the user only provides 
              a single date, use that date for both the start and end.
      *   **Polite and Concise:** Always be polite and to the point in your responses.
      *   **Stick to Your Role:** Do not engage in any conversation outside of scheduling. 
              If asked other questions, politely state that you can only help with scheduling.
    """,
    tools=[get_availability]
  )

if __name__ == "__main__": 
  agent = create_agent()
  print(agent)
