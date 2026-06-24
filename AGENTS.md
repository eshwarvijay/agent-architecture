# AGENTS.md

This repository is a **conceptual knowledge base for designing AI agents** — the
21 agentic design patterns from Antonio Gulli's *Agentic Design Patterns*,
distilled to concepts only (no code), so they apply to any framework or language.

`AGENTS.md` is an open, cross-tool convention read by Codex, Cursor, Antigravity,
Gemini CLI, and others. Claude Code uses `SKILL.md` (same content, different entry
point). Both point at the same files below.

## For any AI coding agent reading this repo

When the task involves **designing or reasoning about AI-agent architecture**
(which patterns to use, their trade-offs, how patterns combine):

1. Read `SKILL.md` — the index: every pattern's purpose and when to use it.
2. Read the relevant `patterns/<nn>-<name>.md` for depth on a chosen pattern.
3. Supporting material: `appendices/` (prompting techniques, frameworks),
   `conclusion.md` (worked multi-pattern example), `glossary.md` (terms).

These files are **concepts, not code**. Implement them in whatever stack the
user's project uses — LangChain / LangGraph, CrewAI, AutoGen, LlamaIndex,
Semantic Kernel, the Anthropic / OpenAI / Gemini SDK directly, or Google ADK.
The pattern is the design; the framework is just the dialect.

> Source snapshot: mid-2025. The patterns don't expire, but concrete model IDs /
> API details mentioned in the text may be dated — verify those against current docs.
