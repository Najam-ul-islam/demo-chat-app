import os
from dotenv import load_dotenv
from openai import OpenAI

# import namespaces



def sync_chat(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")
        api_key = os.getenv("API_Key")

        if not model_deployment:
            raise ValueError("MODEL_DEPLOYMENT environment variable is required")

        # Initialize the OpenAI client
        
        client = OpenAI(base_url=azure_openai_endpoint, api_key=api_key)

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue
            # ChatCompleteions API
            # ====================
            # Get a response
            # completion = client.chat.completions.create(
            #     model=model_deployment,
            #     messages=[
            #         {
            #             "role": "user",
            #             "content": input_text,
            #         }
            #     ],
            # )
            # print(f"\nResponse:\n{completion.choices[0].message.content}")
        
        #    Responses API
        # ===================
            last_response_id = None  
            response = client.responses.create(
                model=model_deployment,
                instructions="""You are a helpful assistant that hepls find information about the topic provided by the user. 
                                Please provide a response in bullet points.""",
                input=input_text,
                previous_response_id=last_response_id,
            )
            print(f"\nResponse:\n{response.output_text}")

    except Exception as ex:
        print(ex)