import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

def main():
    load_dotenv()
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model_deployment_name = os.getenv("MODEL_DEPLOYMENT")
    print("Welcome to OpenAI simple chat client..")
    print(f"Connecting to OpenAI Foundry endpoint {azure_openai_endpoint}")


    token_provider = get_bearer_token_provider(
     DefaultAzureCredential(), "https://ai.azure.com/.default")
    
    openai_client = OpenAI(
     base_url=azure_openai_endpoint,
     api_key=token_provider
)
    
    # start chat loop
    while True:
        input_text= input("Enter a prompt(enter q to quit)")
        if input_text.lower() == "q":
            break
        completion = openai_client.chat.completions.create(
        model=model_deployment_name,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant that answers questions and provides information."
            },
            {
                "role": "user",
                "content": input_text
            }
        ]
        )
        print(completion.choices[0].message.content)

    
if __name__ == "__main__":
    main()
    