import json
import os
from dotenv import load_dotenv
import google.genai as genai
import requests

load_dotenv()

# --- INITIALIZATION ---
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def validate_config():
    if LLM_PROVIDER == "gemini":
        if not GEMINI_API_KEY or "your-api-key" in GEMINI_API_KEY:
            print("❌ Error: Valid GEMINI_API_KEY not found in .env")
            exit(1)
        return genai.Client(api_key=GEMINI_API_KEY)
    elif LLM_PROVIDER == "groq":
        if not GROQ_API_KEY or "your-groq-key" in GROQ_API_KEY:
            print("❌ Error: Valid GROQ_API_KEY not found in .env")
            exit(1)
        return None
    else:
        print(f"❌ Error: Unsupported provider '{LLM_PROVIDER}'")
        exit(1)

client = validate_config()

# --- TOOLS ---
def save_to_memory(key, value):
    """Saves a piece of information to memory."""
    memory = {}
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            memory = json.load(f)
    memory[key] = value
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)
    return f"Saved: {key} = {value}"

def get_from_memory(key):
    """Retrieves a piece of information from memory."""
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            return json.load(f).get(key, "Not found.")
    return "Memory empty."

TOOLS = {"save_to_memory": save_to_memory, "get_from_memory": get_from_memory}

def handle_tool_call(response):
    """Parses and executes tool calls found in the response string."""
    try:
        if "{" in response and "}" in response:
            data = json.loads(response[response.find("{"):response.rfind("}")+1])
            tool_name = data.get("tool")
            if tool_name in TOOLS:
                args = {k: v for k, v in data.items() if k != "tool"}
                print(f"⚙️  Executing {tool_name}...")
                return TOOLS[tool_name](**args)
    except Exception:
        pass
    return None

# --- MODEL INTERFACE ---
def call_model(user_message):
    system_prompt = """You are IronClaw. Available tools:
1. save_to_memory(key, value)
2. get_from_memory(key)
Format tool calls as JSON: {"tool": "save_to_memory", "key": "...", "value": "..."}"""

    prompt = f"{system_prompt}\n\nUser: {user_message}"

    if LLM_PROVIDER == "gemini":
        resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return getattr(resp, "text", str(resp))
    
    # Groq provider
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json=payload
    )
    data = resp.json()
    return data["choices"][0]["message"]["content"] if "choices" in data else json.dumps(data)

# --- INTERFACE ---
def run_agent():
    print(f"🤖 IronClaw Online ({LLM_PROVIDER}). Type 'exit' to stop.\n")
    while True:
        text = input("You: ").strip()
        if text.lower() in ["exit", "quit"]: break
        if not text: continue

        try:
            response = call_model(text)
            print(f"🤖 IronClaw: {response}\n")
            
            tool_result = handle_tool_call(response)
            if tool_result:
                print(f"🛠️ Tool Result: {tool_result}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    run_agent()