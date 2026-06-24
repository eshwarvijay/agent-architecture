# Prompt Chaining

> Prompt chaining decomposes a complex task into a sequence of smaller, focused sub-tasks, where each step is handled by its own prompt and the output of one step becomes the input to the next.

## Overview

Prompt chaining, sometimes called the **Pipeline pattern**, is a paradigm for handling intricate tasks with large language models (LLMs). Rather than expecting an LLM to solve a complex problem in a single, monolithic step, prompt chaining advocates a **divide-and-conquer strategy**: the original, daunting problem is broken into a sequence of smaller, more manageable sub-problems. Each sub-problem is addressed individually through a specifically designed prompt, and the output generated from one prompt is strategically fed as input into the subsequent prompt in the chain.

This sequential processing technique inherently introduces **modularity and clarity** into the interaction with LLMs. Decomposing a complex task makes each individual step easier to understand and debug, making the overall process more robust and interpretable. Each step can be meticulously crafted and optimized to focus on a specific aspect of the larger problem, leading to more accurate and focused outputs.

The crucial mechanism is that the **output of one step acts as the input for the next**. This passing of information establishes a dependency chain (hence the name), where the context and results of previous operations guide subsequent processing. It allows the LLM to build on its previous work, refine its understanding, and progressively move closer to the desired solution.

Prompt chaining is not just about breaking down problems; it also enables the **integration of external knowledge and tools**. At each step, the LLM can be instructed to interact with external systems, APIs, or databases, enriching its knowledge and abilities beyond its internal training data. This expands the potential of LLMs, allowing them to function not as isolated models but as integral components of broader, more intelligent systems.

The significance of prompt chaining extends beyond simple problem-solving — it is a **foundational technique for building sophisticated AI agents**. Agents can use prompt chains to autonomously plan, reason, and act in dynamic environments. By strategically structuring the sequence of prompts, an agent can engage in tasks requiring multi-step reasoning, planning, and decision-making, mimicking human thought processes more closely and enabling more natural and effective interactions with complex domains and systems.

### Why single prompts fall short

For multifaceted tasks, using a single, complex prompt is inefficient and causes the model to struggle with constraints and instructions. Specific failure modes include:

- **Instruction neglect** — parts of the prompt are overlooked.
- **Contextual drift** — the model loses track of the initial context.
- **Error propagation** — early errors amplify through the rest of the response.
- **Insufficient context window** — prompts that need a longer context window leave the model with insufficient information to respond.
- **Hallucination** — increased cognitive load raises the chance of incorrect information.

The chapter's running example: a query that asks an LLM to *analyze a market research report, summarize the findings, identify trends with supporting data points, and draft an email* risks failure because the model might summarize well but fail to extract data or draft the email properly.

## How It Works

Prompt chaining addresses the single-prompt failures by breaking the complex task into a focused, sequential workflow, which significantly improves reliability and control.

**The market-research example as a chain.** The monolithic request above is decomposed into three sequential steps:

1. **Initial prompt (Summarization)** — "Summarize the key findings of the following market research report: [text]." The model's sole focus is summarization, increasing the accuracy of this initial step.
2. **Second prompt (Trend Identification)** — "Using the summary, identify the top three emerging trends and extract the specific data points that support each trend: [output from step 1]." This prompt is now more constrained and builds directly upon a validated output.
3. **Third prompt (Email Composition)** — "Draft a concise email to the marketing team that outlines the following trends and their supporting data: [output from step 2]."

This decomposition gives more granular control over the process. Each step is simpler and less ambiguous, which reduces the cognitive load on the model and leads to a more accurate and reliable final output. The modularity is analogous to a **computational pipeline** where each function performs a specific operation before passing its result to the next.

**Assigning roles per stage.** To ensure an accurate response for each specific task, the model can be assigned a distinct role at every stage. In the market-research scenario, the first prompt could be designated "Market Analyst," the second "Trade Analyst," and the third "Expert Documentation Writer," and so on. Role assignment focuses the model on the concerns relevant to each step.

