## Purpose
Give concise, actionable guidance so an AI coding agent can be productive immediately in this repository.

## Big picture (what this repo is)
- This project appears to be a LiveKit-based agent system that wires audio/video sessions to language & ML services via plugin wrappers. Key runtime pieces are expected in `agent.py` (entrypoint), `tools.py` (tool/plugin adapters), and `prompts.py` (prompt templates). The concrete integrations are listed in `requirements.txt` (LiveKit agents & plugins, OpenAI/Google connectors, `mem0ai` for memory, DuckDuckGo search, and audio plugins such as Silero and noise-cancellation).

## Key files to inspect or update
- `agent.py` — agent entrypoint and orchestration. If you need to add runtime wiring (plugin registration, event loops, LiveKit session handling), edit here.
- `tools.py` — implement tool adapters and wrappers for external services (search, memory, TTS/STT, plugin shims). Expose simple functions with clear inputs/outputs.
- `prompts.py` — store prompt templates and small template helpers. Prefer f-strings or simple format templates that accept a dict of variables.
- `requirements.txt` — authoritative list of runtime dependencies; update when adding plugin packages.

## Project-specific conventions and patterns
- Plugin-first design: new features are generally added as self-contained tools/plugins. Implement the adapter in `tools.py`, add the package to `requirements.txt` (if external), and register the tool from `agent.py`.
- Minimal surface area: keep each tool function small and return JSON-serializable results (dicts, lists, strings). Avoid side-effects during pure computation.
- Use environment variables for secrets/credentials (project uses common connectors — expect `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `LIVEKIT_API_KEY`/`LIVEKIT_URL`, etc.). Look for `.env` usage patterns and `python-dotenv` in `requirements.txt`.

## Integration points (discoverable from `requirements.txt`)
- LiveKit integrations (core runtime and session management).
- OpenAI / Google connectors — used for LLM calls.
- `mem0ai` — memory/cache layer; treat it as a datastore for conversational state.
- Search — DuckDuckGo as a lightweight web search fallback.
- Audio plugins — Silero, noise-cancellation, TTS/STT responsibilities live in plugin adapters.

## How to add or modify behavior (concrete steps)
1. Add any new external dependency to `requirements.txt` (pin versions when possible).
2. Implement a small adapter function in `tools.py` (name the function to reflect intent, e.g., `def ddg_search(query, limit=3):` returning a list of results).
3. Import and register the tool in `agent.py` where tools/plugins are assembled. Keep registration local to an init function so tests can import without side-effects.
4. Add prompt pieces to `prompts.py` if you need reusable templates; prefer small templates with explicit variable keys (no implicit global state).
5. Use `.env` (not committed) for credentials. Document required env names in `agent.py` top comments if you add new credentials.

## Examples (copyable patterns)
- Tool adapter skeleton (put in `tools.py`):

```py
def ddg_search(query, max_results=3):
    # return a list of dicts: [{"title":..., "snippet":..., "url":...}, ...]
    import requests
    # ...implementation using `requests` and DuckDuckGo API/wrapping
    return []
```

- Prompt template (put in `prompts.py`):

```py
BASE_SUMMARY_PROMPT = """
You are an assistant. Use the following context: {context}
Answer concisely.
"""

def render_summary(context: str) -> str:
    return BASE_SUMMARY_PROMPT.format(context=context)
```

## Developer workflows (what works now)
- Install deps: `python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`.
- Run: there is no implemented CLI yet, but the expected runner is `python agent.py` — implement a `if __name__ == '__main__'` guarded `main()` in `agent.py` to start the service.
- Debugging: add verbose logging to `agent.py` and run locally. Use environment variables to toggle verbose mode.

## Tests and CI
- No tests or CI config were discovered. If you add tests, keep them fast and side-effect free (mock external APIs). Prefer pytest and place tests under `tests/`.

## Assumptions & notes for AI agents (explicit)
- Several key source files (`agent.py`, `prompts.py`, `tools.py`) are currently empty placeholders. Assume their intended responsibilities as documented above. When implementing, keep changes minimal and add unit tests for non-trivial logic.
- Use the `requirements.txt` entries as the source of truth for installed capabilities and to infer which external services the project expects.

## When to ask the repo owner
- If you need real API keys, environment variable names, or LiveKit room details — ask the owner. Don't invent secrets or hard-code keys.

If any section is unclear or you want the guidance to be more prescriptive (e.g., provide a concrete `agent.py` starter implementation), tell me which part to expand and I will iterate.
