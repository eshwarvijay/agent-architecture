# Planning

> The Planning pattern is the ability of an agent (or system of agents) to autonomously formulate a sequence of actions that moves from an initial state toward a desired goal state, decomposing a complex objective into smaller, executable, interdependent steps.

## Overview

Intelligent behavior involves more than just reacting to immediate input. It requires foresight, the breaking down of complex tasks into smaller manageable steps, and strategizing how to achieve a desired outcome. The Planning pattern addresses this: at its core, planning is the ability of an agent or a system of agents to formulate a sequence of actions to move from an initial state toward a goal state.

A useful mental model is to think of a planning agent as a specialist to whom you delegate a complex goal. When you ask it to "organize a team offsite," you are defining the *what* — the objective and its constraints — but not the *how*. The agent's core task is to autonomously chart a course to that goal. It must first understand the initial state (e.g., budget, number of participants, desired dates) and the goal state (a successfully booked offsite), and then discover the optimal sequence of actions to connect them. Crucially, the plan is not known in advance; it is created in response to the request.

A hallmark of this process is **adaptability**. An initial plan is merely a starting point, not a rigid script. The agent's real power lies in its ability to incorporate new information and steer the project around obstacles. For example, if a preferred venue becomes unavailable or a chosen caterer is fully booked, a capable agent does not simply fail — it adapts. It registers the new constraint, re-evaluates its options, and formulates a new plan, perhaps by suggesting alternative venues or dates.

However, it is crucial to recognize the **trade-off between flexibility and predictability**. Dynamic planning is a specific tool, not a universal solution. When a problem's solution is already well-understood and repeatable, constraining the agent to a predetermined, fixed workflow is more effective. That approach deliberately limits the agent's autonomy in order to reduce uncertainty and the risk of unpredictable behavior, thereby guaranteeing a reliable and consistent outcome. The decision to use a planning agent versus a simple task-execution agent therefore hinges on a single question: **does the "how" need to be discovered, or is it already known?**

## How It Works

The Planning pattern is a core computational process in autonomous systems. It transforms a high-level objective into a structured plan composed of discrete, executable steps, enabling an agent to synthesize a sequence of actions to achieve a specified goal, particularly within dynamic or complex environments.

The general flow is:

1. **Understand the states.** The agent identifies the initial state (the starting conditions and constraints) and the goal state (what success looks like).
2. **Decompose the objective.** A high-level goal is broken into a sequence of smaller, actionable steps or sub-goals, arranged in a logical order that respects dependencies between them.
3. **Orchestrate execution.** The agent works through the plan, invoking the necessary tools or interacting with various systems to manage dependencies and carry out each step.
4. **Adapt as needed.** As new information arrives or obstacles appear, the agent re-evaluates and revises the plan rather than failing outright.

Large language models are particularly well-suited to the plan-generation step because they can produce plausible and effective plans based on their vast training data. In agent frameworks, this planning behavior is encouraged by **explicitly prompting or designing tasks to require a planning step** — for example, instructing the agent to first produce a plan and only then act on it. This structured approach is what transforms a simple reactive agent into a strategic executor that can proactively work toward a complex objective and adapt its plan when necessary.

### Illustrative implementation (CrewAI)

The chapter demonstrates a straightforward, sequential form of the pattern using the **CrewAI** framework. The example creates a single agent whose role is to both plan and write. The agent is given a role ("Article Planner and Writer"), a goal (plan and then write a concise, engaging summary on a specified topic), and a backstory emphasizing expertise as a technical writer and content strategist whose strength is creating a clear, actionable plan before writing. A language model (an OpenAI chat model) is explicitly assigned to the agent.

A single task is defined with a two-part instruction: first create a bullet-point plan for a summary on a given topic ("The importance of Reinforcement Learning in AI"), and then write the summary (around 200 words) based on that plan. The expected output is structured into two distinct labeled sections — a "Plan" section containing the bulleted outline and a "Summary" section containing the prose. The agent and task are assembled into a crew configured to run sequentially, and the crew is kicked off to execute the task and print the result.

The key conceptual point: the *task description itself* forces a plan-then-execute behavior. The agent is required to externalize a plan before producing the final artifact, which is the simplest manifestation of the Planning pattern — a single agent following a self-generated plan in order.

### Real-world example: Google Gemini DeepResearch

Google Gemini DeepResearch is an agent-based system designed for autonomous information retrieval and synthesis, and it exemplifies a more advanced, dynamic form of planning. It functions through a multi-step agentic pipeline that dynamically and iteratively queries Google Search to systematically explore complex topics. The system processes a large corpus of web-based sources, evaluates the collected data for relevance and knowledge gaps, performs subsequent searches to address those gaps, and consolidates the vetted information into a structured, multi-page summary with citations to the original sources.