**The role of structured output.** The reliability of a prompt chain is highly dependent on the integrity of the data passed between steps. If the output of one prompt is ambiguous or poorly formatted, the subsequent prompt may fail due to faulty input. To mitigate this, specifying a **structured output format such as JSON or XML is crucial**. For example, the trend-identification step can emit a JSON object holding a list of trends, each with a `trend_name` and `supporting_data` field. A structured format ensures the data is machine-readable and can be precisely parsed and inserted into the next prompt without ambiguity. This minimizes the errors that arise from interpreting natural language and is a key component in building robust, multi-step LLM-based systems.

**Inserting deterministic logic between steps.** A major benefit of chaining is that ordinary (non-LLM) program logic can run between model calls. This allows intermediate data processing, output validation, and conditional branching within the workflow — turning a single, multifaceted request that could otherwise produce unreliable or incomplete results into a structured sequence of operations managed by an underlying execution framework.

**Conceptual walk-through of the chapter's code example.** The hands-on example builds a **two-step prompt chain that acts as a data-processing pipeline**, implemented with LangChain. The first stage parses unstructured text and extracts specific information — given an input string describing a laptop, it extracts the technical specifications. The second stage receives that extracted output and transforms it into a structured JSON object keyed by `cpu`, `memory`, and `storage`. The two prompts (one for extraction, one for JSON transformation) are linked using the LangChain Expression Language (LCEL), with an output parser ensuring each step yields a usable string. The first chain extracts the specifications; the full chain then feeds that extraction output into the transformation prompt's input variable. When invoked on the sample laptop description, the chain runs both steps in sequence and produces a final JSON string of the extracted, formatted specifications. The point it demonstrates is the core mechanic of the pattern: each step does one focused job and its output is wired directly into the next step's input.

## Practical Applications & Use Cases

Prompt chaining is a versatile pattern applicable across many agentic scenarios. Its core utility lies in breaking complex problems into sequential, manageable steps.

1. **Information Processing Workflows.** Many tasks process raw information through multiple transformations — e.g., summarizing a document, extracting key entities, then using those entities to query a database or generate a report. A representative chain: (1) extract text content from a URL or document; (2) summarize the cleaned text; (3) extract specific entities (names, dates, locations) from the summary or original text; (4) use the entities to search an internal knowledge base; (5) generate a final report incorporating the summary, entities, and search results. Applied in automated content analysis, AI-driven research assistants, and complex report generation.

2. **Complex Query Answering.** Answering questions that require multiple reasoning or retrieval steps. Example: *"What were the main causes of the stock market crash in 1929, and how did government policy respond?"* The chain: (1) identify the core sub-questions in the user's query; (2) research/retrieve information about the causes of the crash; (3) research/retrieve information about the government's policy response; (4) synthesize the information from the prior steps into a coherent answer. Such systems are needed when a query cannot be answered from a single data point but requires a series of logical steps or integration of information from diverse sources.

   The chapter notes that complex operations frequently **combine parallel processing with prompt chaining**. An automated research agent generating a comprehensive report runs a *hybrid* workflow: it first retrieves many relevant articles, then extracts key information from each article *concurrently* (a well-suited use of parallel processing, since the per-article extractions are independent). Once individual extractions are complete, the process becomes inherently *sequential* — the system must collate the extracted data, synthesize it into a coherent draft, then review and refine that draft into a final report. Each later stage depends on the successful completion of the preceding one: the collated data is the input to the synthesis prompt, and the synthesized text is the input to the final review prompt. So parallel processing handles independent data gathering, while prompt chaining handles the dependent steps of synthesis and refinement.

3. **Data Extraction and Transformation.** Converting unstructured text into a structured format is typically iterative, requiring sequential modifications to improve accuracy and completeness, often with validation and conditional re-prompting between steps. A representative loop: (1) attempt to extract specific fields (name, address, amount) from an invoice; (2) processing step checks whether all required fields were extracted and meet format requirements; (3) conditional prompt — if fields are missing or malformed, craft a new prompt asking the model to specifically find the missing/malformed information, possibly providing context from the failed attempt; (4) validate again and repeat if necessary; (5) output the extracted, validated structured data.

   This applies to data extraction from forms, invoices, or emails. The chapter gives a detailed **OCR example**: processing a PDF form is more effectively handled by a decomposed, multi-step approach. First, an LLM performs the primary text extraction from the document image. Next, the model normalizes the raw output — for instance, converting numeric text like "one thousand and fifty" into its numerical equivalent, 1050. Because precise mathematical calculation is a significant challenge for LLMs, a subsequent step **delegates any required arithmetic to an external calculator tool**: the LLM identifies the needed calculation, feeds the normalized numbers to the tool, and incorporates the precise result. This chained sequence (text extraction → data normalization → external tool use) achieves a final accurate result that is often hard to obtain reliably from a single LLM query.

