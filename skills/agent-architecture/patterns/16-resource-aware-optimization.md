# Resource-Aware Optimization

> Resource-Aware Optimization enables intelligent agents to dynamically monitor and manage computational, temporal, and financial resources during operation — making decisions about how to execute actions so that goals are met within resource budgets or with maximum efficiency.

## Overview

Resource-Aware Optimization lets agents track and manage three categories of resource — computational (compute), temporal (time/latency), and financial (cost) — while they run. It differs from simple planning, which is primarily concerned with sequencing actions. Resource-Aware Optimization instead requires the agent to make decisions about *how* to execute actions in order to achieve goals within specified resource budgets, or to optimize for efficiency.

In practice this means making explicit trade-offs:
- Choosing between a more accurate but expensive model and a faster, lower-cost one.
- Deciding whether to allocate additional compute for a more refined response versus returning a quicker, less detailed answer.

A concrete illustration: an agent tasked with analyzing a large dataset for a financial analyst. If the analyst needs a preliminary report immediately, the agent might use a faster, more affordable model to quickly summarize key trends. If instead the analyst requires a highly accurate forecast for a critical investment decision — and has a larger budget and more time — the agent would allocate more resources and use a powerful, slower, but more precise predictive model. The same task is served differently depending on the prevailing budget, time, and accuracy requirements.

A key strategy within this pattern is the **fallback mechanism**, which acts as a safeguard when a preferred model is unavailable because it is overloaded or throttled. To ensure *graceful degradation*, the system automatically switches to a default or more affordable model, maintaining service continuity instead of failing completely.

The fundamental tension the pattern addresses is the trade-off between the *quality* of a system's output and the *resources* required to produce it. LLM-based applications can be expensive and slow, and selecting the most capable model or tool for every task is often inefficient. Without a dynamic management strategy, systems cannot adapt to varying task complexities or operate within budgetary and performance constraints.

## How It Works

The standardized solution is an agentic system that intelligently monitors and allocates resources based on the task at hand. The canonical architecture is a small ensemble of cooperating agents:

**Router Agent (classification and dispatch).** A Router Agent first classifies the complexity of an incoming request, then forwards it to the most suitable model or tool — a fast, inexpensive model for simple queries and a more powerful one for complex reasoning. Routing can be done at varying levels of sophistication:
- *Simple metric-based routing* — e.g., directing queries by query length, sending shorter queries to less expensive models and longer queries to more capable ones.
- *LLM- or ML-based routing* — a more sophisticated Router Agent uses an LLM or an ML model to analyze query nuance and complexity, determining which downstream language model is most suitable. For example, a factual-recall query is routed to a fast/cheap model, while a complex query requiring deep analysis is routed to a powerful/expensive model.

The LLM router's effectiveness can be improved with optimization techniques. *Prompt tuning* crafts prompts that guide the router LLM toward better routing decisions. *Fine-tuning* the router LLM on a dataset of queries paired with their optimal model choices improves routing accuracy and efficiency. This dynamic routing balances response quality against cost-effectiveness.

**Answering Agents (tiered models).** Behind the router sit agents that are identical in setup but differ in the model they use and therefore in cost. The chapter's running example pairs a powerful, more expensive model (Gemini Pro) for complex problem-solving with a fast, efficient, less expensive model (Gemini Flash) for straightforward questions. The two agents are otherwise configured the same way (name, description, instruction) — only the model assignment and its cost/latency profile differ.

**Critique Agent (feedback and refinement).** A Critique Agent evaluates the responses produced by the answering models and provides feedback serving several functions:
- *Self-correction* — it identifies errors or inconsistencies and prompts the answering agent to refine its output for improved quality.
- *Performance monitoring* — it systematically assesses responses, tracking metrics such as accuracy and relevance, which feed optimization.
- *Signal for reinforcement learning or fine-tuning* — consistent identification of inadequate responses from the cheaper (Flash) model can be used to refine the router agent's logic.

