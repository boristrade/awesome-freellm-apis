# Claude Code (cc) — Free LLM API Config

Run Claude Code on a free backend by pointing it at an **Anthropic-compatible** API.

## How It Works

Claude Code speaks the **Anthropic Messages API** — it sends requests to
`${ANTHROPIC_BASE_URL}/v1/messages` in Anthropic's format, not OpenAI's. So the
backend you point it at has to understand that format. The cleanest free option
is **OpenRouter**, which exposes a native Anthropic-compatible endpoint.

Claude Code reads three environment variables:

- `ANTHROPIC_BASE_URL` — the Anthropic-compatible host (cc appends `/v1/messages`)
- `ANTHROPIC_AUTH_TOKEN` — your provider key (sent as the bearer token)
- `ANTHROPIC_API_KEY` — must be **empty**, or cc prefers it over the auth token

## Quick Config

### OpenRouter (recommended — native Anthropic endpoint)

```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"   # cc appends /v1/messages
export ANTHROPIC_AUTH_TOKEN="sk-or-v1-your_openrouter_key"
export ANTHROPIC_API_KEY=""                             # must be empty
```

Get your key at [openrouter.ai/keys](https://openrouter.ai/workspaces/default/keys).

Set the model with `ANTHROPIC_MODEL` (and optionally `ANTHROPIC_SMALL_FAST_MODEL`
for background tasks):

```bash
export ANTHROPIC_MODEL="anthropic/claude-sonnet-4.5"
export ANTHROPIC_SMALL_FAST_MODEL="anthropic/claude-haiku-4.5"
```

> **Note:** Running Anthropic models through OpenRouter requires a one-time **$10
> account top-up** to unlock the higher request tier. Free (`:free`) models on
> OpenRouter work without a top-up, but Claude Code leans on tool use and long
> context, so a capable model gives the best results.

## Using an OpenAI-compatible provider (Groq, NVIDIA, SiliconFlow, …)

Most free providers in this repo (Groq, NVIDIA NIM, SiliconFlow, Cerebras, etc.)
only expose an **OpenAI-compatible** endpoint. Claude Code can't talk to those
directly — the request/response shapes differ. To use them you need a small
translation proxy that converts between the Anthropic and OpenAI formats:

- [claude-code-router](https://github.com/musistudio/claude-code-router) — purpose-built for this
- [LiteLLM](https://github.com/BerriAI/litellm) — run it as an Anthropic-compatible proxy

Point `ANTHROPIC_BASE_URL` at the proxy, and the proxy at your free provider's
OpenAI endpoint (see the [Quick Reference](../README.md#quick-reference--base-urls--api-keys)
for each provider's base URL and key link).

## Persistent Config

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Free LLM backend for Claude Code (OpenRouter, Anthropic-compatible)
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="sk-or-v1-your_key_here"
export ANTHROPIC_API_KEY=""
export ANTHROPIC_MODEL="anthropic/claude-sonnet-4.5"
```

## Caveats

- Claude Code relies heavily on tool use and large context. Weaker models may fail
  on agentic tasks — prefer a capable model (Claude Sonnet/Haiku via OpenRouter, or
  Llama 3.3 70B+ / DeepSeek R1 through a proxy).
- Leave `ANTHROPIC_API_KEY` empty. If it's set, cc uses it instead of
  `ANTHROPIC_AUTH_TOKEN` and your provider key is ignored.
- Free tiers have rate limits. OpenRouter free models: ~50 RPD; with a $10 top-up: 1,000 RPD.

## More Configs

Visit [freellm.net/config/claude-code/](https://freellm.net/config/claude-code/) for the interactive config generator with all free models.
