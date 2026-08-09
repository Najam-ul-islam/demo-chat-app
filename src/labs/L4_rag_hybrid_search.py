import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


# ============================================================
# Load environment
# ============================================================

load_dotenv()


# ============================================================
# Configuration
# ============================================================

FOUNDRY_PROJECT_ENDPOINT = os.getenv(
    "FOUNDRY_PROJECT_ENDPOINT"
)

FOUNDRY_AGENT_NAME = os.getenv(
    "FOUNDRY_AGENT_NAME"
)

FOUNDRY_AGENT_VERSION = os.getenv(
    "FOUNDRY_AGENT_VERSION"
)


if not FOUNDRY_PROJECT_ENDPOINT:
    raise RuntimeError(
        "Missing FOUNDRY_PROJECT_ENDPOINT"
    )

if not FOUNDRY_AGENT_NAME:
    raise RuntimeError(
        "Missing FOUNDRY_AGENT_NAME"
    )

if not FOUNDRY_AGENT_VERSION:
    raise RuntimeError(
        "Missing FOUNDRY_AGENT_VERSION"
    )


# ============================================================
# FastAPI
# ============================================================

app = FastAPI(
    title="Azure Foundry RAG Agent API",
    version="1.0.0",
)


# ============================================================
# Foundry Project Client
# ============================================================

project_client = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)


# ============================================================
# OpenAI-compatible client
# ============================================================

openai_client = project_client.get_openai_client()


# ============================================================
# Request model
# ============================================================

class AskRequest(BaseModel):
    question: str


# ============================================================
# Health check
# ============================================================

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Azure Foundry RAG Agent API",
        "agent": FOUNDRY_AGENT_NAME,
        "version": FOUNDRY_AGENT_VERSION,
    }


# ============================================================
# Ask Agent
# ============================================================

@app.post("/ask")
async def ask(request: AskRequest):

    try:

        response = openai_client.responses.create(
            input=[
                {
                    "role": "user",
                    "content": request.question,
                }
            ],
            extra_body={
                "agent_reference": {
                    "name": FOUNDRY_AGENT_NAME,
                    "version": FOUNDRY_AGENT_VERSION,
                    "type": "agent_reference",
                }
            },
        )

        return {
            "question": request.question,
            "answer": response.output_text,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Failed to communicate with Foundry agent",
                "error": str(e),
            },
        )
def run_agent():
    import uvicorn

    uvicorn.run(
        "src.labs.L4_rag_hybrid_search:app", reload=True)
