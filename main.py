import json
import os

# --- 1. THE TOOLS (The "Hands") ---
def save_to_memory(key, value):
    """Saves a piece of information to the agent's long-term memory."""
    memory = {}
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            memory = json.load(f)
    
    memory[key] = value
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)
    return f"Successfully remembered that {key} is {value}."

def get_from_memory(key):
    """Retrieves a piece of information from memory."""
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            memory = json.load(f)
            return memory.get(key, "I don't remember that yet.")
    return "Memory file is empty."

# The Tool Registry (The Dispatcher Map)
tools_map = {
    "save_to_memory": save_to_memory,
    "get_from_memory": get_from_memory
}

# --- 2. THE EXECUTOR (The "Bridge") ---
def executor(tool_call):
    name = tool_call["name"]
    args = tool_call["arguments"] # This is a dictionary
    
    print(f"⚙️  System: Executing tool '{name}'...")
    
    func = tools_map.get(name)
    if func:
        # Using the ** unpacking we discussed!
        return func(**args)
    return "Error: Tool not found."

# --- 3. THE GATEWAY (The "Interface") ---
def run_agent():
    print("🤖 Mini-OpenClaw Online. Type 'exit' to stop.")
    
    # In a real app, you'd initialize your LLM client here
    # client = OpenAI(api_key="your-key")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # SIMULATED LLM LOGIC: 
        # In a real script, you'd send 'user_input' to the LLM.
        # If the LLM decides to use a tool, it returns a JSON object.
        
        # Example: If user says "Remember my name is Alex"
        if "remember" in user_input.lower():
            # Simulated Tool Call from LLM
            mock_tool_call = {
                "name": "save_to_memory",
                "arguments": {"key": "user_name", "value": user_input.split("is ")[-1]}
            }
            result = executor(mock_tool_call)
            print(f"Agent: {result}")
        
        elif "who am i" in user_input.lower():
            mock_tool_call = {
                "name": "get_from_memory",
                "arguments": {"key": "user_name"}
            }
            result = executor(mock_tool_call)
            print(f"Agent: Your name is {result}")
            
        else:
            print("Agent: I'm listening! (Try telling me to 'remember' something).")

if __name__ == "__main__":
    run_agent()