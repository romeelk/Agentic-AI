# # 1. Initialize in-memory services for local testing
#     session_service = InMemorySessionService()
#     artifact_service = InMemoryArtifactService()

#     # Define session and user identifiers
#     app_name = Config.APP_NAME
#     user_id = "market_researcher_test_user"
#     session_id = "market_researcher_session_001"

# # 2. Create a session for the interaction
#     await session_service.create_session(
#         app_name=app_name,
#         user_id=user_id,
#         session_id=session_id
#     )
 
#  # 3. Instantiate the Runner with the Informer Agent
#     runner = Runner(
#         agent=informer_agent,
#         app_name=app_name,
#         session_service=session_service,
#         artifact_service=artifact_service,
#     )


# async for event in runner.run_async(
#         user_id=user_id,
#         session_id=session_id,
#         new_message=user_message
#     ):
#         all_events.append(event)
#         # Capture final response text
#         if event.is_final_response() and event.content and event.content.parts:
#             final_response_text = event.content.parts[0].text if hasattr(event.content.parts[0], 'text') else str(event.content.parts[0])