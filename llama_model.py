# llama_model.py

import requests

def ask_ollama(prompt: str, model: str = "llama3") -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )

        data = response.json()
        print("🔍 Raw Ollama response:", data)  # Add this line for debugging

        # Safely return response if it exists
        return data.get("response", "⚠️ No 'response' key found in Ollama output.")

    except Exception as e:
        return f"❌ Error contacting Ollama: {e}"
