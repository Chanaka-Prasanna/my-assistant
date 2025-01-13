from fastapi import FastAPI, Request
from pydantic import BaseModel
from mychat.chat_invoke import conversational_rag_chain
import os

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(request: ChatRequest):
    question = request.question

    response = conversational_rag_chain.invoke(
        {"input": question},
        config={
            "configurable": {"session_id": "abc123"}
        },
    )["answer"]

    return response

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )