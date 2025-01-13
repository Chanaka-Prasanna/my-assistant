from fastapi import FastAPI, Request
from pydantic import BaseModel
from chat_invoke import conversational_rag_chain
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

@app.get("/")
async def root():
    return {"message": "Hello World"}