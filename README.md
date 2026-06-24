# agent-architecture

A **Claude Code skill** for designing AI agents — the 21 agentic design patterns
from Antonio Gulli's *Agentic Design Patterns: A Hands-On Guide to Building
Intelligent Systems*, distilled to **concepts only (no code)**.

It answers *which* patterns an agent needs and *why*. Implement the *how* in your
own stack — LangChain / LangGraph, CrewAI, the Anthropic / OpenAI / Gemini SDK
directly, or Google ADK.

## What's inside

```
SKILL.md          # index — every pattern's purpose + when-to-use (loads on invocation)
patterns/         # 21 pattern files: overview, mechanics, use cases, trade-offs, pitfalls, refs
appendices/       # prompting techniques, frameworks overview, GUI/CLI/coding agents, AgentSpace
conclusion.md     # how patterns combine (worked multi-pattern example)
glossary.md       # core term definitions
```

Plain markdown throughout — also readable straight on GitHub or pasted into any chat.

## Install (Claude Code)

```sh
git clone https://github.com/eshwarvijay/agent-architecture ~/agent-architecture
ln -s ~/agent-architecture ~/.claude/skills/agent-architecture
```

Then ask anything agent-design-shaped — "which pattern for…", "design an agent
that…", or name a pattern. The skill auto-loads its index and pulls in the
relevant `patterns/*.md` on demand.

### Manual (no install)

Point your assistant at the files directly: "Read `SKILL.md` and
`patterns/04-reflection.md`, then propose a design for X."
