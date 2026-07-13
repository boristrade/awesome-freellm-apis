# Claude Code (cc) — Free LLM API Config

Run Claude Code through an **Anthropic-compatible** API. The simplest path is
OpenRouter's native Anthropic endpoint.

## How It Works

Claude Code speaks the **Anthropic Messages API** — it POSTs to
`${ANTHROPIC_BASE_URL}/v1/messages` in Anthropic's format, not OpenAI's. So the
backend has to understand that format. OpenRouter exposes a native
Anthropic-compatible endpoint, so cc works against it directly.

> **Note:** Only **paid Anthropic Claude models** are served over OpenRouter's
> Anthropic endpoint (e.g. `claude-sonnet-4.6`, `claude-opus-4`). Free (`:free`)
> and non-Anthropic models are **not** reachable this way — for those, see
> [OpenAI-compatible providers](#using-a-free-openai-compatible-provider) below.

Claude Code reads three environment variables:

- `ANTHROPIC_BASE_URL` — the Anthropic-compatible host (cc appends `/v1/messages`)
- `ANTHROPIC_AUTH_TOKEN` — your provider key (sent as the bearer token)
- `ANTHROPIC_API_KEY` — must be **empty**, or cc prefers it over the auth token

## Quick Config — OpenRouter

Browse available Claude models at [openrouter.ai/models?q=anthropic](https://openrouter.ai/models?q=anthropic).

```bash
# Add to ~/.zshrc or ~/.bashrc
export OPENROUTER_API_KEY="<your-openrouter-api-key>"   # openrouter.ai/settings/keys
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"   # cc appends /v1/messages
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""                             # must be explicitly empty

# Optional: pin specific models for each role
# export ANTHROPIC_DEFAULT_SONNET_MODEL="anthropic/claude-sonnet-4.6"
# export ANTHROPIC_DEFAULT_HAIKU_MODEL="anthropic/claude-haiku-4.5"

# Then simply run:
claude
```

Get your key at [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys).
Anthropic models consume OpenRouter credits per token — top up your account to use them.

## Using a free OpenAI-compatible provider

Most free providers in this repo (Groq, NVIDIA NIM, SiliconFlow, Cerebras, etc.)
only expose an **OpenAI-compatible** endpoint. Claude Code can't talk to those
directly — the request/response shapes differ. To use them you need a small
translation proxy that converts between the Anthropic and OpenAI formats:

- [claude-code-router](https://github.com/musistudio/claude-code-router) — purpose-built for this
- [LiteLLM](https://github.com/BerriAI/litellm) — run it as an Anthropic-compatible proxy

Point `ANTHROPIC_BASE_URL` at the proxy, and the proxy at your free provider's
OpenAI endpoint (see the [Quick Reference](../README.md#quick-reference--base-urls--api-keys)
for each provider's base URL and key link).

## Caveats

- Only paid Anthropic Claude models work over OpenRouter's Anthropic endpoint.
  Use the proxy route above for free, non-Anthropic models.
- Leave `ANTHROPIC_API_KEY` empty. If it's set, cc uses it instead of
  `ANTHROPIC_AUTH_TOKEN` and your provider key is ignored.
- Claude Code relies heavily on tool use and large context — weaker models routed
  through a proxy may fail on agentic tasks. Prefer a capable model (Llama 3.3 70B+
  or DeepSeek R1).

## More Configs

Visit [freellm.net/config/claude-code/](https://freellm.net/config/claude-code/) for the interactive config generator with all free models.
