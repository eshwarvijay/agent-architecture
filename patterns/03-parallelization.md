# Parallelization

> Executing multiple independent components of an agentic workflow — LLM calls, tool usages, or entire sub-agents — concurrently rather than one after another, to reduce overall execution time.

## Overview

Earlier patterns covered Prompt Chaining (sequential workflows) and Routing (dynamic decision-making and transitions between paths). While essential, many complex agentic tasks involve multiple sub-tasks that can be executed simultaneously rather than one after another. Parallelization addresses exactly this situation.

Parallelization involves executing multiple components — such as LLM calls, tool usages, or even entire sub-agents — concurrently. Instead of waiting for one step to complete before starting the next, parallel execution lets independent tasks run at the same time, significantly reducing the overall execution time for any task that can be broken into independent parts.

A concrete contrast illustrates the gain. Consider an agent that researches a topic and summarizes its findings. A purely **sequential** approach would: (1) search for Source A, (2) summarize Source A, (3) search for Source B, (4) summarize Source B, and (5) synthesize a final answer from summaries A and B. A **parallel** approach instead: (1) searches for Source A and Source B simultaneously, (2) once both searches complete, summarizes Source A and Source B simultaneously, and (3) synthesizes the final answer from both summaries — this final step is typically sequential, waiting for the parallel steps to finish.

The core idea is to identify parts of the workflow that do not depend on the output of other parts and execute them in parallel. This is particularly effective when dealing with external services (such as APIs or databases) that have latency, since you can issue multiple requests concurrently rather than serializing the wait time.

Implementing parallelization often requires frameworks that support asynchronous execution or multi-threading/multi-processing. Modern agentic frameworks are designed with asynchronous operations in mind, allowing steps that can run in parallel to be defined easily. The pattern is vital for improving the efficiency and responsiveness of agentic systems, especially for tasks that involve multiple independent lookups, computations, or interactions with external services. It is a key technique for optimizing the performance of complex agent workflows.

## How It Works

The mechanism rests on distinguishing dependent from independent work, then dispatching the independent work concurrently and rejoining the results at a later convergence point. Several frameworks provide built-in support:

- **LangChain (LCEL):** In the LangChain Expression Language, sequential composition is expressed with the pipe operator, while parallel execution is achieved by structuring chains or graphs to have branches that execute concurrently. The primary method is to bundle multiple runnable components within a dictionary or list construct. When that collection is passed as input to a subsequent component in the chain, the LCEL runtime executes the contained runnables concurrently. `RunnableParallel` is the key construct for running multiple runnables side-by-side; `RunnablePassthrough` can be used to forward the original input through the parallel block so it remains available to downstream steps.

- **LangGraph:** Parallelism is expressed through the graph's topology. Multiple nodes that lack direct sequential dependencies can be initiated from a single common node, creating parallel branches in the workflow. These parallel pathways execute independently and their results are aggregated at a subsequent convergence point in the graph.

- **Google ADK:** Provides robust, native mechanisms to facilitate and manage parallel execution of agents, enhancing the efficiency and scalability of complex multi-agent systems. The framework lets developers design solutions where multiple agents operate concurrently rather than sequentially. ADK's key primitives include `ParallelAgent` (orchestrates concurrent execution of its sub-agents and completes once all of them finish and store their results) and `SequentialAgent` (orchestrates an overall flow of steps in order). ADK can also achieve parallelism through **LLM-Driven Delegation**, where a Coordinator/primary agent's LLM identifies independent sub-tasks and triggers their concurrent handling by specialized sub-agents.

### Walkthrough: LangChain example (described in prose)

The chapter demonstrates a parallel-plus-synthesis workflow built with LangChain. Prerequisites include installing the relevant Python packages (a core LangChain library, a community library, and a model-provider library) and configuring a valid API key for the chosen language model in the local environment.

The workflow processes a single user-supplied topic by running three independent operations concurrently and then combining their outputs:

