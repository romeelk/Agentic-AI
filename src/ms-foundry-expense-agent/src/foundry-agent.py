from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
import os
import sys

def has_file_attachment(response)->bool:
    last_message = response.output[-1]

    return (last_message.type == "message"
        and last_message.content
        and last_message.content[-1].type == "output_text"
        and last_message.content[-1].annotations)

def extract_file_from_response(response):
    last_message = response.output[-1]
        
    file_citation = last_message.content[-1].annotations[-1]  # AnnotationContainerFileCitation
    if file_citation.type == "container_file_citation":
        print("Last conversation response generated a file")
        print(f"The file details are {file_citation.filename}")
        file_id = file_citation.file_id
        file_name = file_citation.filename
        container_id = file_citation.container_id

        return file_id, file_name, container_id


def download_expense_file(openai_client, file_id, file_name, container_id):
    file_content = openai_client.containers.files.content.retrieve(file_id=file_id, container_id=container_id)
    print(f"File ready for download: {file_name}")
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, file_name)
    with open(file_path, "wb") as f:
        f.write(file_content.read())
    print(f"File downloaded successfully: {file_path}")


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
        # Reference the agent to get a response

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
    # save_expense_file(None)

