import os
from dotenv import load_dotenv


# import namespaces for async
from openai import OpenAI
# from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider

def code_interpreter_tool(): 

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    # credentials = None
    async_client = None 
    try:
        # Get configuration settings 
        _:bool = load_dotenv()
        azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        model_deployment: str = os.getenv("MODEL_DEPLOYMENT", "")
        api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
        if not model_deployment:
            raise ValueError("MODEL_DEPLOYMENT environment variable is not set")

        # Initialize an async OpenAI client
        # credentials = DefaultAzureCredential()
        # token_provider = get_bearer_token_provider(
        # credentials, "https://ai.azure.com/.default"
        # )
        async_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=api_key
        ) 
        

        # Track responses
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Await an asynchronous response
            response = async_client.responses.create(
                model=model_deployment,
                instructions="""You are an expert software engineer with extensive experience in Python, JavaScript, 
                                TypeScript, C#, Java, SQL, cloud technologies, APIs, and modern software architecture.

                                Your responsibilities include:
                                - Writing clean, efficient, maintainable, and well-documented code.
                                - Explaining technical concepts clearly.
                                - Identifying bugs and proposing reliable fixes.
                                - Following language-specific best practices and design patterns.
                                - Prioritizing readability and maintainability over clever solutions.
                                - Explaining why a solution works, not just what to type.
                                - Asking clarifying questions when requirements are incomplete.

                                When generating code:
                                - Produce complete and runnable examples whenever possible.
                                - Include comments only where they improve understanding.
                                - Mention assumptions and limitations.
                                - Consider security, performance, and error handling.""",
                                tools=[{"type":"code_interpreter","container":{"type":"auto"}}],
                input=input_text,
                previous_response_id=last_response_id,
            )
            print(f"\nResponse:\n{response.output_text}")
            last_response_id = response.id  # Update the last response ID for context
            

    except Exception as ex:
        print(ex)

    finally:
        # Close the async client session
        # if async_client:
        #     await async_client.close()
        pass
        