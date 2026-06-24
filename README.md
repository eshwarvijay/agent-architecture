# agent-architecture

A **tool-agnostic knowledge base for designing AI agents** — the 21 agentic
design patterns from Antonio Gulli's *Agentic Design Patterns: A Hands-On Guide
to Building Intelligent Systems*, distilled to **concepts only (no code)** so they
apply to any framework, language, or AI coding assistant.

It answers *which* patterns an agent needs and *why*. Implement the *how* in your
own stack — LangChain / LangGraph, CrewAI, AutoGen, LlamaIndex, Semantic Kernel,
the Anthropic / OpenAI / Gemini SDK directly, or Google ADK.

## What's inside

```
SKILL.md          # index — every pattern's purpose + when-to-use (Claude Code entry point)
AGENTS.md         # same index pointer for Codex / Cursor / Antigravity / Gemini CLI
patterns/         # 21 pattern files: overview, mechanics, use cases, trade-offs, pitfalls, refs
appendices/       # prompting techniques, frameworks overview, GUI/CLI/coding agents, AgentSpace
conclusion.md     # how patterns combine (worked multi-pattern example)
glossary.md       # core term definitions
.cursor/rules/    # Cursor auto-attach rule
```

Plain markdown throughout — readable on GitHub, in any editor, or pasted into any chat.

## Use it with your tool

It works two ways with **every** tool: an *automatic* pointer (the agent reads
the relevant pattern file on its own when the task is about agent design), or a
*manual* `@`-mention / paste. Pointers are already included in this repo:

| Tool | Automatic | Notes |
|------|-----------|-------|
| **Claude Code** | `SKILL.md` | Symlink into `~/.claude/skills/` (see below), then invoke by topic. |
| **Codex** | `AGENTS.md` | Read automatically when the repo is the working dir. |
| **Cursor** | `.cursor/rules/agent-architecture.mdc` + `AGENTS.md` | Rule attaches by description match; no token cost until triggered. |
| **Antigravity** | `AGENTS.md` | Also add the repo folder to its Knowledge/context panel. |
| **Gemini CLI / others** | `AGENTS.md` | Most agent CLIs honor the `AGENTS.md` convention. |
| **Any chatbot (no setup)** | — | Open `SKILL.md` + the pattern file on GitHub, paste, or `@`-mention it. |

### Claude Code
```sh
git clone <this-repo> ~/agent-architecture
ln -s ~/agent-architecture ~/.claude/skills/agent-architecture
```
Then ask anything agent-design-shaped ("which pattern for…", "design an agent that…").

### Codex / Cursor / Antigravity / other AGENTS.md tools
Open this repo (or add it as a folder/submodule of your project). The agent will
read `AGENTS.md` and pull in the relevant `patterns/*.md` when you ask it to
design agent architecture. To use it *inside another project*, copy or symlink
this folder in, or `git submodule add` it.

### Manual (works anywhere)
Just point your assistant at the files: "Read `SKILL.md` and
`patterns/04-reflection.md`, then propose a design for X."
