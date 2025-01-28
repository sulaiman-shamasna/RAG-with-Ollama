import requests
import os
import logging

class OllamaLLM:
    def __init__(self, model_name):
        self.api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        self.model_name = model_name

    def chat(self, prompt):
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        logging.info(f"Sending payload to Ollama: {payload}")

        response = requests.post(
            f"{self.api_url}/api/generate",
            json=payload
        )
        response.raise_for_status()
        return response.json()