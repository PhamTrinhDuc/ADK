
import os
import uvicorn
from loguru import logger
from a2a.types import (
   AgentCapabilities,
   AgentCard, 
   AgentSkill
)
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AStarletteApplication
from .agent_executor import SchedulingAgent


HOST = "localhost"
PORT = 10003
VERSION = "1.0.0"

class MissingAPIKeyError(Exception):
    """Exception for missing API key."""

def main(): 
  try:
    if not os.getenv("GOOGLE_API_KEY"):
      raise MissingAPIKeyError("GOOGLE_API_KEY environment variable not set.")
  
    capabilities = AgentCapabilities(streaming=True)

    agent_skill = AgentSkill(
      id="availability_checker", 
      name="Availability Checker", 
      description="Check my calendar to see when I'm available for a pickleball game.",
      tags=["schedule", "availability", "calendar"],
      examples=[
          "Are you free tomorrow?",
          "Can you play pickleball next Tuesday at 5pm?",
      ],
    )

    agent_host_url = f"http://{HOST}:{PORT}"
    
    card = AgentCard(
      name="Nate Agent",
      description="A friendly agent to help you schedule a pickleball game with Nate.",
      url=agent_host_url,
      version=VERSION,
      capabilities=capabilities, 
      skills=[agent_skill],
      defaultInputModes= ["text/plain"], 
      defaultOutputModes= ["text/plain"], 
    )

    request_handler = DefaultRequestHandler(
      agent_executor=SchedulingAgent(), 
      task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
      agent_card=card, 
      http_handler=request_handler
    )

    uvicorn.run(server.build(), host=HOST, port=PORT)
  except MissingAPIKeyError as e:
    logger.error(f"Error: {e}")
    exit(1)
  except Exception as e:
    logger.error(f"An error occurred during server startup: {e}")
    exit(1)

if __name__ == "__main__":
    main()