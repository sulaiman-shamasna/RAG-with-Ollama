# RAG-with-Ollama-and-OpenAI
---
Explore most recent models of **OpenAI**, **Llama**, and **DeepSeek**, et. al.

<div align="center">
  <img src="logo/openai.svg" alt="OpenAI Logo" width="150" hspace="15">
  <img src="logo/ollama.png" alt="Ollama Logo" width="120" hspace="15">
  <img src="logo/deepseek.png" alt="DeepSeek Logo" width="160" hspace="15">
</div>

### General Info.
---
The main motivation of the model is to run the RAG system using ```òllama``` framework and test the newest models, namely ```DeepSeek-R1``` and other multimodal models! In the current version, however, it uses ```OpenAI's``` GPT models, thus, an ```Openai API key``` is required. This, however, will be updated really soon!

Therefore, for the moment, please create a ```.env``` file and put your ```OPENAI_API_KEY``` right there!

### How it works:

- Build the Docker image using the command:
    ```bash
    docker build -f Dockerfile.openai -t sulaiman/ollama-rag:latest .
    ```
- Then run the container using the command:
    ```bash
    docker run --name OLLAMARAGs -v ${PWD}:/app -v ${PWD}/vectorstore:/vectorstore -p 8600:8501 sulaiman/ollama-rag:latest
    ```

Note that on ```Windows``` machine, the volume command ```${PWD}``` might not be working properly (if ```GitBash```). So, you can simple replace the command with the proper ```docker-compose.yml``` file, this way it works, for sure! ... I'll prepare it anyway once I refactor it with ```ollama```. It actually works with ```PowerShell``` 

**Engoy!**


```shell
docker build -f Dockerfile.openai -t sulaiman/openai-rag:latest .
```

```shell
docker run --name OPENAIRAG -v ${PWD}:/app -v ${PWD}/vectorstore:/vectorstore -p 8600:8501 sulaiman/openai-rag:latest
```