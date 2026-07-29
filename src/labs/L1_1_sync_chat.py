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
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        if not model_deployment:
            raise ValueError("MODEL_DEPLOYMENT environment variable is required")

        # Initialize the OpenAI client
        
        client = OpenAI(base_url=azure_openai_endpoint, api_key=api_key)

        last_response_id = None  
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
            
            response = client.responses.create(
                model=model_deployment,
                instructions="""You are an experienced business consultant.

                        Your goal is to help users make informed business decisions.

                        When responding:
                        - Understand the business context.
                        - Identify assumptions.
                        - Evaluate risks and opportunities.
                        - Consider cost, scalability, and implementation effort.
                        - Present trade-offs objectively.
                        - Recommend practical next steps.""",
                        tools = [{"type":"web_search_preview"}],
                input=input_text,
                previous_response_id=last_response_id,
            )
            print(f"\nResponse:\n{response.output_text}")
            last_response_id = response.id 
    except Exception as ex:
        print(ex)