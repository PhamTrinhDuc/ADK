import sys
import os
import uvicorn
from dotenv import load_dotenv
from loguru import logger
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
   AgentCapabilities, 
   AgentCard, 
   AgentSkill
)
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService

from agent import create_agent

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from agent_executor import KarleyAgentExecutor

load_dotenv()

class MissingAPIKeyError(Exception):
    """Exception for missing API key."""
    pass

HOST = "localhost"
PORT = 10002
VERSION = "1.0.0"


def main(): 
  try:
    # Check for API key only if Vertex AI is not configured
    if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
      if not os.getenv("GOOGLE_API_KEY"):
        raise MissingAPIKeyError(
            "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
        )
    capabilities = AgentCapabilities(streaming=True)
    
    skill = AgentSkill(
      id="check_schedule", 
      name="Check Karley's Schedule", 
      description="Checks Karley's availability for a pickleball game on a given date.", 
      tags=["schedule", "calendar"], 
      examples=["Is Karley free to play pickleball tomorrow?"],
    )
    
    card = AgentCard(
      name="Karley Agent",
      description="An agent that manages Karley's schedule for pickleball games.",
      url=f"http://{HOST}:{PORT}",
      version=VERSION,
      defaultInputModes=["text/plain"], 
      defaultOutputModes=["text/plain"],
      capabilities=capabilities, 
      skills=[skill]
    )

    agent = create_agent()

    
    runner = Runner(
      app_name="karley agent", 
      agent=agent, 
      artifact_service=InMemoryArtifactService(), 
      memory_service=InMemoryMemoryService(), 
      session_service=InMemorySessionService(),
    )

    agent_executor = KarleyAgentExecutor(runner=runner)

    request_handler = DefaultRequestHandler(
      agent_executor=agent_executor, 
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