While the Critique Agent does not directly manage the budget, it contributes to *indirect budget management* by spotting suboptimal routing choices — such as sending simple queries to an expensive model, or complex queries to a cheap model that then yields poor results — and informing adjustments that improve resource allocation and produce cost savings. The Critique Agent can be configured to review either only the generated text, or both the original query and the generated text, enabling a more comprehensive evaluation of how well the response aligns with the initial question. It operates from a predefined system prompt that establishes its role as an evaluator, specifies areas for critical focus, emphasizes constructive feedback (fortifying rather than invalidating the work), encourages identification of both strengths and weaknesses, and directs how feedback should be structured and presented.

### Conceptual walk-through: the hierarchical travel-planner example (Google ADK)

A travel planner illustrates how routing maps to a hierarchy of tasks. High-level planning — understanding a user's complex request, breaking it into a multi-step itinerary, and making logical decisions — is handled by a sophisticated, more powerful model (Gemini Pro). This is the "planner" agent, which needs deep contextual understanding and reasoning ability. Once the plan is established, the individual tasks within it — looking up flight prices, checking hotel availability, finding restaurant reviews — are essentially simple, repetitive web queries. These "tool function calls" can be executed by a faster, more affordable model (Gemini Flash). The intuition is clear: the cheap model suffices for straightforward web searches, while the intricate planning phase requires the greater intelligence of the advanced model to ensure a coherent, logical travel plan.

Google's ADK supports this via its multi-agent architecture, which enables modular, scalable applications where different agents handle specialized tasks. Model flexibility allows the direct use of various Gemini models (both Pro and Flash) or integration of other models through LiteLLM. ADK's orchestration capabilities support dynamic, LLM-driven routing for adaptive behavior, and its built-in evaluation features allow systematic assessment of agent performance for system refinement. Conceptually, the chapter defines two answering agents (one on Gemini Pro, one on Gemini Flash) with identical setup but different models and costs, then a Router Agent that — in its simplest form — routes by query length (short queries to Flash, longer queries to Pro).

### Conceptual walk-through: the three-category classifier (OpenAI)

A second example builds a resource-aware system that handles user queries efficiently by first classifying each query into one of three categories to choose the most appropriate and cost-effective processing pathway. This avoids wasting computational resources on simple requests while ensuring complex queries receive the attention they need. The three categories are:
- **simple** — straightforward questions answerable directly without complex reasoning or external data.
- **reasoning** — queries requiring logical deduction or multi-step thought, routed to more powerful models.
- **internet_search** — questions needing current information, which automatically trigger a web search to provide an up-to-date answer.

Conceptually the system works in stages. First, a classification step uses an OpenAI model (the example uses GPT-4o) acting as a classifier, instructed to return exactly one of the three category labels: use *simple* for direct factual questions needing no reasoning or current events; *reasoning* for logic, math, or multi-step inference; *internet_search* if the prompt concerns current events, recent data, or information outside the model's training data. Second, if the query is classified as needing current information, a web search is performed via the Google Custom Search API. Third, a response-generation step selects the model based on the classification — a small, cheap model (GPT-4o-mini) for *simple* queries, a reasoning-oriented model (o4-mini) for *reasoning* queries, and a capable model (GPT-4o) for *internet_search* queries, with the retrieved search results supplied as context to the model. A main orchestration function ties these together: it classifies the prompt, performs a search only when needed, generates the response, and returns the classification, the model actually used, and the generated answer. The net effect is that different query types are directed to differently priced and differently capable models, matching spend and capability to need.

### Conceptual walk-through: OpenRouter (unified routing and fallback)

