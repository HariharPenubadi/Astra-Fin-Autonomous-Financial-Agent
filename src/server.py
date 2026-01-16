from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio

from src.graph.astra_graph import build_graph

# Initialize
app = FastAPI(title="Astra Fin API")

# Allow React to talk to Python (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Brain
graph = build_graph()


class ChatRequest(BaseModel):
    query: str


async def event_generator(query: str):
    """
    Streams events (Brain, Memory, Advisor) to the frontend
    in Server-Sent Events (SSE) format.
    """
    inputs = {"query": query}

    try:
        async for chunk in graph.astream(inputs, stream_mode="updates"):
            for node, values in chunk.items():
                data = {}

                # 1. BRAIN (Planner)
                if node == "planner":
                    data = {
                        "type": "brain",
                        "content": f"Intent: {values.get('intent', 'unknown').upper()}"
                    }

                # 2. MEMORY (Profile)
                elif node == "investor_profile":
                    if values.get("profile_updated"):
                        p = values.get("investor_profile", {})
                        data = {
                            "type": "memory",
                            "content": f"Budget: {p.get('budget')} {p.get('currency')} | Risk: {p.get('risk')}"
                        }

                # 3. ADVISOR / AGENT (Final Answer)
                elif node in ["advisor", "finance_agent", "reasoner"]:
                    # Check if it's a final answer
                    if "answer" in values:
                        data = {
                            "type": "response",
                            "content": values["answer"]
                        }

                if data:
                    # SSE Format: "data: {json}\n\n"
                    yield f"data: {json.dumps(data)}\n\n"
                    # Small delay to ensure React renders smoothly
                    await asyncio.sleep(0.05)

    except Exception as e:
        err = {"type": "error", "content": str(e)}
        yield f"data: {json.dumps(err)}\n\n"


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    return StreamingResponse(event_generator(req.query), media_type="text/event-stream")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)