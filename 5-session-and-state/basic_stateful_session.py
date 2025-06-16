
import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from qa_agent import agent
from loguru import logger



load_dotenv()
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Pham Trinh Duc",
    "user_preferences": """
        I like to play Pickleball, Disc Golf, and Tennis.
        My favorite food is Mexican.
        My favorite TV show is Game of Thrones.
        Loves it when people like and subscribe to his YouTube channel.
    """,
}

APP_NAME = "qa_agent"
USER_ID = "pham_trinh_duc"
SESSION_ID = str(uuid.uuid4())
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

logger.info(f"Created session: {stateful_session.app_name}")

runner = Runner(
    app_name=APP_NAME,
    session_service=session_service_stateful,
    agent=agent,
)

new_message = types.Content(
  role="user", 
  parts = [types.Part(text="What is my favorite food?")]
)

for event in runner.run (
  user_id=USER_ID, 
  session_id=SESSION_ID,
  new_message=new_message,
):

  if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

print("==== Session Event Exploration ====")
session = session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# Log final Session state
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"{key}: {value}")