OpenRouter provides a unified interface to hundreds of AI models through a single API endpoint, with automated failover and cost-optimization, integrable through common SDKs or frameworks. The chapter notes a request is made by sending a chat-completion call to the OpenRouter endpoint with authorization headers (an API key) and optional site-identification headers, naming a specific model (e.g., OpenAI's GPT-4o) to receive the response. OpenRouter offers two distinct methodologies for deciding which computational model processes a request:

- **Automated Model Selection.** The request is routed to an optimized model chosen from a curated set, with the choice based on the specific content of the user's prompt (invoked by specifying a special `openrouter/auto` model identifier). The identifier of the model that ultimately handled the request is returned in the response metadata.
- **Sequential Model Fallback.** The user specifies a hierarchical list of models. The system first attempts the primary model in the sequence; if it fails for any reason — service unavailability, rate-limiting, or content filtering — the system automatically re-routes to the next model in the list, continuing until one succeeds or the list is exhausted. The final cost and the returned model identifier correspond to the model that actually completed the computation. (The chapter shows this as a `models` list naming, for example, an Anthropic Claude model first and a fallback model second.)

OpenRouter also publishes a leaderboard that ranks available models by cumulative token production and surfaces the latest models from different providers (ChatGPT, Gemini, Claude).

### Beyond dynamic model switching: a spectrum of optimizations

Resource-aware optimization extends well beyond swapping models. The chapter enumerates a broader spectrum of techniques:

- **Dynamic Model Switching.** Strategically selecting among LLMs based on task intricacy and available compute — a lightweight, cost-effective LLM for simple queries; sophisticated, resource-intensive models for complex, multifaceted problems.
- **Adaptive Tool Use & Selection.** Intelligently choosing the most appropriate and efficient tool for each sub-task from a suite of options, weighing factors like API usage cost, latency, and execution time — optimizing the use of external APIs and services.
- **Contextual Pruning & Summarization.** Managing how much information the agent processes by strategically minimizing prompt token count: summarizing and selectively retaining only the most relevant information from interaction history, reducing inference cost and avoiding unnecessary computational overhead.
- **Proactive Resource Prediction.** Anticipating resource demands by forecasting future workloads and system requirements, enabling proactive allocation and management to keep the system responsive and prevent bottlenecks.
- **Cost-Sensitive Exploration (multi-agent).** Extending optimization to include communication costs alongside computational costs, shaping how agents collaborate and share information to minimize overall resource expenditure.
- **Energy-Efficient Deployment.** Tailored for environments with stringent resource constraints, minimizing the energy footprint of agent systems to extend operational time and reduce running costs.
- **Parallelization & Distributed Computing Awareness.** Distributing computational workloads across multiple machines or processors to increase processing power and throughput, achieving greater efficiency and faster task completion.
- **Learned Resource Allocation Policies.** Introducing a learning mechanism so agents adapt and optimize their allocation strategies over time, based on feedback and performance metrics, improving efficiency through continuous refinement.
- **Graceful Degradation and Fallback Mechanisms.** Ensuring the system keeps functioning — perhaps at reduced capacity — even under severe resource constraints, degrading gracefully and falling back to alternative strategies to maintain operation and essential functionality.
- **Prioritization of Critical Tasks.** Ensuring the most important tasks receive resources first when resources are limited.

## Practical Applications & Use Cases

- **Cost-Optimized LLM Usage.** An agent decides whether to use a large, expensive LLM for complex tasks or a smaller, more affordable one for simpler queries, based on a budget constraint.
- **Latency-Sensitive Operations.** In real-time systems, an agent chooses a faster but potentially less comprehensive reasoning path to guarantee a timely response.
- **Energy Efficiency.** For agents deployed on edge devices or with limited power, processing is optimized to conserve battery life.
- **Fallback for Service Reliability.** An agent automatically switches to a backup model when the primary choice is unavailable, ensuring service continuity and graceful degradation.
- **Data Usage Management.** An agent opts for summarized data retrieval instead of full dataset downloads to save bandwidth or storage.
- **Adaptive Task Allocation.** In multi-agent systems, agents self-assign tasks based on their current computational load or available time.

## Trade-offs & When to Use

The central trade-off is between output quality and the resources consumed to produce it. A more powerful model raises quality but costs more and is slower; a cheaper model is faster and less expensive but may be less accurate. Resource-Aware Optimization is the mechanism that programmatically balances this trade-off per request rather than committing to one fixed point.

Rule of thumb — use this pattern when:
- Operating under strict financial budgets for API calls or computational power.
- Building latency-sensitive applications where quick response times are critical.
- Deploying agents on resource-constrained hardware such as edge devices with limited battery life.
- Programmatically balancing the trade-off between response quality and operational cost.
- Managing complex, multi-step workflows where different tasks have varying resource requirements (e.g., the travel planner where high-level planning needs a powerful model and routine lookups do not).

There is added complexity cost to the pattern itself: introducing a router, tiered models, and a critique loop adds moving parts and the routing decision itself consumes some latency and (for LLM-based routers) tokens. The pattern pays off when the savings or quality gains from correct routing outweigh that overhead — which is typically the case at scale or under firm budget/latency constraints.

## Pitfalls

- **Misrouting.** A poorly tuned router sends simple queries to an expensive model (wasting money) or complex queries to a cheap model (yielding poor results). The Critique Agent exists partly to detect this and feed corrections back into the routing logic.
- **Router overhead.** An LLM-based router adds its own latency and token cost to every request; for trivially simple workloads the routing step can cost more than it saves.
- **Naive routing heuristics.** Routing on a crude proxy like query length is easy but unreliable — a short query can still be hard, and a long query can be trivial. Length-based routing is a starting point, not a robust solution; nuance-aware (LLM/ML) routing is more accurate but more expensive.
- **Fallback masking failures.** Automatic fallback to a cheaper/default model preserves continuity but can silently degrade quality; without monitoring (e.g., the Critique Agent), persistent degradation may go unnoticed.

## Relationships to Other Patterns

- **Routing (Chapter 2).** Resource-Aware Optimization is a specialization of routing where the routing criterion is resource cost/complexity rather than topical intent — the Router Agent here decides *which tier of model* handles a request. The same routing mechanisms (simple metric, LLM-based, ML-based) apply.
- **Multi-Agent Systems (Chapter 7).** The canonical implementation is a multi-agent architecture (router, tiered answering agents, critique agent); Google ADK's multi-agent framework provides the modular, scalable structure. Cost-Sensitive Exploration extends optimization to inter-agent communication costs.
- **Reflection / Critique (Chapter 4).** The Critique Agent is a reflection mechanism applied to resource decisions — evaluating outputs, prompting self-correction, and refining the router's logic over time.
- **Planning (Chapter 6).** The pattern is explicitly contrasted with simple planning: planning sequences actions, whereas Resource-Aware Optimization decides how to execute them within resource budgets. The hierarchical travel planner shows planning and resource-aware routing working together.
- **Evaluation and Monitoring.** The Critique Agent's performance-monitoring role connects to systematic evaluation; ADK's built-in evaluation features support measuring agent performance for refinement.
- **Memory Management / Contextual Pruning.** Contextual Pruning & Summarization overlaps with context/memory management — trimming history to control token count and inference cost.
- **Learning and Adaptation (Chapter 9).** Learned Resource Allocation Policies and fine-tuning the router on past optimal choices apply learning to make the optimization self-improving.

## Key Takeaways

- Resource-Aware Optimization is essential: intelligent agents can manage computational, temporal, and financial resources dynamically, making decisions about model usage and execution paths based on real-time constraints and objectives.
- The core trade-off is output quality versus the resources required to produce it; the pattern balances response quality with cost-effectiveness on a per-request basis.
- A Router Agent classifies request complexity and dispatches to the most suitable model or tool — a fast, cheap model for simple queries (e.g., Gemini Flash, GPT-4o-mini), a powerful, expensive model for complex reasoning (e.g., Gemini Pro, GPT-4o).
- A Critique Agent enables self-correction, performance monitoring, and refinement of routing logic, indirectly improving budget management by catching misrouted queries.
- Multi-agent frameworks such as Google ADK provide the modular, scalable structure (specialized answering, routing, and critique agents), with model flexibility (Gemini Pro/Flash directly, or other models via LiteLLM) and LLM-driven orchestration.
- Routers can be improved through prompt tuning and fine-tuning on datasets of queries paired with optimal model choices.
- Unified gateways like OpenRouter offer automated model selection and sequential model fallback across many providers through a single endpoint, with the actual model and cost reported back in the response.
- The pattern spans many techniques beyond model switching: adaptive tool selection, contextual pruning and summarization, proactive resource prediction, cost-sensitive exploration, energy-efficient deployment, parallelization, learned allocation policies, graceful degradation, and prioritization of critical tasks.
- Integrating these optimization principles into agent design is fundamental for building scalable, robust, and sustainable AI systems.

## References

1. Google's Agent Development Kit (ADK): https://google.github.io/adk-docs/
2. Gemini Flash 2.5 & Gemini 2.5 Pro: https://aistudio.google.com/
3. OpenRouter: https://openrouter.ai/docs/quickstart
