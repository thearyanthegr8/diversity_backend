from langchain_community.llms import Ollama

llm = Ollama(model="llama3:8b", base_url="http://localhost:11434")

response = llm.invoke("What is the oldest river in the world?")

print(response)