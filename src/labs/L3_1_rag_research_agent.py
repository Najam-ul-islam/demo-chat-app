# Before running the sample:
#    pip install azure-ai-projects>=2.1.0

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://najamcapricon88-3575-resource.services.ai.azure.com/api/projects/najamcapricon88-3575"

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "rag-research-agent"
my_version = "6"

openai_client = project_client.get_openai_client()
while True:
        input_text = input('\nEnter a prompt (or type "quit" to exit): ')
        if input_text.lower() == "quit":
            break
        if len(input_text) == 0:
            print("Please enter a prompt.")
            continue
        # Reference the agent to get a response
        response = openai_client.responses.create(
            input=[{"role": "user", "content": input_text}],
            extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
        )

        print(f"Response output: {response.output_text}")