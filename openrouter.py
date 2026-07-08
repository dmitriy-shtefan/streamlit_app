import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_openrouter(api_key, messages, model, temperature=0.7):
    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": temperature,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]