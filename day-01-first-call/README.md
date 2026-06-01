# Day 01: First LLM API Call

Run the first Poe OpenAI-compatible LLM API call.

```bash
cd examples/llm-basic/day-01-first-call
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
set -a
source .env
set +a
python main.py
```

The API key is read from `POE_API_KEY`.

