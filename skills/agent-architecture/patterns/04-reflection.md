# Reflection Pattern

> An agent evaluates its own work, output, or internal state and uses that evaluation to iteratively self-correct and refine its response toward higher quality, accuracy, and completeness.

## Overview

Earlier patterns — Chaining (sequential execution), Routing (dynamic path selection), and Parallelization (concurrent execution) — let agents perform complex tasks more efficiently and flexibly. But even with sophisticated workflows, an agent's *initial* output or plan might not be optimal, accurate, or complete. Reflection addresses this gap.

The Reflection pattern is a form of self-correction or self-improvement. The agent doesn't just produce an output; it then examines that output (or the process that generated it), identifies potential issues or areas for improvement, and uses those insights to generate a better version or to modify its future actions. Refinement can be driven by feedback, internal critique, or comparison against desired criteria. Reflection can occasionally be facilitated by a *separate* agent whose specific role is to analyze the output of an initial agent.

What distinguishes Reflection from earlier patterns is the **feedback loop**. Unlike a simple sequential chain — where output is passed directly to the next step — or routing — which merely chooses a path — Reflection feeds the agent's output back into the process for evaluation and improvement.

Reflection adds a layer of **meta-cognition** to agentic systems: agents learn from their own outputs and processes, moving beyond merely executing instructions toward a more sophisticated form of problem-solving and content generation, exhibiting a degree of self-awareness and adaptability.

**Synergy with goal setting and monitoring.** A goal provides the ultimate benchmark for the agent's self-evaluation, while monitoring tracks its progress. In many practical cases, Reflection acts as the *corrective engine*, using monitored feedback to analyze deviations from the goal and adjust strategy. This synergy transforms the agent from a passive executor into a purposeful system that adaptively works to achieve its objectives.

**Synergy with memory.** Reflection's effectiveness is significantly enhanced when the LLM keeps a memory of the conversation. Conversational history gives the evaluation phase crucial context, letting the agent assess its output not in isolation but against previous interactions, user feedback, and evolving goals. Without memory, each reflection is a self-contained event; with memory, reflection becomes a *cumulative* process where each cycle builds on the last — the agent learns from past critiques and avoids repeating errors, yielding more intelligent, context-aware refinement.

## How It Works

A reflection cycle typically involves four steps:

1. **Execution.** The agent performs a task or generates an initial output.
2. **Evaluation / Critique.** The agent (often via another LLM call or a set of rules) analyzes the result from the previous step. This evaluation might check for factual accuracy, coherence, style, completeness, adherence to instructions, or other relevant criteria.
3. **Reflection / Refinement.** Based on the critique, the agent determines how to improve. This might involve generating a refined output, adjusting parameters for a subsequent step, or even modifying the overall plan.
4. **Iteration (optional but common).** The refined output or adjusted approach is executed again, and the reflection process repeats until a satisfactory result is achieved or a stopping condition is met (e.g., a quality threshold or a maximum iteration count).

### Self-reflection vs. the Producer–Critic model

Reflection can be performed by the agent on itself (self-reflection), or — often more effectively — by a distinct critic. Choosing between these is a key architectural decision within the pattern.

A key and highly effective implementation separates the process into two distinct logical roles: a **Producer** and a **Critic** (also called the "Generator–Critic" or "Producer–Reviewer" model). While a single agent can perform self-reflection, using two specialized agents — or two separate LLM calls with distinct system prompts — often yields more robust and unbiased results.

- **The Producer agent.** Its primary responsibility is to perform the initial execution of the task. It focuses entirely on generating the content — writing code, drafting a blog post, creating a plan. It takes the initial prompt and produces the first version of the output.
- **The Critic agent.** Its sole purpose is to evaluate the Producer's output. It is given a *different* set of instructions, often a distinct persona (e.g., "You are a senior software engineer," "You are a meticulous fact-checker"). The Critic's instructions guide it to analyze the work against specific criteria — factual accuracy, code quality, stylistic requirements, completeness — and it is designed to find flaws, suggest improvements, and provide structured feedback.

This separation of concerns is powerful because it prevents the **"cognitive bias"** of an agent reviewing its own work. The Critic approaches the output with a fresh perspective, dedicated entirely to finding errors and areas for improvement. The Critic's feedback is then passed back to the Producer, which uses it as a guide to generate a new, refined version. The separation also enhances objectivity and allows for more specialized, structured feedback.

