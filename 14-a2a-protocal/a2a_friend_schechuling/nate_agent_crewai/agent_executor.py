from loguru import logger

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
  Part, 
  TextPart,
  UnsupportedOperationError,
  InternalError, 
  InvalidParamsError
)
from a2a.utils.errors import ServerError

from agent import SchedulingAgent

class SchedulingAgentExecutor(AgentExecutor): 
  """AgentExecutor for the scheduling agent."""

  def __init__(self):
    """Initializes the SchedulingAgentExecutor."""
    self.agent = SchedulingAgent()
  
  async def execute(
    self, 
    context: RequestContext , 
    event_queue: EventQueue) -> None:

    """Executes the scheduling agent."""
    if not context.task_id or not context.context_id: 
      raise ValueError("RequestContext must have task_id and context_id")
    if not context.message: 
      raise ValueError("RequestContext must have a message")
    
    updater = TaskUpdater(event_queue=event_queue, 
                          task_id=context.task_id, 
                          context_id=context.context_id)
    
    if not context.current_task: 
      await updater.submit()
    
    await updater.start_work()
    if self._validate_request(context): 
      raise ServerError(error=InvalidParamsError())
    
    query = context.get_user_input()
    try: 
      result = self.agent.invoke(query=query)
    except Exception as e:
      logger.error(f"Error invoking agent: {e}")
      raise ServerError(error=InternalError()) from e
    
    parts = [Part(root=TextPart(text=result))]
    await updater.add_artifact(parts)
    await updater.complete()


  async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
      """Handles task cancellation."""
      raise ServerError(error=UnsupportedOperationError())


  def _validate_request(self, context: RequestContext) -> bool:
      """Validates the request context."""
      return False