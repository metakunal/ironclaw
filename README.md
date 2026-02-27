# IronClaw

A minimal Python agent using Gemini or Groq for LLM calls, with simple memory tools.

## Setup

1. Clone repository:
   ```bash
   git clone <your-repo-url>
   cd ironclaw
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env` and fill in your keys:
   ```bash
   cp .env .env.local
   # edit .env.local
   ```
   - `LLM_PROVIDER` should be `gemini` or `groq`.
   - For Gemini, set `GEMINI_API_KEY`.
   - For Groq, set `GROQ_API_KEY` and `GROQ_API_URL`.

5. Run the agent:
   ```bash
   python main.py
   ```

## Usage

Type a message and the agent will respond. You can ask it to remember things:

```
You: remember my name is Alex
Agent: Successfully remembered that user_data is Alex.
You: who am I?
Agent: Your name is Alex
```

To stop, type `exit` or `quit`.

## Git

Make sure to add and commit your changes, then push:

```bash
git add .
git commit -m "Initial commit with Gemini/Groq integration"
git push origin main
```

`.env` and other sensitive files are ignored by `.gitignore`.
