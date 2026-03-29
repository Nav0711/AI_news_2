import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key present: {bool(api_key)}")
if api_key:
    genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say 'ok' in one word only")
    print("1.5-flash Success!")
except Exception as e:
    print(f"1.5-flash Error: {e}")

try:
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Say 'ok' in one word only")
    print("2.0-flash Success!")
except Exception as e:
    print(f"2.0-flash Error: {e}")

try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Say 'ok' in one word only")
    print("2.5-flash Success!")
except Exception as e:
    print(f"2.5-flash Error: {e}")
