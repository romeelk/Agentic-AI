import os
import sys
import traceback
import datetime

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai.types.responses import ResponseOutputItem
from dotenv import load_dotenv

from azure.core.exceptions import HttpResponseError
from azure.core.exceptions import ClientAuthenticationError

load_dotenv()


def _get_citation_filename(message:ResponseOutputItem):
    """
    A helper function to extract the response file citation file name

    Args:
        message (ResponseOutputItem): output from openai response api

    Returns:
        string: the citation filename
    """
    try:
        citation = message.content[-1].annotations[-1]

        return citation.filename if citation.type == "file_citation" else None
    except (AttributeError, IndexError):
        return None


def main():
    """ 
    Main entry point for Foundry Agent. Setups Agent authentication
    and main agent chat loop.
    """
    print("Welcome to basic Prompt Agent from Microsoft Foundry")
    current_date_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"The current date time is:{current_date_time.strftime('%d-%m-%Y %H:%M:%S')}")

    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", None)
    agent_name = os.getenv("AGENT_NAME", None)

    if endpoint is None:
        print("Could not find env var FOUNDRY_PROJECT_ENDPOINT. Exiting agent")
        sys.exit()
    if agent_name is None:
        print("Could not find env var AGENT_NAME. Exiting agent")
        sys.exit()
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

        while True:
            query = input("User:(q to quit):")
            if query.lower() == "q":
                sys.exit()

            response = openai_client.responses.create(
                conversation=conversation.id,
                input=query,
                extra_body={
                    "agent_reference": {"name": agent.name, "type": "agent_reference"}
                },
            )

            file_name = _get_citation_filename(response.output[-1])
            if file_name:
                print(f"{response.output_text} (source:{file_name})")
            else:
                print(f"{response.output_text}")


if __name__ == "__main__":
    try:
        main()
    except ClientAuthenticationError as client_auth_error:
        print(f"Error authenticating Agent to MS Foundry at line {client_auth_error.__traceback__.tb_lineno}: {traceback.format_exc()}")
    except HttpResponseError as http_response_error:
        print(f"Error during request to Agent in MS Foundry at line {http_response_error.__traceback__.tb_lineno}: {traceback.format_exc()}")
    except Exception as exception:
        print(f"An unknown error occured at line {exception.__traceback__.tb_lineno}: {traceback.format_exc()}")
    