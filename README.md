# agent-architecture

**A design-phase reference for building AI agents.** The 21 agentic design
patterns from Antonio Gulli's *Agentic Design Patterns: A Hands-On Guide to
Building Intelligent Systems*, distilled to **concepts only — no code.**

A capable LLM is not an agent. Turning one into a reliable, goal-directed system
takes structure: how it breaks down a task, calls tools, remembers, recovers from
errors, and knows when to ask a human. These patterns are that structure — the
Gang-of-Four design patterns for the agent era. This repo tells you **which
patterns a problem needs and why**; you implement the **how** in your own stack
(LangChain / LangGraph, CrewAI, the Anthropic / OpenAI / Gemini SDK, or Google ADK).

> Packaged as a **Claude Code skill** — install it (below) and Claude loads the
> right pattern on demand while you design. But every file is plain markdown, so
> it's just as useful read straight on GitHub or pasted into any chat.

---

## How to use it

**The workflow is design → implement:**

1. **Pick patterns** — match your problem against the catalog below (or the *Decision guide*). Most real agents need 3–6.
2. **Go deep** — read the matching `patterns/<name>.md` for mechanics, trade-offs, and the pitfalls that bite in production.
3. **Compose** — see *How patterns combine* for how they layer into one system.
4. **Implement** — build it in your framework. This repo deliberately stops at the design boundary.

**As a Claude Code skill**, that loop is automatic — ask *"which pattern for X?"*,
*"design an agent that…"*, or name a pattern, and Claude reads the relevant files
for you.

---

## The 21 patterns

### Part 1 — Foundations: the core execution loop
| Pattern | What it is | Reach for it when |
|---|---|---|
| **Prompt Chaining** | Split a task into a sequence of LLM steps, each feeding the next | One prompt overloads the model — instructions get dropped, context drifts |
| **Routing** | Classify the input, dispatch to the right handler/tool/sub-agent | Several distinct paths exist and the right one depends on the request |
| **Parallelization** | Run independent sub-tasks concurrently, then synthesize | Sub-tasks don't depend on each other and latency matters |
| **Reflection** | Agent critiques and revises its own output (often via a separate critic) | First drafts are unreliable and quality beats speed |
| **Tool Use** | LLM calls external functions / APIs / DBs (function calling) | The agent needs live data, calculations, or real-world actions |
| **Planning** | Agent forms a multi-step plan before acting | The *how* must be discovered at runtime, not hard-coded |
| **Multi-Agent** | Specialized agents coordinate (supervisor / hierarchical / network) | A monolithic agent is too complex; roles benefit from separation |

### Part 2 — State, knowledge & goals
| Pattern | What it is | Reach for it when |
|---|---|---|
| **Memory Management** | Short-term context + long-term persistent memory | The agent must remember within or across sessions |
| **Learning & Adaptation** | Behavior improves over time (in-context, fine-tuning, RL, self-mod) | The agent should adapt from feedback, not stay static |
| **Model Context Protocol (MCP)** | Open protocol standardizing tool/resource/prompt access | Tools & data must be discoverable and reusable across agents |
| **Goal Setting & Monitoring** | Define goals + success criteria, then track progress | The agent needs explicit objectives and a way to know it's on track |

### Part 3 — Robustness & interaction
| Pattern | What it is | Reach for it when |
|---|---|---|
| **Exception Handling & Recovery** | Detect, handle, recover (retry / fallback / circuit-breaker) | Tools and environments fail and the agent must degrade gracefully |
| **Human-in-the-Loop** | Insert human approval / escalation / correction at key points | Stakes are high, confidence is low, or oversight is required |
| **Knowledge Retrieval (RAG)** | Retrieve external knowledge to ground generation | The agent needs facts beyond training data, or must cite sources |

