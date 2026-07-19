# 🛫 AI Travel Agent — Free LLM Edition

A Streamlit app that researches and plans a personalized travel itinerary using
two AI agents (Researcher + Planner) — running entirely on **free APIs**:

- **LLM**: any OpenAI-compatible free provider from [freellm.net](https://freellm.net)
  (Groq, OpenRouter, Mistral, Cerebras, or a custom base URL)
- **Web search**: DuckDuckGo — no API key at all

Adapted from the original
[`ai_travel_agent`](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/starter_ai_agents/ai_travel_agent)
in awesome-llm-apps, which requires a paid OpenAI key (GPT-4o) plus a SerpAPI
key. This version needs **one free API key**, no credit card.

## Quick Start

```bash
git clone https://github.com/boristrade/awesome-freellm-apis.git
cd awesome-freellm-apis/code-examples/ai-travel-agent
pip install -r requirements.txt
streamlit run travel_agent_free.py
```

1. Get a free key — fastest is [console.groq.com/keys](https://console.groq.com/keys)
   (email signup, no credit card). Other options: the
   [Quick Reference table](../../README.md#quick-reference--base-urls--api-keys).
2. In the sidebar, pick a provider preset (base URL + model ID are prefilled and
   editable) and paste your key.
3. Enter a destination and number of days, then hit **Generate Itinerary**.
4. Optionally download the result as an `.ics` calendar file.

## Preset providers

| Preset | Base URL | Default model | Credit card? |
|---|---|---|---|
| Groq | `https://api.groq.com/openai/v1` | `llama-3.3-70b-versatile` | No |
| OpenRouter | `https://openrouter.ai/api/v1` | `meta-llama/llama-3.3-70b-instruct:free` | No (registration) |
| Mistral AI | `https://api.mistral.ai/v1` | `mistral-small-latest` | No |
| Cerebras | `https://api.cerebras.ai/v1` | `llama-3.3-70b` | No |
| Custom | any OpenAI-compatible endpoint | — | — |

> The Researcher agent uses tool calling for web search, so pick a model that
> supports function calling (all defaults above do). If a provider rejects tool
> calls, switch models or presets in the sidebar — no code changes needed.

## What changed vs. the original

| | Original | Free edition |
|---|---|---|
| LLM | OpenAI GPT-4o (paid) | Any free OpenAI-compatible API (`OpenAILike`) |
| Web search | SerpAPI (key required) | DuckDuckGo (`ddgs`, no key) |
| Keys needed | 2 (OpenAI + SerpAPI) | 1 (free LLM provider) |

Everything else — the two-agent Researcher/Planner flow and the `.ics` calendar
export — is unchanged.
