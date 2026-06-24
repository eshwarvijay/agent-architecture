# Tool Use (Function Calling)

> A pattern that lets an agent's LLM decide when and how to invoke external functions, APIs, databases, services, or even other agents, so it can act on and retrieve information from the world beyond its own training data.

## Overview

Earlier agentic patterns (Chaining, Routing, Parallelization, Reflection) are mostly about orchestrating interactions between language models and managing the flow of information inside the agent's own internal workflow. Tool Use is the pattern that lets agents step outside that internal loop and interact with the real world and external systems.

Tool Use is typically implemented through a mechanism called **function calling**. It enables an agent to interact with external APIs, databases, and services, or to execute code. The LLM at the core of the agent decides, based on the user's request or the current state of the task, when and how to use a specific external function.

This pattern is fundamental because it breaks the limitations of the LLM's training data. It lets the model access up-to-date information, perform calculations it cannot do reliably on its own, interact with user-specific data, and trigger real-world actions. Function calling is the technical mechanism that bridges the gap between the LLM's reasoning capabilities and the vast array of external functionalities available.

**Function calling vs. the broader notion of "tool calling."** While "function calling" aptly describes invoking specific, predefined code functions, it is useful to consider the more expansive concept of "tool calling." This broader framing acknowledges that an agent's capabilities can extend well beyond simple function execution. A "tool" can be a traditional function, but it can also be a complex API endpoint, a request to a database, or even an instruction directed at another specialized agent. This perspective enables more sophisticated systems — for instance, a primary agent might delegate a complex data-analysis task to a dedicated "analyst agent," or query an external knowledge base through its API. Thinking in terms of tool calling better captures the full potential of agents to act as orchestrators across a diverse ecosystem of digital resources and other intelligent entities.

Frameworks such as LangChain, LangGraph, and the Google Agent Developer Kit (ADK) provide robust support for defining tools and integrating them into agent workflows, often leveraging the native function-calling capabilities of modern LLMs such as those in the Gemini and OpenAI series. Within these frameworks, you define the tools and then configure agents (typically LLM agents) to be aware of and capable of using those tools. Tool Use is a cornerstone pattern for building powerful, interactive, and externally aware agents — it is what transforms a language model from a text generator into an agent capable of sensing, reasoning, and acting in the digital or physical world.

## How It Works

The Tool Use process typically unfolds in the following steps:

1. **Tool Definition.** External functions or capabilities are defined and described to the LLM. This description includes the function's purpose, its name, and the parameters it accepts — along with the types and descriptions of those parameters. The quality of these descriptions matters, because the model relies on them to understand what each tool does and how to call it.

2. **LLM Decision.** The LLM receives the user's request together with the available tool definitions. Based on its understanding of the request and the tools, it decides whether calling one or more tools is necessary to fulfill the request. If no tool is needed, it can simply answer directly.

3. **Function Call Generation.** If the LLM decides to use a tool, it generates a structured output (often a JSON object) that specifies the name of the tool to call and the arguments/parameters to pass to it, with those arguments extracted from the user's request. Importantly, the model does not execute anything itself at this stage; it only emits a structured request describing the call it wants made.

4. **Tool Execution.** The agentic framework or orchestration layer intercepts this structured output. It identifies the requested tool and executes the actual external function with the provided arguments. This separation — the model proposes, the orchestration layer disposes — is central to the pattern.

5. **Observation / Result.** The output or result from the tool execution is returned to the agent.

6. **LLM Processing (optional but common).** The LLM receives the tool's output as context and uses it to formulate a final response to the user, or to decide on the next step in the workflow. That next step might be calling another tool, reflecting, or providing a final answer.

### Framework illustrations

The chapter walks through several framework examples. Code is omitted here; each is described for what it demonstrates conceptually.

- **LangChain.** Tool use in LangChain is a two-stage process. First, one or more tools are defined, typically by encapsulating existing functions or other runnable components and giving each a clear natural-language description of its purpose and the kinds of queries it handles. Second, these tools are bound to a language model (one with function/tool-calling capability), which grants the model the ability to generate a structured tool-use request when it determines an external call is required. The worked example defines a simulated information-retrieval tool whose description tells the model what sorts of questions it answers (e.g., "capital of France," "weather in London"); the tool returns canned answers for a few known queries and a default response otherwise. An agent is assembled from the model, the tools, and a prompt template, then run by an executor that manages the agent's reasoning loop and actually invokes the chosen tools. Multiple queries are run to show both the specific and the default tool responses. Conceptually, LangChain simplifies tool definition (e.g., a decorator that turns a function into a tool) and provides higher-level constructs for building and running a tool-calling agent.

