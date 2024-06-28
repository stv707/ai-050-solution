import os
import asyncio
from dotenv import load_dotenv

# Add Azure OpenAI package
from openai import AsyncAzureOpenAI

## Addition Function to get user text from user.txt
def get_user_text(file_path='user.txt'):
    # Check if the file exists and is not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf8') as file:
            return file.read().strip()
    else:
        # If the file is empty or doesn't exist, prompt the user to enter message
        return input("Enter user message: ")

# Set to True to print the full response from OpenAI for each call
printFullResponse = False

async def main(): 
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Configure the Azure OpenAI client
        client = AsyncAzureOpenAI(
            azure_endpoint = azure_oai_endpoint, 
            api_key=azure_oai_key,  
            api_version="2024-02-15-preview"
        )
        

        while True:
            # Pause the app to allow the user to change the system prompt
            print("------------------\nPausing the app to allow you to change the system prompt.\nPress anything then enter to continue...")
            input()

            # Read in system message and prompt for user message
            system_text = open(file="system.txt", encoding="utf8").read().strip()
            user_text = get_user_text()
            if user_text.lower() == 'quit' or system_text.lower() == 'quit':
                print('Exiting program...')
                break
            
            # Read the grounding text freshly for each request
            grounding_text = open(file="grounding.txt", encoding="utf8").read().strip()
            
            # Debugging prints to ensure the correct texts are being read
            print("\nSystem Message:", system_text)
            print("\nUser Message:", user_text)
            print("\nGrounding Text:", grounding_text)

            await call_openai_model(system_message = system_text, 
                                    user_message = user_text, 
                                    grounding_message = grounding_text,
                                    model=azure_oai_deployment, 
                                    client=client
                                    )

    except Exception as ex:
        print(ex)

async def call_openai_model(system_message, user_message, grounding_message, model, client):
    # Format and send the request to the model
    combined_message = grounding_message + " " + user_message
    messages =[
        {"role": "system", "content": system_message},
        {"role": "user", "content": combined_message},
    ]
    
    # Debugging prints to check the message structure
    print("\nSending request to Azure OpenAI model with the following messages:\n", messages)

    # Call the Azure OpenAI model
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800
    )

    if printFullResponse:
        print(response)

    print("Response:\n" + response.choices[0].message.content + "\n")

if __name__ == '__main__': 
    asyncio.run(main())
