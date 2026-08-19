from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

import os
import sys
import traceback

from openai import OpenAI 
from openai.resources.responses import Responses

def has_file_attachment(response:Responses)->bool:
    """ Checks if agent response contains a file attachment

    Args:
        response: OpenAI response

    Returns:
        bool: true if agent response has a file false if not
    """    
    last_message = response.output[-1]

    return (last_message.type == "message"
        and last_message.content
        and last_message.content[-1].type == "output_text"
        and last_message.content[-1].annotations)

def extract_file_from_response(response:Responses):
    """Extract the file from the openai response.

    Args:
        response: OpenAI response

    Returns:
        tuple: file_id, file_name, container_id
    """    
    last_message = response.output[-1]

    file_citation = last_message.content[-1].annotations[-1]  # AnnotationContainerFileCitation
    if file_citation.type == "container_file_citation":
        print("Last conversation response generated a file")
        print(f"The file details are {file_citation.filename}")
        file_id = file_citation.file_id
        file_name = file_citation.filename
        container_id = file_citation.container_id

        return file_id, file_name, container_id


def download_expense_file(openai_client:OpenAI, file_id, file_name, container_id):
    """ Downloads the Azure Foundry agents generated file which is generated
        using the CodeInterpreter tool

    Args:
        openai_client (OpenAi): _description_
        file_id (string): the file_id of the file generated
        file_name (string): the file_name generated 
        container_id (string): the container_id - i think relates to the sandbox
    """    
    file_content = openai_client.containers.files.content.retrieve(file_id=file_id, container_id=container_id)
    print(f"File ready for download: {file_name}")
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path,"generated_expenses", file_name)
    with open(file_path, "wb") as f:
        f.write(file_content.read())
    print(f"File downloaded successfully: {file_path}")


def main():
    load_dotenv()

    myEndpoint = os.getenv("AZURE_EXISTING_AIPROJECT_ENDPOINT")

    if myEndpoint is None:
        print("Failed to load AZURE_EXISTING_AIPROJECT_ENDPOINT env var. Exiting agent.")
        sys.exit()

    project_client = AIProjectClient(
        endpoint=myEndpoint,
        credential=DefaultAzureCredential(),
    )

    my_agent = "expense-agent"
    # Get an existing agent
    agent = project_client.agents.get(agent_name=my_agent)
    print(f"Retrieved agent: {agent.name} with ID: {agent.id}")

    openai_client = project_client.get_openai_client()

    # create a conversation for context memory
    conversation = openai_client.conversations.create()
        
    while True:
        try:
            prompt= input("Enter your query for the Agent(q to quit):")

            if prompt.lower() == "q":
                print("Thank you for using expense agent!")
                break

            response = openai_client.responses.create(
                conversation=conversation.id,
                input=[{"role": "user", "content": prompt}],
                extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
            )

            print(f"Response output: {response.output_text}")

            if has_file_attachment(response):
                file_id, file_name, container_id = extract_file_from_response(response)
                if file_id and container_id:
                    download_expense_file(openai_client,file_id,file_name,container_id)
            else:
                print("No expense file generated...")

        except:
            print("I was unable to process your query..")
            
if __name__ == "__main__":
    # run agent main loop
    try:
        main()
    except Exception as e:
        print(f"Error creating agent at line {e.__traceback__.tb_lineno}: {traceback.format_exc()}")