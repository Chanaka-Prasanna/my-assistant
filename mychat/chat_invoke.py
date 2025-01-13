from mychat.chat import conversational_rag_chain

response = conversational_rag_chain.invoke(
    {"input": """
    I need social links of chanaka.
     """},
    config={
        "configurable": {"session_id": "abc123"}
    },  # constructs a key "abc123" in `store`.
)["answer"]

print(response)