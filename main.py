from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chat import conversational_rag_chain

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/chat")
def chat_endpoint(chat_request: ChatRequest):
    try:
        response = conversational_rag_chain.invoke(
            {"input": chat_request.question},
            config={"configurable": {"session_id": "abc123"}}
        )["answer"]
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
