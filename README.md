# Mini-OpenClaw AI Agent

This repository contains a simple Python-based interactive agent named **Mini-OpenClaw**. The project demonstrates a basic architecture for a chatbot-like system that can remember and recall information using a local JSON "memory" store.

## Overview

The agent is split into three logical sections:

1. **Tools (The "Hands")**
   - `save_to_memory(key, value)` stores a key-value pair in a local `memory.json` file.
   - `get_from_memory(key)` retrieves a value for a given key from `memory.json`.
   - A `tools_map` dictionary registers the available functions for dispatch.

2. **Executor (The "Bridge")**
   - The `executor(tool_call)` function receives a tool call object and invokes the corresponding tool with the provided arguments. It handles dispatch and prints a log message.

3. **Gateway (The "Interface")**
   - The `run_agent()` function runs a simple command-line loop, simulating communication with an LLM. For demonstration purposes, the code interprets phrases containing "remember" or "who am i" as requests to use the memory tools.

The script can be run directly with Python. It uses a simulated LLM logic where certain user inputs trigger tool calls.

## Usage

1. **Install Python** (version 3.7+ recommended).
2. **Run the agent**:
   ```bash
   python main.py
   ```
3. **Interact with the agent**:
   - Type a sentence containing the word "remember" such as `Remember my name is Alex`.
   - Ask `Who am I?` to have the agent recall the stored name.
   - Enter `exit` or `quit` to terminate the program.

## Files

- `main.py` - The core Python script containing the agent logic.
- `memory.json` (created at runtime) - Stores memory key-value pairs persisted between sessions.

## Extending the Agent

This prototype can be extended by hooking up a real LLM API instead of the simulated logic, adding more tools, or implementing more advanced memory management and conversational capabilities.

## License

This project is provided as-is for educational purposes. Feel free to modify and expand upon it.