- **CrewAI.** This example shows function calling in a role-based, multi-agent framework. A custom tool simulates looking up a stock price for a ticker. Notably, the tool is designed to return clean, raw data (a floating-point price) for valid tickers and to raise a standard error for unknown ones, rather than returning an error string — this makes the tool more reusable and forces the agent to handle success and failure outcomes properly. An agent is defined with a role ("Senior Financial Analyst"), a goal, and a backstory, and is given the stock-price tool. A task is defined with a specific description that guides the agent on how to react both when data is retrieved and when the lookup fails, plus an expected-output format. The agent and task are assembled into a crew, which orchestrates how they work together, and the crew is run to produce the final answer. The example illustrates how tools, agents, and tasks compose into a collaborative workflow.

- **Google ADK — pre-built tools.** ADK ships a library of natively integrated tools that can be dropped directly into an agent's capabilities:
  - **Google Search.** A pre-built tool that acts as a direct interface to the Google Search engine, giving the agent the ability to perform web searches and retrieve external information. The example defines a basic search agent, attaches the Google Search tool, sets up an in-memory session service and a runner, and answers a question like "what's the latest AI news?" by iterating over the agent's events to extract the final response.
  - **Code Execution.** ADK provides a built-in code-execution tool that gives an agent a sandboxed Python interpreter. This lets the model write and run code to perform computational tasks, manipulate data structures, and execute procedural scripts. Such functionality is critical for problems that require deterministic logic and precise calculations — things outside the scope of probabilistic language generation alone. The example defines a "calculator" agent instructed to solve math by writing and executing Python and returning only the numeric result; the surrounding logic distinguishes the intermediate steps (the generated code and its execution result) from the final answer.
  - **Enterprise / Vertex AI Search.** A specialized search agent answers questions by searching a specified Vertex AI Search datastore (identified by a datastore ID). It is wired to a runner with an in-memory session service, streams the agent's response back as it arrives, and reports final-response metadata including source attributions (grounding) from the datastore. Error handling surfaces issues such as an incorrect datastore ID or missing permissions. This demonstrates retrieving and synthesizing information from a private datastore to answer user queries.

- **Vertex AI Extensions.** A Vertex AI extension is a structured API wrapper that lets a model connect with external APIs for real-time data processing and action execution. Extensions offer enterprise-grade security, data privacy, and performance guarantees, and can be used for tasks such as generating and running code, querying websites, and analyzing information from private datastores. Google provides prebuilt extensions for common use cases (e.g., Code Interpreter and Vertex AI Search), with the option to create custom ones. The benefits include strong enterprise controls and seamless integration with other Google products. The key distinction from plain function calling lies in execution: **Vertex AI automatically executes extensions, whereas function calls require manual execution by the user or client** (the orchestration layer).

## Practical Applications & Use Cases

Tool Use applies in virtually any scenario where an agent must go beyond generating text to perform an action or retrieve specific, dynamic information:

1. **Information retrieval from external sources.** Accessing real-time data not present in the LLM's training data. Example: a weather agent. Tool: a weather API that takes a location and returns current conditions. Flow: user asks "What's the weather in London?"; the LLM identifies the need for the weather tool, calls it with "London," receives data, and formats it into a user-friendly response.

2. **Interacting with databases and APIs.** Performing queries, updates, or other operations on structured data. Example: an e-commerce agent with API calls to check inventory, get order status, or process payments. Flow: user asks "Is product X in stock?"; the LLM calls the inventory API, gets a stock count, and reports the status.

3. **Performing calculations and data analysis.** Using external calculators, data-analysis libraries, or statistical tools. Example: a financial agent with a calculator function, a stock-market data API, and a spreadsheet tool. Flow: user asks for AAPL's current price and the potential profit on 100 shares bought at $150; the LLM calls the stock API, then the calculator, then formats the response. This shows chaining multiple tool calls within one request.

4. **Sending communications.** Sending emails or messages, or calling external communication services. Example: a personal-assistant agent with an email-sending API. Flow: user says "Send an email to John about the meeting tomorrow"; the LLM calls the email tool with the recipient, subject, and body extracted from the request.

5. **Executing code.** Running code snippets in a safe environment. Example: a coding-assistant agent with a code interpreter. Flow: user provides a Python snippet and asks what it does; the LLM uses the interpreter tool to run the code and analyze its output.

