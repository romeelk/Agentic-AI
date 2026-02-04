from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
import os


load_dotenv()

foundry_endpoint = os.getenv("AZURE_EXISTING_AIPROJECT_ENDPOINT")

project_client = AIProjectClient(endpoint=foundry_endpoint, credential=DefaultAzureCredential())


# name of existing agent
foundry_agent_name = "expense-agent"

foundry_agent = project_client.agents.get(agent_name=foundry_agent_name)

if foundry_agent is not None:
    print(f"Fetched existing {foundry_agent.name}")

    openai_client = project_client.get_openai_client()

    # replaces previous API thread concept
    conversation = openai_client.conversations.create(
            items=[{"type": "message", "role": "user", "content": "Tell me what you can help with?"}],
        )
    response = openai_client.responses.create(conversation=conversation.id,
    extra_body={"agent": {"name": foundry_agent.name, "type": "agent_reference"}},
    )

    print(f"Response output: {response.output_text}")

    response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={"agent": {"name": foundry_agent.name, "type": "agent_reference"}},
    input="And what is expense limit for category Travel?",
)
    print(f"Response output: {response.output_text}")