### Implementation considerations

Implementing reflection requires structuring the workflow to include these feedback loops. This can be done through iterative loops in custom procedural code, or using frameworks that support state management and conditional transitions based on evaluation results.

A *single* step of evaluation and refinement can be implemented within an ordinary LangChain/LangGraph, ADK, or Crew.AI chain. But *true iterative* reflection — looping until satisfactory — typically involves more complex orchestration, because it requires mechanisms for state management and cyclical execution. These are handled natively in graph-based frameworks such as LangGraph (or through custom procedural code).

### Worked example — LangChain (described, not coded)

The chapter walks through a LangChain example using OpenAI's GPT-4o to iteratively generate and refine a Python function that calculates the factorial of a number. Conceptually it does the following:

- It sets up the environment, loads the API key, and initializes the LLM with a *low temperature* for focused, more deterministic output.
- The core task is defined by a prompt asking for a `calculate_factorial` function with specific requirements: accept an integer, compute the factorial, include a clear docstring, handle the edge case that 0! = 1, and raise an error on negative input.
- A loop (capped at a maximum number of iterations, e.g., 3) drives the reflection. On the **first iteration** the model generates initial code from the task prompt. On **subsequent iterations** it refines the code based on the prior critique.
- A separate **"reflector" role** — the same model but with a *different system prompt* casting it as a senior software engineer / meticulous code reviewer — critiques the generated code against the original requirements, looking for bugs, style issues, missing edge cases, and improvements.
- The critique is returned either as a bulleted list of issues, or — if no issues are found — the single sentinel phrase `CODE_IS_PERFECT`, which serves as the **stopping condition**.
- A growing **conversation history** (task prompt, each generated code version, and each critique) is maintained and passed to the model at every step, giving context to both the generation/refinement and the reflection stages.
- The loop ends when the critique signals the code is perfect or the iteration cap is reached, and the final refined code is printed.

This demonstrates a single reflector role implemented as a distinct prompted persona within one running loop.

### Worked example — Google ADK (described, not coded)

The chapter shows a conceptual ADK example using a Generator–Critic structure built from a sequential pipeline of two LLM-backed agents:

- A **Generator** agent ("DraftWriter") produces an initial short, informative draft paragraph on the user's subject and saves it to a shared state key (e.g., `draft_text`).
- A **Critic/Reviewer** agent ("FactChecker") reads the draft from that state key, verifies the factual accuracy of all claims, and outputs a *structured* result — a dictionary with a `status` field ("ACCURATE" or "INACCURATE") and a `reasoning` field explaining the status and citing specific issues. This is saved to another state key (e.g., `review_output`).
- A **SequentialAgent** ties the two together and guarantees execution order: the Generator runs first and writes to state; the Reviewer then reads that state, performs its check, and writes its findings back to state.

This shows reflection realized as a sequential multi-agent pipeline with shared state passing output between specialized agents. The chapter notes that an **alternative ADK implementation using a `LoopAgent`** is also available for those wanting true iterative looping rather than a single pass.

## Practical Applications & Use Cases

Reflection is valuable wherever output quality, accuracy, or adherence to complex constraints is critical:

1. **Creative writing and content generation.** Refining generated text, stories, poems, or marketing copy. *Example:* an agent writing a blog post generates a draft, critiques it for flow, tone, and clarity, then rewrites — repeating until quality standards are met. *Benefit:* more polished, effective content.
2. **Code generation and debugging.** Writing code, identifying errors, and fixing them. *Example:* an agent writes an initial function, runs tests or static analysis, identifies errors or inefficiencies, then modifies the code based on the findings. *Benefit:* more robust and functional code.
3. **Complex problem solving.** Evaluating intermediate steps or proposed solutions in multi-step reasoning. *Example:* an agent solving a logic puzzle proposes a step, evaluates whether it moves closer to the solution or introduces contradictions, and backtracks or chooses a different step if needed. *Benefit:* better navigation of complex problem spaces.
4. **Summarization and information synthesis.** Refining summaries for accuracy, completeness, and conciseness. *Example:* an agent generates an initial summary, compares it against the key points of the original document, then refines to add missing information or improve accuracy. *Benefit:* more accurate and comprehensive summaries.
5. **Planning and strategy.** Evaluating a proposed plan to find flaws or improvements. *Example:* an agent generates a plan, simulates its execution or evaluates its feasibility against constraints, then revises the plan. *Benefit:* more effective and realistic plans.
6. **Conversational agents.** Reviewing previous turns to maintain context, correct misunderstandings, or improve response quality. *Example:* a customer support chatbot reviews the conversation history and its last message after a user reply, ensuring coherence and accurately addressing the latest input. *Benefit:* more natural and effective conversations.