6. **Controlling other systems or devices.** Interacting with smart-home devices, IoT platforms, or other connected systems. Example: a smart-home agent with an API to control lights. Flow: user says "Turn off the living room lights"; the LLM calls the smart-home tool with the command and target device.

## Trade-offs & When to Use

**What problem it solves.** LLMs are powerful text generators but are fundamentally disconnected from the outside world. Their knowledge is static, limited to their training data, and they lack the ability to perform actions or retrieve real-time information. Without a bridge to external systems, their utility for real-world problems is severely constrained.

**Why the pattern works.** Tool Use provides a standardized solution: describe available external functions ("tools") to the LLM in a way it can understand; let the LLM decide whether a tool is needed and emit a structured request (e.g., JSON) naming the function and its arguments; have an orchestration layer execute the call, retrieve the result, and feed it back to the LLM. The model then incorporates up-to-date external information or the result of an action into its final response — effectively giving it the ability to act.

**Rule of thumb.** Use Tool Use whenever an agent needs to break out of the LLM's internal knowledge and interact with the outside world. This is essential for tasks requiring:
- real-time data (e.g., weather, stock prices);
- access to private or proprietary information (e.g., querying a company's database);
- precise calculations;
- executing code;
- triggering actions in other systems (e.g., sending an email, controlling smart devices).

A notable execution trade-off appears in the Vertex AI comparison: managed **extensions execute automatically** (less control wiring, strong enterprise guardrails, tighter Google-ecosystem integration), whereas **plain function calls require manual execution** by the client/orchestration layer (more control and portability, more responsibility on the developer).

## Pitfalls

- A tool that returns error messages as ordinary strings can mask failures from the agent. The CrewAI example deliberately raises a standard error for an unknown ticker instead of returning an error string, so the agent is forced to recognize and handle the failure outcome rather than treating it as valid data.
- Weak or ambiguous tool descriptions and parameter definitions undermine the LLM's ability to choose the right tool and supply correct arguments, since the model's tool selection depends entirely on those descriptions.
- The model only proposes a structured call; the orchestration layer must reliably parse it and execute the real function. For managed extensions execution is automatic, but for ordinary function calling, forgetting that execution is the client's responsibility is a common source of confusion.
- External integrations introduce operational failure modes — wrong identifiers (e.g., an incorrect datastore ID), missing permissions, and runtime/event-loop conflicts — that must be handled gracefully, as the Vertex AI Search example illustrates.

## Relationships to Other Patterns

- **Chaining, Routing, Parallelization, Reflection.** Tool Use is positioned as the pattern that moves beyond purely internal orchestration; tool results can feed into a chain, inform routing decisions, or be reflected upon before producing a final answer. A single request may chain multiple tool calls (e.g., fetch a price, then calculate profit).
- **Multi-agent delegation.** Under the broader "tool calling" framing, another specialized agent can itself be a tool. A primary agent can delegate a sub-task (such as data analysis) to a dedicated agent, making Tool Use a building block for orchestrator/multi-agent systems.
- **Retrieval / knowledge grounding.** Querying an external knowledge base or a Vertex AI Search datastore through its API is a form of tool use that grounds responses in private or up-to-date sources, complete with source attributions.
- **Sessions / memory.** The ADK examples rely on a session service and runner to manage conversation context across tool-using interactions (covered more fully in the chapter on sessions and memory).

## Key Takeaways

- Tool Use (Function Calling) allows agents to interact with external systems and access dynamic information.
- It involves defining tools with clear descriptions and parameters that the LLM can understand.
- The LLM decides when to use a tool and generates structured function calls; it does not execute the tool itself.
- Agentic frameworks execute the actual tool calls and return the results to the LLM.
- Tool Use is essential for building agents that can perform real-world actions and provide up-to-date information.
- LangChain simplifies tool definition (e.g., a decorator that converts a function into a tool) and provides higher-level agent and executor constructs for building tool-using agents.
- Google ADK offers a number of useful pre-built tools, including Google Search, Code Execution, and a Vertex AI Search tool.
- Managed Vertex AI extensions execute automatically, while plain function calls must be executed manually by the client.

## References

1. LangChain Documentation (Tools): https://python.langchain.com/docs/integrations/tools/
2. Google Agent Developer Kit (ADK) Documentation (Tools): https://google.github.io/adk-docs/tools/
3. OpenAI Function Calling Documentation: https://platform.openai.com/docs/guides/function-calling
4. CrewAI Documentation (Tools): https://docs.crewai.com/concepts/tools
