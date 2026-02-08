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

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

with open("safe_models.txt", "w") as f:
    try:
        f.write("Listing models...\n")
        count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if m.name.startswith("models/gemini"):
                    f.write(m.name + "\n")
                    count += 1
                    if count >= 10:
                        break
    except Exception as e:
        f.write(f"Error: {e}\n")