## Trade-offs & When to Use

**What it solves.** An agent's initial output is often suboptimal — inaccurate, incomplete, or failing to meet complex requirements. Basic agentic workflows have no built-in process for the agent to recognize and fix its own errors, so the first response becomes the final one regardless of quality. Reflection introduces a self-correction mechanism: a producer generates output, a critic (or the producer itself) evaluates it against predefined criteria, and the critique drives an improved version. Iterating generation → evaluation → refinement progressively raises quality, producing more accurate, coherent, and reliable outcomes.

**Costs.** The benefits come with important trade-offs:

- **Higher cost and latency.** Each refinement loop may require a new LLM call, making the pattern suboptimal for time-sensitive applications.
- **Memory-intensive.** With each iteration the conversational history expands — initial output, critique, and subsequent refinements all accumulate — raising the risk of exceeding the model's context window or being throttled by API services.

**Rule of thumb.** Use Reflection when the **quality, accuracy, and detail** of the final output matter more than **speed and cost**. It is particularly effective for generating polished long-form content, writing and debugging code, and creating detailed plans. Employ a **separate critic agent** specifically when tasks require high objectivity or specialized evaluation that a generalist producer agent might miss.

## Pitfalls

- **Self-review bias.** An agent critiquing its own work is prone to "cognitive bias" — it tends to overlook its own errors. A separate critic with a distinct persona mitigates this.
- **Context-window growth.** Because history accumulates each cycle, long reflection loops can overflow the context window or trigger API throttling.
- **Latency/cost blow-up in time-sensitive settings.** The per-iteration LLM calls make naive iterative reflection a poor fit where responsiveness or budget is paramount; cap iterations and define clear stopping conditions.

## Relationships to Other Patterns

- **Chaining / Routing / Parallelization.** Reflection differs by introducing a feedback loop rather than simply forwarding output or selecting a path; as a control structure it can be composed with these foundational patterns to build more robust, functionally complex agentic systems.
- **Goal Setting and Monitoring (Ch. 11).** The goal supplies the benchmark for self-evaluation and monitoring tracks progress; Reflection serves as the corrective engine that uses monitored feedback to analyze deviations and adjust strategy.
- **Memory (Ch. 8).** Conversational memory turns reflection from isolated, single-shot events into a cumulative process where each cycle learns from prior critiques.
- **Multi-Agent systems.** The Producer–Critic model is itself a small multi-agent arrangement, and ADK realizes it through multi-agent sequential (and loop) pipelines.

## Key Takeaways

- Reflection's primary advantage is the ability to **iteratively self-correct and refine** outputs, yielding significantly higher quality, accuracy, and adherence to complex instructions.
- It centers on a **feedback loop of execution → evaluation/critique → refinement**, and is essential for tasks requiring high-quality, accurate, or nuanced outputs.
- A powerful implementation is the **Producer–Critic model**, where a separate agent (or prompted role) evaluates the initial output. This separation of concerns enhances objectivity and enables more specialized, structured feedback.
- These benefits come at the cost of **increased latency and computational expense**, plus a higher risk of exceeding the context window or being throttled by API services.
- **Full iterative reflection** generally requires stateful workflows (e.g., LangGraph), but a **single reflection step** can be implemented in LangChain using LCEL to pass output for critique and subsequent refinement.
- **Google ADK** facilitates reflection through sequential workflows where one agent's output is critiqued by another, enabling subsequent refinement (and via a LoopAgent for full iteration).
- Overall, the pattern lets agents perform self-correction and enhance their performance over time, transforming them into purposeful, adaptive systems.

## References

1. *Training Language Models to Self-Correct via Reinforcement Learning* — https://arxiv.org/abs/2409.12917
2. LangChain Expression Language (LCEL) Documentation — https://python.langchain.com/docs/introduction/
3. LangGraph Documentation — https://www.langchain.com/langgraph
4. Google Agent Developer Kit (ADK) Documentation (Multi-Agent Systems) — https://google.github.io/adk-docs/agents/multi-agents/