1. A language model instance is initialized (a small chat model with a moderate temperature for some creativity), wrapped in error handling so initialization failures are caught gracefully.
2. **Three independent chains** are defined, each performing a distinct task on the same input topic: one summarizes the topic concisely; one generates three interesting questions about it; and one identifies five to ten key terms (comma-separated). Each chain is composed of a task-specific prompt template, the language model, and a string output parser.
3. A **parallel block** bundles the three chains so they execute simultaneously. The block also includes a passthrough so the original topic remains available to later steps.
4. A separate **synthesis prompt** takes the summary, questions, key terms, and the original topic, and instructs the model to produce a comprehensive answer.
5. The full end-to-end chain is built by piping the parallel block into the synthesis prompt, then the language model, then the output parser.
6. An asynchronous driver function invokes the full chain on a sample topic (the example uses "The history of space exploration") and prints the synthesized result; the standard Python async entry point manages execution.

A crucial conceptual caveat the chapter emphasizes: `asyncio` provides **concurrency, not parallelism**. It runs on a single thread using an event loop that intelligently switches between tasks when one is idle (for example, waiting on a network request). This creates the *effect* of multiple tasks progressing at once, but the code is still executed by only one thread, constrained by Python's Global Interpreter Lock (GIL). The benefit comes from overlapping I/O waits, not from true multi-core execution.

### Walkthrough: Google ADK example (described in prose)

The chapter then builds an equivalent multi-agent system in Google ADK to research and synthesize information on sustainable-technology advancements:

1. **Three researcher sub-agents** are defined as LLM-backed agents, each specialized: one researches renewable energy sources, one researches electric-vehicle technology, and one researches carbon-capture methods. Each is configured with a Gemini model and a Google Search tool, is instructed to summarize its findings concisely (one to two sentences) and output only the summary, and stores its result into the shared session state under a distinct output key.
2. A **ParallelAgent** is created to run the three researchers concurrently. It orchestrates their concurrent execution and finishes only once all sub-agents have completed and written their results into state.
3. A **merger (synthesis) agent** — also an LLM agent — reads the three summaries from session state and synthesizes them into a single structured report with headings per topic, source attributions, and a brief overall conclusion. Its instruction strictly grounds the output exclusively on the provided input summaries, prohibiting the addition of any external knowledge or facts not present in those summaries. It needs no tools and no output key, since its direct response is the final output.
4. A **SequentialAgent** orchestrates the whole pipeline: it first runs the ParallelAgent to populate state, then runs the merger agent to produce the final output. This sequential pipeline is set as the root agent and is the entry point for the system.

This example illustrates the common composite shape: a parallel fan-out stage for independent work, feeding a sequential synthesis stage that converges the results.

## Practical Applications & Use Cases

Parallelization optimizes agent performance across many application types:

1. **Information Gathering and Research** — the classic case: collecting information from multiple sources simultaneously. Example: an agent researching a company runs news-article search, stock-data pull, social-media-mention check, and company-database query all at once, gathering a comprehensive view far faster than sequential lookups.
2. **Data Processing and Analysis** — applying different analysis techniques or processing different data segments concurrently. Example: an agent analyzing customer feedback runs sentiment analysis, keyword extraction, categorization, and urgent-issue identification simultaneously across a batch of feedback entries, producing a multi-faceted analysis quickly.
3. **Multi-API or Tool Interaction** — calling multiple independent APIs or tools to gather different information or perform different actions. Example: a travel-planning agent checks flight prices, hotel availability, local events, and restaurant recommendations concurrently, presenting a complete plan faster.
4. **Content Generation with Multiple Components** — generating different parts of a complex piece of content in parallel. Example: an agent creating a marketing email generates the subject line, drafts the body, finds a relevant image, and creates call-to-action button text simultaneously, then assembles the email more efficiently.
5. **Validation and Verification** — performing multiple independent checks concurrently. Example: an agent verifying user input checks email format, validates the phone number, verifies the address against a database, and checks for profanity simultaneously, giving faster feedback on validity.
6. **Multi-Modal Processing** — processing different modalities (text, image, audio) of the same input concurrently. Example: an agent analyzing a social-media post analyzes the text for sentiment and keywords while analyzing the image for objects and scene description, integrating cross-modal insights more quickly.
7. **A/B Testing or Multiple Options Generation** — generating multiple variations of a response in parallel to select the best one. Example: an agent generates three different article headlines simultaneously using slightly different prompts or models, enabling quick comparison and selection.

