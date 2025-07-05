from typing import Callable

import httpx
from a2a.client import A2AClient
from a2a.types import (
    AgentCard,
    SendMessageRequest,
    SendMessageResponse,
    Task,
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
)
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

TaskCallbackArg = Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent
TaskUpdateCallback = Callable[[TaskCallbackArg, AgentCard], Task]

class RemoteAgentConnections:
  def __init__(self, agent_card: AgentCard, agent_url: str):
    logger.debug(f"Creating connection to {agent_card.name} at {agent_url}")
    self._http_client = httpx.AsyncClient(timeout=30)
    self.agent_client = A2AClient(httpx_client=self._http_client, agent_card=agent_card, url=agent_url)
    self.card = agent_card
    self.conversation_name = None
    self.conversation = None
    self.pending_tasks = set()
  
  def get_agent(self) -> AgentCard: 
    return self.card
  
  async def send_message(self, message: SendMessageRequest) -> SendMessageResponse:
    logger.debug(f"Sending message to {self.card.name}: {message}")
    response = await self.agent_client.send_message(message)
    logger.debug(f"Received response from {self.card.name}: {response}")
    return response
