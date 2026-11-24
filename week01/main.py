import os, time
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException   
from pydantic import BaseModel
from google import genai
from google.genai import errors
from groq import Groq

load_dotenv() # Load environment variables from a .env file
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

gemini_model = "gemini-3.5-flash-lite"
groq_model = "openai/gpt-oss-20b"

app = FastAPI(title = "AI Chatbot API")

session = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    model_used: str

def ask_gemini(history):
    contents = []
    for h in history:
        contents.append({"role": h["role"], "parts": [{"text": h["content"]}]})
    for attempt in range(3):
        try:
            response = gemini_client.models.generate_content(
                model=gemini_model,
                contents=contents
            )
            return response.text
        except errors.ServerError as e:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"[Lỗi {e.code}] Thử lại lần {attempt + 1} sau {wait_time} giây...")
            time.sleep(wait_time)  # Wait for the exponential backoff time before retrying
    return "Xin lỗi, sever đang quá tải. Vui lòng thử lại sau."

def ask_groq(history):
    messages = []
    for h in history:
        role = "assistant" if h["role"] == "model" else "user"
        messages.append({"role": role, "content": h["content"]})
    response = groq_client.chat.completions.create(
        model=groq_model,
        messages=messages
    )
    return response.choices[0].message.content

def get_ai_reply(history):
    try:
        reply = ask_gemini(history)
        return reply, "Gemini"
    except Exception as e:
        print(f"Gemini API error: {e}. Falling back to Groq.")
        try:
            reply = ask_groq(history)
            return reply, "Groq"
        except Exception as e:
            print(f"Groq API error: {e}. No AI response available.")
            raise HTTPException(status_code=503, detail="Both AI services are unavailable. Please try again later.")


@app.get("/")
def home():
    return {"message": "Server đang chạy ngon lành!"}
@app.post("/chat", response_model=ChatResponse)

def chat_endpoint(req: ChatRequest):

    if req.session_id not in session:
        session[req.session_id] = []

    user_history = session[req.session_id]
    user_history.append({"role": "user", "content" : req.message})

    bot_reply, model_used = get_ai_reply(user_history)
    user_history.append({"role": "model", "content" : bot_reply})
    return ChatResponse(session_id=req.session_id, reply=bot_reply, model_used=model_used)

 
