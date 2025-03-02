import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the conversational_rag_chain with error handling
try:
    from chat_invoke import conversational_rag_chain
    logger.info("Successfully imported conversational_rag_chain")
except ImportError as e:
    logger.error(f"Failed to import conversational_rag_chain: {e}")
    # Define a mock if import fails (for development)
    class MockChain:
        def invoke(self, *args, **kwargs):
            return {"answer": "This is a mock response. The actual chain couldn't be loaded."}
    conversational_rag_chain = MockChain()

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: connections, load models, etc.
    logger.info("Application startup")
    try:
        # Add any initialization code here
        logger.info("Initialization completed")
    except Exception as e:
        logger.error(f"Startup error: {e}")
    
    yield  # This is where the application runs
    
    # Shutdown logic
    logger.info("Application shutdown")

# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Hello World", "status": "operational"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest, request: Request):
    logger.info(f"Received chat request: {chat_request.question[:50]}...")
    
    try:
        # Get client IP for logging
        client_host = request.client.host if request.client else "unknown"
        logger.info(f"Processing request from {client_host}")
        
        # Process the request
        response = conversational_rag_chain.invoke(
            {"input": chat_request.question},
            config={"configurable": {"session_id": "abc123"}}
        )
        
        # Check if response contains the expected answer
        if isinstance(response, dict) and "answer" in response:
            answer = response["answer"]
            logger.info(f"Successfully generated response of length: {len(answer)}")
            return {"answer": answer}
        else:
            logger.error(f"Unexpected response format: {type(response)}")
            return {"answer": "An error occurred: Unexpected response format", "error": True}
            
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Railway and Render specific PORT handling
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment for Railway/Render compatibility
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"Starting server on port {port}")
    
    # Use these settings for production
    uvicorn.run(
        "main:app",  # Assuming this file is named main.py
        host="0.0.0.0",
        port=port,
        workers=int(os.environ.get("WEB_CONCURRENCY", 1)),
        log_level="info",
        reload=False  # Set to False in production
    )