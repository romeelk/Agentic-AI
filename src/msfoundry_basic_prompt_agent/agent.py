import os
import sys
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import datetime
from dotenv import load_dotenv

load_dotenv()

def _get_citation_filename(message):
    try:
        citation = message.content[-1].annotations[-1]
   
        return citation.filename if citation.type == "file_citation" else None
    except (AttributeError, IndexError):
        return None
    
def main():
    print("Welcome to basic Prompt Agent from Microsoft Foundry")
    current_date_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"The current date time is:{current_date_time.strftime("%d-%m-%Y %H:%M:%S")}")

    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    agent_name = os.environ["AGENT_NAME"]

    if endpoint is None:
        print("Could not find env var FOUNDRY_PROJECT_ENDPOINT")
    with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
    ):
        print(f"Successfully authenticated to Microsoft Foundry endpoint {endpoint}")

        agent = project_client.agents.get(agent_name=agent_name)

        if agent is None:
            print("Failed to get agent.")
            sys.exit()

        print(f"Successful obtained agent {agent.name} with id {agent.id}")

        # Create a conversation for the agent interaction
        conversation = openai_client.conversations.create()
        print(f"Created conversation (id: {conversation.id})")
        # Main chat loop
        while True:
            query = input("User:(q to quit):")
            if query.lower() == "q":
                sys.exit()

            response = openai_client.responses.create(conversation=conversation.id,input=query, extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}})
           
            if(hasattr(response.output[-1].content[-1],"annotations")):
                file_name = _get_citation_filename(response.output[-1])
                print(f"{response.output_text} (source:{file_name})")
            else:
                print(f"{response.output_text}")

if __name__ == "__main__":
    main()