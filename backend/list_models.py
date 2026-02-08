import google.generativeai as genai
import os

# MANUAL ENV LOADING
env_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                if not os.environ.get(key):
                    os.environ[key] = value

print(f"Key loaded: {bool(os.environ.get('GEMINI_API_KEY'))}")
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

try:
    print("Listing models...")
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if m.name.startswith("models/gemini"):
                print(m.name)
                count += 1
                if count >= 5:
                    break
except Exception as e:
    print(f"Error listing models: {e}")
