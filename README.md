

## 🤖 Liar AI Agent (Gemini API)

This script creates an AI agent that **intentionally lies** in response to user input using the **Gemini API** via an OpenAI-compatible wrapper.

### 📦 Requirements

* Python 3.8+
* `.env` file with:

  ```
  KEY=your_gemini_api_key
  ```

### 🚀 Run

```bash
uv run go
```

### 🔧 Tech Used

* Gemini 2.0 Flash (OpenAI-style)
* `dotenv`, `colorama`
* Custom `Agent`, `Runner`, `RunConfig` from `agents` module

### ⚠️ Note

Agent is **intentionally misleading** — useful for testing, reverse psychology bots, etc.
