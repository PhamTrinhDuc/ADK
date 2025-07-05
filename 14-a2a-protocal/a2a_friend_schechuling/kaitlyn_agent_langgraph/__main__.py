import os
import sys
import uvicorn
from loguru import logger
import httpx
from a2a.types import (
   AgentCapabilities,
   AgentCard, 
   AgentSkill, 
)
from a2a.server.tasks import InMemoryPushNotifier, InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from .agent_executor import KaitlynAgentExecutor



class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


HOST = "localhost"
PORT = 10004
VERSION = "1.0.0"


def main(): 
  try: 
    if not os.getenv("GOOGLE_API_KEY"):
      raise MissingAPIKeyError("GOOGLE_API_KEY environment variable not set.")

    capabilities = AgentCapabilities(streaming=True)

    agent_skill = AgentSkill(
      id="schedule_pickleball",
      name="Pickleball Scheduling Tool",
      description="Helps with finding Kaitlyn's availability for pickleball",
      tags=["scheduling", "pickleball"],
      examples=["Are you free to play pickleball on Saturday?"],
    )

    agent_card = AgentCard(
      name="Kaitlyn Agent",
      description="Helps with scheduling pickleball games",
      url=f"http://{HOST}:{PORT}",
      version=VERSION,
      defaultInputModes=["text/plain"], 
      defaultOutputModes=["text/plain"],
      capabilities=capabilities, 
      skills=[agent_skill],
    )

    httpx_client = httpx.AsyncClient()
    request_handler = DefaultRequestHandler(
        agent_executor=KaitlynAgentExecutor(),
        task_store=InMemoryTaskStore(),
        push_notifier=InMemoryPushNotifier(httpx_client),
    )
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    uvicorn.run(server.build(), host=HOST, port=PORT)

  except MissingAPIKeyError as e:
    logger.error(f"Error: {e}")
    sys.exit(1)
  except Exception as e:
    logger.error(f"An error occurred during server startup: {e}")
    sys.exit(1)


if __name__ == "__main__":
    main()