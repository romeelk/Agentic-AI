from dotenv import load_dotenv

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as project_client,
):
    model = os.environ("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    openai_client = project_client.get_openai_client
    print(f"Starting agent with model: {model}")
    
    with project_client.get_openai_client() as openai_client:
        response = openai_client.responses.create(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        input="What is the size of France in square miles?",
    )
        print(f"Response output: {response.output_text}")


