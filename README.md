# agent-architecture

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-skill-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Code skill">
  <img src="https://img.shields.io/badge/patterns-21-5436DA?style=for-the-badge" alt="21 patterns">
  <img src="https://img.shields.io/badge/install-%2Fplugin-000000?style=for-the-badge&logo=anthropic&logoColor=white" alt="install via /plugin">
</p>

**A Claude Code skill that turns Claude into an agent-design expert.**

Ask Claude to design an AI agent and, by default, it improvises from memory —
plausible, but generic, and blind to the failure modes that bite in production.
This skill gives Claude a structured, battle-tested body of knowledge — the **21
agentic design patterns** from Antonio Gulli's *Agentic Design Patterns* — so that
instead of guessing, it reasons from a real catalog: which patterns your problem
needs, how they trade off, and how they compose into a reliable system.

It changes *how Claude thinks* about agent design, not just what it knows.

---

## Why this is useful

A powerful LLM is **not** an agent. Making one reliable takes architecture — how it
breaks down a task, calls tools, remembers, recovers from errors, and knows when to
escalate to a human. That architecture is a solved problem: there are ~21 recurring
patterns (the Gang-of-Four equivalents for the agent era). This skill puts all of
them at Claude's fingertips, as **concepts you can apply in any framework**
(LangChain, CrewAI, the raw Anthropic/OpenAI/Gemini SDK, or Google ADK). Code is
deliberately excluded — the patterns are durable; framework choices aren't.

---

## What changes — with vs. without the skill

> **You:** *"Design a text-to-SQL agent that runs queries against our production database."*

**Without the skill — Claude improvises:**
> "I'd use an LLM to generate SQL from the question, run it, and return the
> results. You could add error handling and maybe let it retry."

Reasonable, but vague. It misses the schema-grounding problem, has no quality loop,
and — dangerously — no safety gate before a generated query hits production.

**With the skill — Claude reasons from the catalog:**
> "This needs five patterns working together:
> - **RAG** to ground generation in your real schema (don't trust the model's guess at table names)
> - **Tool Use** as the executor — but *your code* runs the SQL, never the model; and the tool should **raise** on DB errors, not return them as strings, so failures aren't silently swallowed
> - **Reflection** with a *separate critic* (a 'meticulous SQL reviewer' persona) — self-review is biased; review the SQL against the schema *before* executing, capped at 3 iterations for cost
> - **Human-in-the-Loop** as a write-gate — read-only `SELECT`s run autonomously; anything mutating escalates for approval (escalation is just another tool)
> - **Exception Handling** to retry transient failures and feed permanent ones back into the reflection loop
>
> Here's the runtime flow…"

Same question. The second answer is **specific, ordered, and safe** — it names the
non-obvious pitfalls (raise-don't-return, biased self-review, the model-proposes /
code-executes boundary) that come straight from the patterns, not from improvisation.

---

## What becomes possible

Loaded, the skill lets you:

- **Pick the right patterns fast** — describe a problem, get the minimal set of patterns that solves it (most agents need 3–6), with the trade-offs spelled out.
- **Go deep on any one** — get a pattern's full mechanics, real-world use cases, and the production pitfalls, without code noise.
- **Design compositions** — see how patterns stack into one system (a research assistant = Planning + Tool Use + Multi-Agent + Reflection + Memory).
- **Pressure-test a design** — ask "what am I missing?" and Claude checks your architecture against the full catalog (no guardrails? no eval? no recovery?).
- **Stay framework-agnostic** — decide *what* to build here; implement the *how* in whatever stack you use.

It's a **design-phase** tool: it makes the architecture decisions sharp *before* you
write code.

---

## How to use it

Just talk to Claude about agent design. The skill activates on questions like:

- *"Which patterns should this agent use?"*
- *"Design an agent that does X."*
- *"What's the difference between Routing and Planning?"*
- *"Review this agent design for what's missing."*
- …or naming any pattern (RAG, Reflection, MCP, A2A, guardrails…).

Claude loads a one-screen index of all 21 patterns, then pulls the full detail for
whichever ones your problem needs — so the right knowledge is in context exactly
when it matters.

---

## The 21 patterns at a glance

| | Group | Patterns |
|---|---|---|
| 🧩 | **Foundations** | Prompt Chaining · Routing · Parallelization · Reflection · Tool Use · Planning · Multi-Agent |
| 🧠 | **State & Knowledge** | Memory Management · Learning & Adaptation · Model Context Protocol (MCP) · Goal Setting & Monitoring |
| 🛡️ | **Robustness** | Exception Handling & Recovery · Human-in-the-Loop · Knowledge Retrieval (RAG) |
| 🚀 | **Advanced & Scaling** | Inter-Agent Comms (A2A) · Resource-Aware Optimization · Reasoning Techniques · Guardrails / Safety · Evaluation & Monitoring · Prioritization · Exploration & Discovery |

<sub>Plus appendices (prompting techniques · frameworks overview · GUI/CLI/coding agents · AgentSpace), a worked composition example, and a glossary.</sub>

---

## Install

**As a plugin (recommended)** — one-command install from within Claude Code:

```
/plugin marketplace add eshwarvijay/agent-architecture
/plugin install agent-architecture
```

**Or manually** — clone and symlink the skill:

```sh
git clone https://github.com/eshwarvijay/agent-architecture ~/agent-architecture
ln -s ~/agent-architecture/skills/agent-architecture ~/.claude/skills/agent-architecture
```

Either way — next time you ask Claude an agent-design question, the skill kicks in.

**No Claude Code?** Every file is plain markdown. Point any assistant at
`skills/agent-architecture/`: *"Read SKILL.md and the relevant patterns/ files,
then design X."* — or just browse the patterns here on GitHub.

---

*Distilled from Antonio Gulli, “Agentic Design Patterns” (2025) — concepts only, a
derived reference; see the book for full text and code. Snapshot: mid-2025, so the
patterns hold but specific model/API details may have moved on.*

<details>
<summary>🍳 <i>psst… you found the kitchen</i></summary>

<p align="center">
  <img src="assets/clawd-cooking.jpeg" alt="Clawd the chef cooking up an agent" width="200">
  <br>
  <sub><b>Patterns are the recipe.</b> Use the fewest that work — 3–6, not all 21. Over-season and your clean paneer butter masala turns into a 30-spice mess no one can debug.</sub>
</p>

</details>
