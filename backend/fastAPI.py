import ollama
@app.get("/ai")
def ask_ai():

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": "What is FastAPI?"
            }
        ]
    )

    return {
        "answer": response["message"]["content"]
    }