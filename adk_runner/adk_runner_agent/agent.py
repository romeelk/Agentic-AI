from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv
from google.genai import types
import asyncio

load_dotenv()

async def main():


    APP_NAME = "adk_runner_app"
    USER_ID = "user1"

    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    root_agent = Agent(
        name="assistant",
        model="gemini-2.5-flash",
        instruction="You are a helpful assistant."
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    while True:
        message = input("You: ")

        if message.lower() in ("exit", "quit","e","q"):
            break

        user_message = types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )
        # main event loop
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=user_message,
        ):
            if hasattr(event, "content") and event.content:
                print("Assistant:", event.content.parts[0].text)



if __name__ == "__main__":
    # Run the async event loop
    asyncio.run(main())