Across all of these, parallelization is a fundamental optimization technique that lets developers build more performant and responsive applications by leveraging concurrent execution for independent tasks.

## Trade-offs & When to Use

**The problem it solves:** In a purely sequential execution, each task waits for the previous one to finish, so total processing time is the *sum* of all individual task durations. This latency becomes a significant bottleneck when tasks depend on external I/O operations — calling different APIs, querying multiple databases — and hinders the system's overall performance and responsiveness.

**Why the pattern helps:** By identifying workflow components (tool usages or LLM calls) that do not rely on each other's immediate outputs and running them at the same time, the pattern drastically reduces total execution time. A main process can invoke several sub-tasks that run in parallel and wait for all of them to complete before proceeding to the next step.

**Cost:** Adopting a concurrent or parallel architecture introduces substantial complexity and cost. It impacts key development phases including design, debugging, and system logging — concurrent execution is harder to reason about, harder to trace, and harder to log coherently than straight-line sequential code. This overhead must be weighed against the latency savings.

**Rule of thumb:** Use this pattern when a workflow contains multiple independent operations that can run simultaneously — fetching data from several APIs, processing different chunks of data, or generating multiple pieces of content for later synthesis. Conversely, if tasks are tightly dependent (each needs the prior one's output), parallelization offers little and adds needless complexity.

## Pitfalls

- **Concurrency is not parallelism.** Single-threaded async runtimes (such as Python's `asyncio`) interleave tasks during idle/I/O waits on one thread, constrained by the GIL. This speeds up I/O-bound workloads but does not provide true multi-core CPU parallelism — understand which kind of speedup your workload actually needs.
- **Grounding in synthesis steps.** When a synthesis/merger step combines parallel results, it can drift and introduce external information. The ADK example explicitly instructs the merger agent to ground its output *exclusively* on the provided input summaries and add no outside knowledge — a deliberate guardrail against hallucination at the convergence point.
- **Increased operational complexity.** Design, debugging, and logging all become harder under concurrency; budget for this overhead.

## Relationships to Other Patterns

- **Prompt Chaining (sequential):** Parallelization is the concurrent counterpart to sequential chaining. The two compose naturally — the canonical shape is a parallel fan-out feeding a sequential synthesis/convergence step (as in both the LangChain and ADK examples, where independent branches run concurrently and a final sequential step combines them).
- **Routing (conditional):** Routing handles dynamic, conditional branching between paths. Integrating parallel processing with sequential (chaining) and conditional (routing) control flows makes it possible to construct sophisticated, high-performance systems that efficiently manage diverse and complex tasks.
- **Multi-agent delegation:** In ADK, parallelization can be realized through multi-agent delegation, where a primary coordinator model assigns different sub-tasks to specialized agents that operate concurrently.

## Key Takeaways

- Parallelization is a pattern for executing independent tasks concurrently to improve efficiency.
- It is particularly useful when tasks involve waiting for external resources, such as API calls.
- Adopting a concurrent or parallel architecture introduces substantial complexity and cost, impacting design, debugging, and system logging.
- Frameworks like LangChain and Google ADK provide built-in support for defining and managing parallel execution.
- In LangChain Expression Language (LCEL), `RunnableParallel` is a key construct for running multiple runnables side-by-side.
- Google ADK can facilitate parallel execution through LLM-Driven Delegation, where a Coordinator agent's LLM identifies independent sub-tasks and triggers their concurrent handling by specialized sub-agents.
- Parallelization reduces overall latency and makes agentic systems more responsive for complex tasks.
- Remember that single-threaded async (e.g., `asyncio`) provides concurrency, not true parallelism.

## References

1. LangChain Expression Language (LCEL) Documentation (Parallelism): https://python.langchain.com/docs/concepts/lcel/
2. Google Agent Developer Kit (ADK) Documentation (Multi-Agent Systems): https://google.github.io/adk-docs/agents/multi-agents/
3. Python `asyncio` Documentation: https://docs.python.org/3/library/asyncio.html