4. **Content Generation Workflows.** Composing complex content is a procedural task decomposed into distinct phases: ideation, structural outlining, drafting, and revision. A representative chain: (1) generate several topic ideas based on a user's general interest; (2) processing step lets the user select one (or auto-choose the best); (3) generate a detailed outline for the selected topic; (4) write a draft section for the first outline point; (5) write subsequent sections one at a time, providing previous sections as context, continuing for all outline points; (6) review and refine the complete draft for coherence, tone, and grammar. Used for creative narratives, technical documentation, and other structured textual content.

5. **Conversational Agents with State.** Although comprehensive state-management architectures use methods more complex than simple sequential linking, prompt chaining provides a **foundational mechanism for preserving conversational continuity**. The technique maintains context by constructing each conversational turn as a new prompt that systematically incorporates information or extracted entities from preceding interactions. A representative flow: (1) process the first user utterance, identifying intent and key entities; (2) processing step updates the conversation state with intent and entities; (3) based on current state, generate a response and/or identify the next required piece of information; repeat for subsequent turns, with each new utterance initiating a chain that leverages the accumulating conversation history (state). This is fundamental to conversational agents maintaining context and coherence across extended, multi-turn dialogues.

6. **Code Generation and Refinement.** Generating functional code is a multi-stage process: a problem is decomposed into a sequence of discrete logical operations executed progressively. A representative chain: (1) understand the user's request and generate pseudocode or an outline; (2) write the initial code draft from the outline; (3) identify potential errors or improvement areas (perhaps using a static analysis tool or another LLM call); (4) rewrite or refine the code based on identified issues; (5) add documentation or test cases. The modular structure reduces operational complexity at each step and allows inserting deterministic logic (validation, conditional branching) between model calls.

7. **Multimodal and Multi-step Reasoning.** Analyzing datasets with diverse modalities requires breaking the problem into smaller prompt-based tasks. Example: interpreting an image that contains a picture with embedded text, labels highlighting specific text segments, and tabular data explaining each label. A representative chain: (1) extract and comprehend the text from the image; (2) link the extracted text with its corresponding labels; (3) interpret the gathered information using the table to determine the required output.

## Trade-offs & When to Use

**Rule of thumb (when to use):** Use prompt chaining when a task is too complex for a single prompt, involves multiple distinct processing stages, requires interaction with external tools between steps, or when building agentic systems that need to perform multi-step reasoning and maintain state.

**Benefits:**
- Significantly improves **reliability and control** by focusing the model on one specific operation at a time, reducing cognitive load.
- Makes the process **more manageable and easier to debug**, because each step can be inspected and optimized in isolation.
- Allows the **integration of external tools and structured data formats** between steps.
- Enables inserting **deterministic logic** (validation, conditional branching, intermediate processing) between model calls.
- Foundational for multi-step agentic systems that plan, reason, and execute.

**Costs / limitations:**
- Reliability is **highly dependent on the integrity of data passed between steps** — ambiguous or poorly formatted intermediate output can cause downstream prompts to fail (mitigated by structured output formats).
- Comprehensive state management generally needs methods **more sophisticated than simple sequential linking**; chaining is a foundational mechanism, not a complete state architecture.
- Implementation ranges from direct sequential function calls in a script up to specialized frameworks; complex architectures benefit from frameworks that manage control flow, state, and component integration.

## Pitfalls

- **Faulty intermediate input.** If one step's output is ambiguous or poorly formatted, the next step may fail. The chapter's mitigation is to specify structured output (JSON/XML) so data is machine-readable and parsed without ambiguity.
- **Error propagation.** Because steps are dependent, an early error can amplify through the chain — a reason to validate intermediate outputs (and to use conditional re-prompting, as in the data-extraction loop).
- **Treating chaining as full state management.** Relying on sequential linking alone for conversational state under-serves complex use cases; real state architectures go beyond simple chaining.

## Relationships to Other Patterns

