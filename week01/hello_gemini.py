import os
from dotenv import load_dotenv
from google import genai

load_dotenv() # Load environment variables from a .env file
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Giải thích LLM là gì cho sinh viên năm 3 trong 3 câu."
)
print(response.text)