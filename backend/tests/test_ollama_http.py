import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": "Say hello in one sentence.",
        "stream": False
    }
)

print(response.status_code)
print(response.text)