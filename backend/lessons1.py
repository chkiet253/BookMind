import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

input_messages = [
    {
        "role": "user",
        "content": "Why is the sky blue?"
    }
]

response = client.responses.create(
    model="qwen/qwen-2.5-7b-instruct",
    instructions="Repsond like an Artist",
    input=input_messages,
    reasoning = {
        
    }
)

print(response.output_text)

# full_response = ""

# for event in response:
#     if event.type == 'response.output_text.delta':
#         print(event.delta, end="", flush=True)
#         full_response += event.delta

# print("\nFull response: ", full_response)