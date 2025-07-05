import os
from dotenv import load_dotenv
load_dotenv()

from datetime import date
from crewai.llm import LLM
from crewai.agent import Agent, Task
from crewai.crew import Crew, Process
from tools import AvailabilityTool



class SchedulingAgent: 
  """Agent that handles scheduling tasks."""

  def __init__(self): 
    """Initializes the SchedulingAgent."""
    if os.getenv("GOOGLE_API_KEY"):
        self.llm = LLM(
            model="gemini/gemini-2.0-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
    else:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    self.scheduling_assistant = Agent(
      role="Personal Scheduling Assistant",
      goal="Check my calendar and answer questions about my availability.",
      backstory=(
          "You are a highly efficient and polite assistant. Your only job is "
          "to manage my calendar. You are an expert at using the "
          "Calendar Availability Checker tool to find out when I am free. You never "
          "engage in conversations outside of scheduling."
      ),
      verbose=True,
      allow_delegation=False,
      tools=[AvailabilityTool()],
      llm=self.llm,
    )
  
  def invoke(self, query: str) -> str: 
    """Kicks off the crew to answer a scheduling question."""
    task_description = (
      f"Answer the user's question about my availability. The user asked: '{query}'. "
      f"Today's date is {date.today().strftime('%Y-%m-%d')}."
    )

    check_availability_task = Task(
      description=task_description,
      expected_output="A polite and concise answer to the user's question about my availability, based on the calendar tool's output.",
      agent=self.scheduling_assistant,
    )

    crew = Crew(
       tasks=[check_availability_task],
       agents=[self.scheduling_assistant], 
       process=Process.sequential,
       verbose=True
    )

    results = crew.kickoff()
    return str(results)