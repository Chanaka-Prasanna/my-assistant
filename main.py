import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chat_invoke import conversational_rag_chain

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

# Get PORT from Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if not set
    uvicorn.run(app, host="0.0.0.0", port=port)
