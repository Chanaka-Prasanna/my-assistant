from fastapi import FastAPI, Request
from pydantic import BaseModel
from chat_invoke import conversational_rag_chain

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
    uvicorn.run(app, host="0.0.0.0", port=8000)