- **Parallelization.** Complex real-world workflows often combine *parallel processing* (for independent sub-tasks like extracting from many articles simultaneously) with *prompt chaining* (for the dependent synthesis and refinement steps that must run in order). The two are complementary stages of one pipeline.
- **Tool Use / external integration.** Chaining naturally incorporates calls to external systems, APIs, databases, and tools (e.g., delegating arithmetic to a calculator tool) between steps, enriching the LLM beyond its training data.
- **Routing / conditional workflows.** Deterministic logic inserted between steps enables conditional branching, connecting chaining to routing-style control flow.
- **Foundation for agents.** Prompt chaining is presented as a foundational pattern on which sophisticated agentic systems (multi-step reasoning, planning, state management) are built.
- **Context Engineering vs. Prompt Engineering.** The chapter contrasts these two disciplines (see below); chaining is one mechanism within the broader practice of constructing the informational environment an agent operates in.

### Context Engineering and Prompt Engineering

The chapter includes an extended discussion distinguishing **Context Engineering** from traditional prompt engineering. Context Engineering is the systematic discipline of designing, constructing, and delivering a *complete informational environment* to an AI model **prior to token generation**. Its core assertion is that output quality depends less on the model's architecture and more on the richness of the context provided.

It represents an evolution from traditional **prompt engineering**, which focuses primarily on optimizing the phrasing of a user's immediate query. Context Engineering expands the scope to include several layers of information:

- The **system prompt** — a foundational set of instructions defining the AI's operational parameters (e.g., "You are a technical writer; your tone must be formal and precise.").
- **Retrieved documents** — information the AI actively fetches from a knowledge base to inform its response (e.g., pulling technical specifications for a project).
- **Tool outputs** — results from the AI using an external API to obtain real-time data (e.g., querying a calendar to determine availability).
- **Implicit data** — user identity, interaction history, and environmental state.

The core principle is that even advanced models underperform when given a limited or poorly constructed view of the operational environment. The practice reframes the task from merely *answering a question* to *building a comprehensive operational picture* for the agent. The chapter's example: a context-engineered email-drafting agent would integrate the user's calendar availability (tool output), the professional relationship with the recipient (implicit data), and notes from previous meetings (retrieved documents) before responding — producing outputs that are highly relevant, personalized, and pragmatically useful.

The **"engineering"** component involves building robust pipelines to fetch and transform this data at runtime and establishing feedback loops to continually improve context quality. Specialized tuning systems can automate this at scale — the chapter cites **Google's Vertex AI prompt optimizer**, which systematically evaluates responses against sample inputs and predefined evaluation metrics, adapting prompts and system instructions across different models without extensive manual rewriting. Ultimately, Context Engineering is the methodology for advancing stateless chatbots into highly capable, situationally-aware systems.

## Key Takeaways

- Prompt Chaining breaks down complex tasks into a sequence of smaller, focused steps; it is occasionally known as the **Pipeline pattern**.
- Each step in a chain involves an LLM call or processing logic, using the output of the previous step as input.
- The pattern improves the **reliability and manageability** of complex interactions with language models by focusing the model on one operation at a time.
- **Structured output** (JSON/XML) between steps is crucial for reliable data passing.
- Deterministic logic, validation, and conditional branching can be inserted between model calls.
- Frameworks like **LangChain/LangGraph**, **CrewAI**, and **Google ADK** provide robust tools to define, manage, and execute these multi-step sequences. LangChain offers foundational abstractions for linear sequences; LangGraph extends these to stateful and cyclical computations needed for more sophisticated agentic behaviors.
- Prompt chaining is **foundational** for developing multi-step agentic systems capable of planning, reasoning, tool integration, and state management — enabling workflows well beyond the capability of a single prompt.

## References

1. LangChain Documentation on LCEL — https://python.langchain.com/v0.2/docs/core_modules/expression_language/
2. LangGraph Documentation — https://langchain-ai.github.io/langgraph/
3. Prompt Engineering Guide – Chaining Prompts — https://www.promptingguide.ai/techniques/chaining
4. OpenAI API Documentation (General Prompting Concepts) — https://platform.openai.com/docs/guides/gpt/prompting
5. Crew AI Documentation (Tasks and Processes) — https://docs.crewai.com/
6. Google AI for Developers (Prompting Guides) — https://cloud.google.com/discover/what-is-prompt-engineering?hl=en
7. Vertex Prompt Optimizer — https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-optimizer
