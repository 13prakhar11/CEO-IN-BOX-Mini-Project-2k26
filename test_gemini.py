import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("Auto-CEO"))

config = types.GenerateContentConfig(
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Write a short story about a robot learning to love.",
    config=config,
)

print(response.text)