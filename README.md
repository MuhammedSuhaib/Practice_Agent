# Web Search Agent

Python agent that can search the web using DuckDuckGo or Tavily API.  

## Requirements
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Environment variables in `.env`:
```

GEMINI_API_KEY=your_key
Tracing_key=your_key
Tavily_API_KEY=your_key

````

## Run

```bash
uv run go
```

Type queries in the prompt.
Type `off` to exit.