Its operation is not a single query-response event but a managed, long-running process:

- **Plan generation and human review.** It begins by deconstructing the user's prompt into a multi-point research plan, which is then presented to the user for review and modification. This enables collaborative shaping of the research trajectory *before* execution begins.
- **Iterative search-and-analysis loop.** Once the plan is approved, the agentic pipeline initiates a loop that is more than a series of predefined searches. The agent dynamically formulates and refines its queries based on the information it gathers, actively identifying knowledge gaps, corroborating data points, and resolving discrepancies. Google Search functions as a tool the agent calls repeatedly.
- **Asynchronous, resilient execution.** A key architectural component is the ability to manage the process asynchronously. Because an investigation can involve analyzing hundreds of sources, this design makes it resilient to single-point failures and lets the user disengage and be notified upon completion. The system can also integrate user-provided documents, blending information from private sources with its web-based research.
- **Synthesis into a structured report.** The final output is not merely a concatenated list of findings but a structured, multi-page report. During synthesis, the model critically evaluates the collected information, identifies major themes, and organizes the content into a coherent narrative with logical sections. The report is designed to be interactive, often including features like an audio overview, charts, and links to the original cited sources for verification and further exploration.
- **Transparency via sources.** In addition to the synthesized results, the model explicitly returns the full list of sources it searched and consulted, presented as citations — providing complete transparency and direct access to the primary information.

By automating the iterative search-and-filter cycle (a core bottleneck in manual research), the system delivers efficiency, while its capacity to process a larger volume and variety of sources than a human could in a comparable timeframe delivers comprehensiveness. This broader scope helps reduce selection bias and increases the likelihood of uncovering less obvious but potentially critical information, leading to a more robust, well-supported understanding of the subject.

### Real-world example: OpenAI Deep Research API

The OpenAI Deep Research API is a specialized tool designed to automate complex research tasks. It uses an advanced, agentic model that can independently reason, plan, and synthesize information from real-world sources. Unlike a simple Q&A model, it takes a high-level query and autonomously breaks it into sub-questions, performs web searches using its built-in tools, and delivers a structured, citation-rich final report. The API gives direct programmatic access to this entire process. At the time of writing, it used models such as `o3-deep-research` for high-quality synthesis and the faster `o4-mini-deep-research` for latency-sensitive applications.

Its key benefits include:

- **Structured, cited output.** It produces well-organized reports with inline citations linked to source metadata, ensuring claims are verifiable and data-backed.
- **Transparency.** Unlike the abstracted process in a consumer chat product, the API exposes all intermediate steps — including the agent's reasoning, the specific web search queries it executed, and any code it ran. This supports detailed debugging, analysis, and a deeper understanding of how the final answer was constructed.
- **Extensibility.** It supports the Model Context Protocol (MCP), enabling developers to connect the agent to private knowledge bases and internal data sources, blending public web research with proprietary information.

Conceptually, a request specifies a model, an input prompt, and the tools the agent may use. The input typically includes a system/developer message defining the agent's persona and desired output format, plus the user query. A web-search tool must be included; additional tools such as a code interpreter or custom MCP tools (for internal data) are optional. The chapter's walkthrough shows that after the call returns, you can extract the final report text, then enumerate the inline citations (each carrying the cited text span, title, URL, and character location within the report), and finally inspect the intermediate steps — the model's reasoning summaries, the exact web-search queries it executed (with status), and any code the interpreter ran (with input and output). The demonstration's purpose is to make visible that a deep-research agent's output is the product of an explicit plan-reason-search-synthesize loop, not a single opaque generation.

## Practical Applications & Use Cases

The Planning pattern lets an agent move beyond simple, reactive actions to goal-oriented behavior, providing the logical framework needed to solve problems that require a coherent sequence of interdependent operations.

