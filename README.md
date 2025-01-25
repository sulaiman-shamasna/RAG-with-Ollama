# RAG-with-Ollama

<div align="center">
  <img src="logo/ollama.png" alt="Ollama-Logo">
</div>

### General Info.
---
The main motivation of the model is to run the RAG system using ```òllama``` framework and test the newest models, namely ```DeepSeek-R1``` and other multimodal models! In the current version, however, it uses ```OpenAI's``` GPT models, thus, an ```Openai API key``` is required. This, however, will be updated really soon!

Therefore, for the moment, please create a ```.env``` file and put your ```OPENAI_API_KEY``` right there!

### How it works:

- Build the Docker image using the command:
    ```bash
    docker build -f Dockerfile.dev -t sulaiman/ollama-rag:latest .
    ```
- Then run the container using the command:
    ```bash
    docker run --name OLLAMARAGX -v ${PWD}:/app -v ${PWD}/vectorstore:/vectorstore -p 8600:8501 sulaiman/ollama-rag:latest
    ```

Note that on ```Windows``` machine, the volume command ```${PWD}``` might not be working properly. So, you can simple replace the command with the proper ````docker-compose.yml``` file, this way it works, for sure! ... I'll prepare it anyway once I refactor it with ```ollama```.

**Engoy!**