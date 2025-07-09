import random
import sys
import os
from collections.abc import AsyncIterable
from datetime import date, datetime, timedelta
from typing import Any, List, Literal
from pydantic import BaseModel, Field

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from tools import get_availability

memory = MemorySaver()


class ResponseFormat(BaseModel):
  """Respond to the user in this format."""

  status: Literal["input_required", "completed", "error"] = "input_required"
  message: str


class KaitlynAgent:
  """KaitlynAgent - a specialized assistant for scheduling."""

  SYSTEM_INSTRUCTION = (
    "You are Kaitlyn's scheduling assistant. "
    "Your sole purpose is to use the 'get_availability' tool to answer questions about Kaitlyn's schedule for playing pickleball. "
    "You will be provided with the current date to help you understand relative date queries like 'tomorrow' or 'next week'. "
    "Use this information to correctly call the tool with a specific date (e.g., 'YYYY-MM-DD'). "
    "If the user asks about anything other than scheduling pickleball, "
    "politely state that you cannot help with that topic and can only assist with scheduling queries. "
    "Do not attempt to answer unrelated questions or use tools for other purposes."
    "Set response status to input_required if the user needs to provide more information."
    "Set response status to error if there is an error while processing the request."
    "Set response status to completed if the request is complete."
  )

  def __init__(self):
    self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    self.tools = [get_availability]

    self.graph = create_react_agent(
      self.model,
      tools=self.tools,
      checkpointer=memory,
      prompt=self.SYSTEM_INSTRUCTION,
      response_format=ResponseFormat,
    )
  
  def invoke(self, query: str, context_id: str): 
    config: RunnableConfig = {"configurable": {"thread_id": context_id}}
    today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}."
    augmented_query = f"{today_str}\n\nUser query: {query}"
    self.graph.invoke(input=augmented_query, config=config)
    return self.get_agent_response(config)
  
  async def stream(self, query: str, context_id: str) -> AsyncIterable[dict[str, any]]: 
    config: RunnableConfig = {"configurable": {"thread_id": context_id}}
    today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}."
    augmented_query = f"{today_str}\n\nUser query: {query}"
    inputs = {"messages": [("user", augmented_query)]}

    for item in self.graph.stream(input=inputs, config=config, stream_mode="values"): 
      message = item["messages"][-1]
      if (
        isinstance(message, AIMessage)
        and message.tool_calls
        and len(message.tool_calls)> 0
      ): 
        yield {
          "is_task_complete": False,
          "require_user_input": False,
          "content": "Checking Kaitlyn's availability...",
        }
      
      elif isinstance(message, ToolMessage): 
        yield {
          "is_task_complete": False,
          "require_user_input": False,
          "content": "Processing availability...",
        }

    yield self.get_agent_response(config)

  def get_agent_response(self, config: RunnableConfig) -> dict[str, any]:
    current_state = self.graph.get_state(config)
    structured_response = current_state.values.get("structured_response")
    if structured_response and isinstance(structured_response, ResponseFormat):
      if structured_response.status == "input_required":
        return {
            "is_task_complete": False,
            "require_user_input": True,
            "content": structured_response.message,
        }
      if structured_response.status == "error":
        return {
            "is_task_complete": False,
            "require_user_input": True,
            "content": structured_response.message,
        }
      if structured_response.status == "completed":
        return {
            "is_task_complete": True,
            "require_user_input": False,
            "content": structured_response.message,
        }

    return {
      "is_task_complete": False,
      "require_user_input": True,
      "content": (
          "We are unable to process your request at the moment. "
          "Please try again."
      ),
    }