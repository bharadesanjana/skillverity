from app.config import settings
import google.generativeai as genai
import os

print(f"API_KEY from settings: {settings.GEMINI_API_KEY}")
print(f"API_KEY length: {len(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else 0}")

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    print("GenAI configured successfully.")
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Model initialized.")
except Exception as e:
    print(f"GenAI configuration failed: {e}")