- **Procedural task automation / workflow orchestration.** A business process such as onboarding a new employee can be decomposed into a directed sequence of sub-tasks — creating system accounts, assigning training modules, and coordinating with different departments. The agent generates a plan to execute these steps in a logical order, invoking tools or interacting with various systems to manage dependencies.
- **Robotics and autonomous navigation (state-space traversal).** A system, whether a physical robot or a virtual entity, must generate a path or sequence of actions to transition from an initial state to a goal state. This involves optimizing for metrics such as time or energy consumption while adhering to environmental constraints, like avoiding obstacles or following traffic regulations.
- **Structured information synthesis.** When tasked with generating a complex output such as a research report, an agent can formulate a plan with distinct phases for information gathering, data summarization, content structuring, and iterative refinement.
- **Multi-step customer support.** For problem resolution that spans multiple steps, an agent can create and follow a systematic plan covering diagnosis, solution implementation, and escalation.
- **Competitive analysis.** A deep-research agent can be directed to systematically gather and collate data on market trends, competitor product specifications, public sentiment from diverse online sources, and marketing strategies — replacing the laborious manual tracking of multiple competitors and freeing analysts to focus on higher-order strategic interpretation rather than data collection.
- **Academic literature review.** The system can identify and summarize foundational papers, trace the development of concepts across numerous publications, and map out emerging research fronts within a field, accelerating the initial and most time-consuming phase of academic inquiry.

## Trade-offs & When to Use

**Rule of thumb:** Use the Planning pattern when a user's request is too complex to be handled by a single action or tool — whenever a task requires a sequence of interdependent operations to reach a final, synthesized outcome. Ideal cases include generating a detailed research report, onboarding a new employee, or executing a competitive analysis.

The central trade-off is **flexibility versus predictability**:

- **Dynamic planning** (the agent discovers the plan) maximizes adaptability and is appropriate when the path to the goal is genuinely unknown and must be discovered, or when the environment is dynamic and obstacles are likely.
- **Fixed workflows** (the plan is predetermined) are more effective when the solution is already well-understood and repeatable. Constraining the agent reduces uncertainty and the risk of unpredictable behavior, guaranteeing a reliable, consistent outcome — at the cost of autonomy.

The deciding question is always: **does the "how" need to be discovered, or is it already known?** If it is already known, prefer a fixed, predetermined workflow rather than a planning agent.

## Pitfalls

- **Misapplying dynamic planning.** Treating dynamic planning as a universal solution is a mistake. For well-understood, repeatable problems, granting the agent autonomy introduces unnecessary uncertainty and unpredictable behavior; a fixed workflow is safer and more reliable.
- **Treating the initial plan as rigid.** A plan is a starting point, not a script. An agent that cannot incorporate new information or re-plan around obstacles will simply fail when reality diverges from its first plan.
- **Failing on partial information.** Without an adaptive re-evaluation step, agents fail outright when a constraint changes (e.g., a resource becomes unavailable) instead of formulating an alternative.
- **Opacity of the planning process.** When intermediate planning, reasoning, and tool-call steps are hidden, debugging and verification become difficult — which is why exposing those steps (as the OpenAI Deep Research API does) is valuable.

## Relationships to Other Patterns

- **Tool Use.** Planning produces a sequence of steps that the agent executes largely by invoking tools (e.g., Google Search as a tool, a code interpreter, or systems involved in an onboarding workflow). Planning supplies the structure; tool use supplies the actions. The OpenAI Deep Research API also references custom MCP tools for connecting to internal/private data sources (covered in the chapter on tool use, referenced as Chapter 10).
- **Reflection.** Adaptive planning incorporates reflection — the agent evaluates gathered information, identifies knowledge gaps, corroborates and reconciles data, and revises its plan accordingly. Google Deep Research is described as an agent that "reflects, plans, and executes."
- **Multi-agent systems.** Planning can be performed by a single agent or by a system of agents; the CrewAI example uses the multi-agent "crew" framework even though it is configured with a single agent following a sequential process.

## Key Takeaways

- Planning enables agents to break down complex goals into actionable, sequential steps.
- It is essential for handling multi-step tasks, workflow automation, and navigating complex environments.
- LLMs can perform planning by generating step-by-step approaches based on task descriptions, drawing on their training data to produce plausible, effective plans.
- Explicitly prompting or designing tasks to require planning steps encourages this behavior in agent frameworks (e.g., instructing an agent to produce a plan before acting).
- A plan is a starting point, not a rigid script — adaptability (re-planning around obstacles and new information) is the source of a planning agent's real power.
- Choose dynamic planning only when the "how" must be discovered; prefer fixed workflows when the solution is already known and repeatable.
- Google Deep Research exemplifies advanced planning: it deconstructs a prompt into a reviewable research plan, then reflects, plans, and executes an iterative search-and-synthesis loop using Google Search as a tool.

## References

1. Google DeepResearch (Gemini Feature): gemini.google.com
2. OpenAI, *Introducing deep research*: https://openai.com/index/introducing-deep-research/
3. Perplexity, *Introducing Perplexity Deep Research*: https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research
