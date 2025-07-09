import asyncio
import sys
import os
from loguru import logger
from google.adk.runners import Runner
from google.genai import types

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from host_agent_adk.host.agent import root_agent
from google.adk.sessions import DatabaseSessionService



db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

async def process_agent_response(event):
    """Process and display agent response events."""
    # Log basic event info
    print(f"Event ID: {event.id}, Author: {event.author}")

    # Check for specific parts first
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "executable_code") and part.executable_code:
                # Access the actual code string via .code
                print(
                    f"  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```"
                )
                has_specific_part = True
            elif hasattr(part, "code_execution_result") and part.code_execution_result:
                # Access outcome and output correctly
                print(
                    f"  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}"
                )
                has_specific_part = True
            elif hasattr(part, "tool_response") and part.tool_response:
                # Print tool response information
                print(f"  Tool Response: {part.tool_response.output}")
                has_specific_part = True
            # Also print any text parts found in any event for debugging
            elif hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"Response: '{part.text.strip()}'")

    # Check for final response after specific parts
    final_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
        else:
            print(
                f"\n==> Final Agent Response: [No text content in final event]"
            )
    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", 
                            parts=[types.Part(text=query)])
    final_response_text = None
    try:
      async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
      ):
        # Process each event and get the final response if available
        response = await process_agent_response(event)
        if response:
            final_response_text = response
    except Exception as e:
        logger.error(f"Error during agent call: {e}")
    return final_response_text


async def main_async(): 

  APP_NAME = "Schedule agent"
  USER_ID = "duc pham"

  runner = Runner(
    agent=root_agent,
    app_name=APP_NAME, 
    session_service=session_service,
  )

  existing_sessions = await session_service.list_sessions(
    app_name=APP_NAME,
    user_id=USER_ID,
  )
  
  # If there's an existing session, use it, otherwise create a new one
  if existing_sessions and len(existing_sessions.sessions) > 0:
      # Use the most recent session
      SESSION_ID = existing_sessions.sessions[0].id
      print(f"Continuing existing session: {SESSION_ID}")
  else:
      # Create a new session with initial state
      new_session = await session_service.create_session(
          app_name=APP_NAME,
          user_id=USER_ID,
          state={},
      )
      SESSION_ID = new_session.id
      print(f"Created new session: {SESSION_ID}")

  while True:
    # Get user input
    user_input = input("You: ")

    # Check if user wants to exit
    if user_input.lower() in ["exit", "quit"]:
        print("Ending conversation. Your data has been saved to the database.")
        break

    # Process the user query through the agent
    await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main_async())