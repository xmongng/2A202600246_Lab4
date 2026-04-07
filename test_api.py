import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

client = ChatNVIDIA(
  model="openai/gpt-oss-120b",
  api_key=os.getenv("NVIDIA_API_KEY"), 
  temperature=1,
  top_p=1,
  max_tokens=4096,
)

print("Streaming response:")
for chunk in client.stream([{"role": "user", "content": "Hello, how are you?"}]):
  if hasattr(chunk, 'additional_kwargs') and "reasoning_content" in chunk.additional_kwargs:
    print(chunk.additional_kwargs["reasoning_content"], end="")
  print(chunk.content, end="")
print()