### Part 4 — Advanced & scaling
| Pattern | What it is | Reach for it when |
|---|---|---|
| **Inter-Agent Communication (A2A)** | Open protocol for agents to discover & task each other | Independent agents (even across orgs) must interoperate |
| **Resource-Aware Optimization** | Route by cost/latency; budget tokens; model fallback | Cost or latency budgets matter; cheap vs. expensive models per task |
| **Reasoning Techniques** | CoT, Tree-of-Thought, Self-Correction, ReAct, debate, inference-time scaling | The task needs deliberate multi-step reasoning, not one shot |
| **Guardrails / Safety** | Layered input/output/behavioral/tool constraints + moderation | Untrusted input, harmful-output risk, prompt injection, policy needs |
| **Evaluation & Monitoring** | Assess responses & trajectories (LLM-as-judge, tool metrics) | You need to measure quality and watch agents in production |
| **Prioritization** | Rank tasks/goals/actions by urgency, importance, cost, dependencies | The agent juggles competing tasks and must choose what's next |
| **Exploration & Discovery** | Explore unknown spaces, generate & test hypotheses | The goal is open-ended discovery, not optimizing a known objective |

---

## Decision guide

- **Task too big for one prompt?** → Prompt Chaining (sequential) · Parallelization (independent) · Planning (unknown steps)
- **Need to pick among handlers?** → Routing
- **Output quality unreliable?** → Reflection (+ Goal Setting for criteria, Evaluation to measure)
- **Needs external data/actions?** → Tool Use → standardize with MCP → ground with RAG
- **One agent too complex?** → Multi-Agent; if agents span orgs → A2A
- **Must remember things?** → Memory Management
- **High stakes / untrusted input?** → Guardrails + Human-in-the-Loop + Exception Handling
- **Cost or latency pressure?** → Resource-Aware Optimization (+ Prioritization)
- **Hard reasoning?** → Reasoning Techniques (CoT / ToT / ReAct …)
- **Open-ended discovery?** → Exploration & Discovery

---

## How patterns combine

Real agents stack several. Take an **autonomous research assistant** answering
*"Analyze the impact of quantum computing on cybersecurity"* — five patterns woven
into one system:

1. **Planning** decomposes the query into a research plan (concepts → algorithms → threats → synthesis).
2. **Tool Use** executes each step — search tools, academic-DB queries.
3. **Multi-Agent** splits the work: a *Researcher* gathers sources, a *Writer* drafts from the plan.
4. **Reflection** adds a *Critic* that reviews the draft; feedback loops back to the Writer to self-correct.
5. **Memory Management** holds the plan, sources, drafts, and critiques so context survives the whole run.

No single pattern does this; the composition does. `conclusion.md` has the full
walkthrough.

---

## What's inside

```
SKILL.md          # the index Claude loads — every pattern's purpose + when-to-use
patterns/         # 21 deep files: overview, mechanics, use cases, trade-offs, pitfalls, refs
appendices/       # prompting techniques · frameworks overview · GUI/CLI/coding agents · AgentSpace
conclusion.md     # how patterns combine (full worked example)
glossary.md       # core agentic-AI terms
```

Each `patterns/*.md` carries the chapter's full conceptual depth — including the
non-obvious pitfalls (e.g. *tools should raise errors, not return them as strings*;
*a separate critic beats self-review*; *the model proposes the call, your code
executes it*). Code is excluded on purpose: the patterns are durable, framework
choices aren't.

---

## Install (Claude Code)

```sh
git clone https://github.com/eshwarvijay/agent-architecture ~/agent-architecture
ln -s ~/agent-architecture ~/.claude/skills/agent-architecture
```

Then ask anything agent-design-shaped and the skill loads the right pattern on demand.

**No install?** Point any assistant at the files: *"Read `SKILL.md` and
`patterns/04-reflection.md`, then propose a design for X."*

---

*Distilled from Antonio Gulli, “Agentic Design Patterns” (2025). Concepts only — a
derived reference; see the book for full text and code. Snapshot: mid-2025, so the
patterns hold but specific model/API details may have moved on.*
