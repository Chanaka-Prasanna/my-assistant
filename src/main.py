from pydantic import BaseModel
from chat_invoke import conversational_rag_chain
import os

# This function will be executed every time your Appwrite function is triggered
def main(context):
    # Parse incoming request
    body = context.req.json  # Retrieve JSON payload from request
    path = context.req.path  # Get the path of the request
    
    # Define response structure
    def json_response(data, status=200):
        return context.res.json(data, status)

    # Define models and logic
    class ChatRequest(BaseModel):
        question: str

    if path == "/chat":
        try:
            # Validate and parse incoming request
            chat_request = ChatRequest(**body)
            question = chat_request.question

            # Call your chain logic here
            response = conversational_rag_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": "abc123"}}
            )["answer"]

            # Return the result
            return json_response({"answer": response})
        except Exception as e:
            # Handle errors
            return json_response({"error": str(e)}, status=500)
    
    if path == "/":
        return json_response({"message": "Hello World"})
    
    # Default for unsupported paths
    return json_response({"error": "Not Found"}, status=404)
