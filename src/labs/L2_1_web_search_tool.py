import os
from dotenv import load_dotenv
from openai import OpenAI

# Get configuration settings 
_:bool = load_dotenv()
azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
model_deployment: str = os.getenv("MODEL_DEPLOYMENT", "")
api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
if not model_deployment:
    raise ValueError("MODEL_DEPLOYMENT environment variable is not set")

def web_search_tool():
    """
    This function demonstrates the usage of a web search tool.
    It prompts the user for a search query, performs the search,
    and displays the results.
    """
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Prompt the user for a search query
    query = input("Enter your search query: ")
    print(f"Searching for: {query}")

    async_client = OpenAI(
        base_url=azure_openai_endpoint,
        api_key=api_key
    ) 

    last_response_id = None  # Initialize the last response ID for context
 
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
                                tools = [{"type":"web_search_preview"}],
                                input=query,
                                previous_response_id=last_response_id,
    )
    print(f"\nResponse:\n{response.output_text}")
    last_response_id = response.id  # Update the last response ID for context
