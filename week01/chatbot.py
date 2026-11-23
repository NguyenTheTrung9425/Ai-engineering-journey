import os, json,  time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv() # Load environment variables from a .env file
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.5-flash-lite"

history = []
def ask_gemini(history):

    contents = []
    for h in history:
        contents.append({"role": h["role"], "parts": [{"text": h["content"]}]})
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents
            )
            return response.text
        except errors.ServerError as e:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"[Lỗi {e.code}] Thử lại lần {attempt + 1} sau {wait_time} giây...")
            time.sleep(wait_time)  # Wait for the exponential backoff time before retrying
    return "Xin lỗi, sever đang quá tải. Vui lòng thử lại sau."


def save_history(history):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    


while True:
    user_input = input("You: ")
    if user_input in ["exit", "quit"]:
        break
    
    history.append({"role": "user", "content": user_input})
    reply = ask_gemini(history)
    history.append({"role": "model", "content": reply})
    
    save_history(history)
    print(f"Gemini: {reply}")




    