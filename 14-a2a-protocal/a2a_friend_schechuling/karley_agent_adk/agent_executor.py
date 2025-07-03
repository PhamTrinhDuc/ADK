
import asyncio
from loguru import logger
from collections.abc import AsyncGenerator

from a2a.server.agent_execution import AgentExecutor
from a2a.server.events.event_queue import EventQueue
from a2a.server.agent_execution.context import RequestContext
from a2a.server.tasks import TaskUpdater
from a2a.types import (
  Part, 
  TextPart, 
  FilePart,
  FileWithUri,
  FileWithBytes,
  TaskState,
  UnsupportedOperationError
)

from google.adk import Runner
from google.adk.events import Event
from google.genai import types

class KarleyAgentExcecutor: 
  def __init__(self, runner: Runner): 
    self.runner = runner # commute with Google ADK
    self._running_sessions = {} # track active sessions

  async def execute(self, context: RequestContext, event_queue: EventQueue): # entry point
    if not context.task_id or not context.context_id: 
      raise ValueError("context: RequestContext must have task_id and context_id")
    if not context.message: 
      raise ValueError("context: RequestContext must have message")
    
    updater = TaskUpdater(event_queue=event_queue, task_id=context.task_id, context_id=context.context_id)
    if not context.current_task: 
      updater.submit()

    updater.start_work()
    await self._process_request(new_message=context.message, 
                                session_id=context.context_id, 
                                task_updater=updater)

  def cancel(self, context: RequestContext, event_queue: EventQueue): 
    raise SyntaxError(error = UnsupportedOperationError())    

  async def _process_request(self, 
                             new_message: types.Content, 
                             session_id: str, 
                             task_updater: TaskUpdater) -> None: 
    session_obj = self._upsert_session(session_id=session_id)
    session_id = session_obj.session_id  

    async for event in self._run_agent(session_id=session_id, new_message=new_message): 
      if event.is_final_response(): 
        parts = convert_genai_parts_to_a2a(
          parts=event.content.parts if event.content and event.content.parts else []
        )

        logger.debug("Yielding final response: %s", parts)
        task_updater.add_artifact(parts=parts)
        task_updater.complete()
        break
      if not event.get_function_calls(): 
        logger.debug("Yielding update response")
        task_updater.update_status(
          state=TaskState.working, 
          message=task_updater.new_agent_message(
            parts=event.content.parts if event.content and event.content.parts else []
          )
        )
      else:
        logger.debug("Skipping event")

  def _run_agent(self, 
                 session_id: str, 
                 new_message: types.Content) -> AsyncGenerator[Event, None]: 
    return self.runner.run_async(
      user_id="karley_agent", session_id=session_id, new_message=new_message
    )
    
  async def _upsert_session(self, session_id: str): 
    # Try to get existing session
    session = await self.runner.session_service.get_session(
      app_name=self.runner.app_name, user_id="karley_agent", session_id=session_id
    )

    # If doensn't exist, create new one
    if session is None: 
      session = await self.runner.session_service.create_session(
        app_name=self.runner.app_name, user_id="karley_agent", session_id=session_id
      )

    if session is None: 
      raise ValueError(f"Failed to get or create session: {session_id}")
    return session


def convert_a2a_parts_to_genai(parts: list[Part]) -> list[types.Part]: 
  return [convert_genai_part_to_a2a(part=part) for part in parts]


def convert_a2a_part_to_genai(part: Part) -> types.Part: 
  """Convert a single A2A Part type into a Google Gen AI Part type."""
  """
  | Loại dữ liệu gốc     | Xử lý ra sao?                                                        |
  | -------------------- | -------------------------------------------------------------------- |
  | `TextPart`           | Trả về `types.Part(text=...)`                                        |
  | `FilePart` với URI   | Trả về `types.Part(file_data=FileData(file_uri=..., mime_type=...))` |
  | `FilePart` với Bytes | Trả về `types.Part(inline_data=Blob(data=..., mime_type=...))`       |
  | Khác                 | Raise `ValueError`                                                   |
  """
  
  root = part.root
  if isinstance(root, TextPart): 
    return types.Part(text=root.text)
  if isinstance(root, FilePart): 
    if isinstance(root.fil, FileWithUri): 
      return types.Part(
        file_data=types.FileData(
          file_uri=root.file, 
          mime_type=root.file.mimeType
        )
      )
    if isinstance(root.file, FileWithBytes): 
      return types.Part(
        file_data=types.Blob(
          data=root.file.bytes.encode("utf-8"), 
          mime_type=root.file.mimeType or "application/octet-stream"
        )
      )
    raise ValueError(f"Unsupported file type: {type(root.file)}")
  raise ValueError(f"Unsupported part type: {type(part)}")
  

def convert_genai_parts_to_a2a(parts: list[types.Part]) -> list[Part]: 
  return [convert_genai_part_to_a2a(part=part) for part in parts
          if (part.text or part.file_data or part.inline_data)]


def convert_genai_part_to_a2a(part: types.Part) -> Part: 
  if part.text: 
    return Part(root=TextPart(text=part.text))
  
  if part.file_data: 
    if part.file_data.file_uri: 
      return Part(
        root=FilePart(
          file=FileWithUri(
            uri=part.file_data.file_uri, 
            mimeType=part.file_data.mime_type
          )
        )
      )
    else: 
      raise ValueError("Part missing value file_uri")

  if part.inline_data: 
    if part.inline_data.data: 
      return Part(
        root=FilePart(
          file=FileWithBytes(
            mimeType=part.inline_data.mime_type,
            bytes=part.inline_data.data
          )
        )
      )
    else: 
      raise ValueError("Part missing value data")
    
  raise ValueError(f"Unsupported part type: {part}")
  




