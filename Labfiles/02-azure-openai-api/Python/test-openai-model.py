import os
from dotenv import load_dotenv

# Assuming that 'AzureOpenAI' is a valid import based on your provided code
from openai import AzureOpenAI

def main(): 
    try: 
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint, 
            api_key=azure_oai_key,  
            api_version="2024-02-15-preview"
                )

        # Create a system message
        system_message = """I am a hiking enthusiast named Forest who helps people discover hikes in their area. 
     If no area is specified, I will default to near Rainier National Park. 
     I will then provide three suggestions for nearby hikes that vary in length. 
     I will also share an interesting fact about the local nature on the hikes when making a recommendation."""
        messages_array = [{"role": "system", "content": system_message}]

        while True:
            # Get input text
            input_text = input("Enter Prompt (or type quit to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Enter Prompt.")
                continue
            
            # Add user input to messages array
            messages_array.append({"role": "user", "content": input_text})

            print("\nSending API Request...\n\n")
            
            # Send request to Azure OpenAI model
            response = client.chat.completions.create(
                model=azure_oai_deployment,
                temperature=0.7,
                max_tokens=1200,
                messages=messages_array
            )
            generated_text = response.choices[0].message.content
            
            # Add generated text to messages array
            messages_array.append({"role": "system", "content": generated_text})

            # Print generated text
            print("Summary: " + generated_text + "\n")

            # Optionally, if you want to clear the messages array after each interaction uncomment the line below
            # messages_array = [{"role": "system", "content": system_message}]

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
