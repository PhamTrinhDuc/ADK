import uuid
import httpx
from loguru import logger

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
  AgentCard, 
  Part, 
  TextPart,
  Role, 
  Message, 
  MessageSendParams, 
  SendMessageRequest, 
)

NATE_AGENT_CARD_PATH = "./well-known/agent.json"
NATE_AGENT_URL = "http://localhost:10002"


async def main() -> None: 
  async with httpx.AsyncClient() as http_client: 
    resolver = A2ACardResolver(
      httpx_client=http_client, 
      base_url=NATE_AGENT_URL,
    )

    nate_card_use: AgentCard  | None = None

    try: 
      logger.info(
        f"Fetching public agent card from: {NATE_AGENT_URL}{NATE_AGENT_CARD_PATH}"
      )
      _public_card = await resolver.get_agent_card()
      nate_card_use = _public_card

    except Exception as e:
      logger.error(f"Error fetching public agent card: {e}")
      raise RuntimeError("Failed to fetch public agent card") 
    
    client = A2AClient(
      httpx_client=http_client, agent_card=nate_card_use
    )

    messge_payload = Message(
      role=Role.user, 
      messageId=str(uuid.uuid4()), 
      parts=[Part(root=TextPart(text="Xin chào, bạn có nhiệm vụ gì ?"))]
    )

    request_message = SendMessageRequest(
      id=str(uuid.uuid4()), 
      params=MessageSendParams(message=messge_payload)
    )

    response = await client.send_message(request=request_message)

    print(response.model_dump_json(indent=2))
  

if __name__ == "__main__": 
  import asyncio

  asyncio.run(main())
