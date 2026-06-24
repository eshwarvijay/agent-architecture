# Agentic Frameworks Overview

> A tour of the major frameworks for building LLM-powered agents, arranged from low-level building blocks to high-level multi-agent orchestration platforms, so you can match a framework's level of abstraction to what your application actually needs.

## Overview

The landscape of agentic frameworks offers a diverse spectrum of tools, ranging from low-level libraries for defining an individual agent's logic to high-level platforms for orchestrating multi-agent collaboration. At the foundational level, LangChain enables simple, linear workflows, while LangGraph introduces stateful, cyclical graphs for more complex reasoning. Higher-level frameworks such as CrewAI and Google's ADK shift the focus to orchestrating teams of agents with predefined roles, while others like LlamaIndex specialize in data-intensive applications.

This variety presents developers with a core trade-off: the granular control of graph-based systems versus the streamlined development of more opinionated platforms. Choosing the right framework therefore hinges on whether the application requires a simple sequence, a dynamic reasoning loop, or a managed team of specialists. The intent of this appendix is to help you pick the precise level of abstraction your project demands.

## Frameworks

### LangChain

LangChain is a framework for developing applications powered by large language models. Its core strength lies in the LangChain Expression Language (LCEL), which lets you "pipe" components together into a chain. This creates a clear, linear sequence in which the output of one step becomes the input for the next. It is built for workflows that are Directed Acyclic Graphs (DAGs) — meaning the process flows in one direction without loops.

Conceptually, an LCEL chain wires a prompt into a model and then into an output parser, so a request flows straight through those stages and produces a result without looping back.

LangChain operates at the most foundational level of the frameworks discussed here, offering the components and standardized interfaces needed to create sequences of operations, such as calling a model and parsing its output.

**Typical use:**
- **Simple RAG:** retrieve a document, build a prompt from it, and get an answer from an LLM.
- **Summarization:** take user text, feed it to a summarization prompt, and return the result.
- **Extraction:** pull structured data (such as JSON) out of a block of text.

### LangGraph

LangGraph is a library built on top of LangChain to handle more advanced agentic systems. It lets you define your workflow as a graph composed of nodes (functions or LCEL chains) and edges (conditional logic). Its main advantage is the ability to create cycles, allowing the application to loop, retry, or call tools in a flexible order until a task is complete. It explicitly manages the application state, which is passed between nodes and updated throughout the process.

Compared with LangChain, LangGraph extends the foundation with a more flexible and powerful control flow by treating an agent's workflow as a stateful graph. A developer explicitly defines nodes (functions or tools) and edges (which dictate the path of execution). This graph structure allows for complex, cyclical reasoning where the system can loop, retry tasks, and make decisions based on an explicitly managed state object that is passed between nodes. It gives the developer fine-grained control over a single agent's thought process, or the ability to construct a multi-agent system from first principles.

As an illustration, a LangGraph workflow can be wired to run in parallel: from a single start point, three separate nodes each make an independent LLM call — one to write a joke, one a story, and one a poem about a given topic — and all three feed into an aggregator node that combines them into one formatted output before the graph ends. This shows how nodes, edges, and shared state coordinate concurrent work and then merge the results.

**Typical use:**
- **Multi-agent systems:** a supervisor agent routes tasks to specialized worker agents, potentially looping until the goal is met.
- **Plan-and-execute agents:** an agent creates a plan, executes a step, and then loops back to update the plan based on the result.
- **Human-in-the-loop:** the graph can pause and wait for human input before deciding which node to go to next.

#### LangChain vs. LangGraph

| Aspect | LangChain | LangGraph |
| --- | --- | --- |
| Core abstraction | Chain (using LCEL) | Graph of nodes |
| Workflow type | Linear (Directed Acyclic Graph) | Cyclical (graphs with loops) |
| State management | Generally stateless per run | Explicit and persistent state object |
| Primary use | Simple, predictable sequences | Complex, dynamic, stateful agents |

**Which one should you use?**
- Choose **LangChain** when your application has a clear, predictable, linear flow of steps. If you can define the process from A to B to C without needing to loop back, LangChain with LCEL is the right tool.
- Choose **LangGraph** when you need your application to reason, plan, or operate in a loop. If your agent must use tools, reflect on the results, and potentially try again with a different approach, you need LangGraph's cyclical and stateful nature.

### Google's ADK

Google's Agent Development Kit (ADK) provides a high-level, structured framework for building and deploying applications composed of multiple, interacting AI agents. It contrasts with LangChain and LangGraph by offering a more opinionated and production-oriented system for orchestrating agent collaboration, rather than providing the fundamental building blocks for an agent's internal logic.

ADK abstracts away much of the low-level graph construction. Instead of asking the developer to define every node and edge, it provides pre-built architectural patterns for multi-agent interaction. For example, it includes built-in agent types such as `SequentialAgent` and `ParallelAgent` that manage the flow of control between agents automatically. The framework is architected around the concept of a "team" of agents, often with a primary agent delegating tasks to specialized sub-agents. State and session management are handled more implicitly by the framework, giving a more cohesive but less granular approach than LangGraph's explicit state passing.

The contrast is captured by an analogy: where LangGraph gives you the detailed tools to design the intricate wiring of a single robot or a team, Google's ADK gives you a factory assembly line designed to build and manage a fleet of robots that already know how to work together.

As a conceptual example, ADK can define a search-augmented agent: given a model, a name, a description, an instruction telling it to answer using web search, and the Google Search tool, the agent will not rely only on its pre-existing knowledge. Following its instructions, it uses the search tool to find relevant, real-time information from the web and then uses that information to construct its answer.

**Typical use:** production-oriented multi-agent applications where you want managed orchestration of a team of collaborating agents across the full agent lifecycle, rather than wiring control flow by hand.

### CrewAI

CrewAI offers an orchestration framework for building multi-agent systems by focusing on collaborative roles and structured processes. It operates at a higher level of abstraction than foundational toolkits, providing a conceptual model that mirrors a human team. Instead of defining the granular flow of logic as a graph, the developer defines the actors and their assignments, and CrewAI manages their interaction.

Its core components are **Agents**, **Tasks**, and the **Crew**:
- An **Agent** is defined not just by its function but by a persona — a specific role, a goal, and a backstory — which guides its behavior and communication style.
- A **Task** is a discrete unit of work with a clear description and an expected output, assigned to a specific Agent.
- The **Crew** is the cohesive unit that contains the Agents and the list of Tasks, and it executes a predefined **Process**.

The Process dictates the workflow, which is typically either **sequential** (the output of one task becomes the input for the next in line) or **hierarchical** (a manager-like agent delegates tasks to and coordinates the workflow among other agents). For example, a crew can be configured to run its agents and tasks as a sequential process, tackling a list of tasks in a specific order with detailed logging enabled to monitor progress.

Among the frameworks, CrewAI occupies a distinct position. It moves away from the low-level, explicit state management and control flow of LangGraph, where a developer wires together every node and conditional edge. Instead of building a state machine, the developer designs a "team charter." And while Google's ADK provides a comprehensive, production-oriented platform for the entire agent lifecycle, CrewAI concentrates specifically on the logic of agent collaboration and on simulating a team of specialists.

**Typical use:** modeling a collaborating team of role-playing specialists where the natural design unit is who does what, in what order, rather than explicit graph wiring.

### Microsoft AutoGen

AutoGen is a framework centered on orchestrating multiple agents that solve tasks through conversation. Its architecture enables agents with distinct capabilities to interact, allowing for complex problem decomposition and collaborative resolution. Its primary advantage is a flexible, conversation-driven approach that supports dynamic and complex multi-agent interactions. The trade-off is that this conversational paradigm can lead to less predictable execution paths and may require sophisticated prompt engineering to ensure tasks converge efficiently.

### LlamaIndex

LlamaIndex is fundamentally a data framework designed to connect large language models with external and private data sources. It excels at creating sophisticated data ingestion and retrieval pipelines, which are essential for building knowledgeable agents that can perform RAG. While its data indexing and querying capabilities are exceptionally powerful for creating context-aware agents, its native tools for complex agentic control flow and multi-agent orchestration are less developed than those of agent-first frameworks. LlamaIndex is optimal when the core technical challenge is data retrieval and synthesis.

### Haystack

Haystack is an open-source framework engineered for building scalable, production-ready search systems powered by language models. Its architecture is composed of modular, interoperable nodes that form pipelines for document retrieval, question answering, and summarization. Its main strength is its focus on performance and scalability for large-scale information-retrieval tasks, making it suitable for enterprise-grade applications. A potential trade-off is that its design, optimized for search pipelines, can be more rigid for implementing highly dynamic and creative agentic behaviors.

### MetaGPT

MetaGPT implements a multi-agent system by assigning roles and tasks based on a predefined set of Standard Operating Procedures (SOPs). It structures agent collaboration to mimic a software development company, with agents taking on roles like product managers or engineers to complete complex tasks. This SOP-driven approach results in highly structured and coherent outputs, a significant advantage for specialized domains like code generation. Its primary limitation is its high degree of specialization, which makes it less adaptable for general-purpose agentic tasks outside its core design.

### SuperAGI

SuperAGI is an open-source framework designed to provide complete lifecycle management for autonomous agents. It includes features for agent provisioning, monitoring, and a graphical interface, aiming to enhance the reliability of agent execution. Its key benefit is a focus on production-readiness, with built-in mechanisms to handle common failure modes such as looping and to provide observability into agent performance. A potential drawback is that its comprehensive platform approach can introduce more complexity and overhead than a more lightweight, library-based framework.

### Semantic Kernel

Developed by Microsoft, Semantic Kernel is an SDK that integrates large language models with conventional programming code through a system of "plugins" and "planners." It allows an LLM to invoke native functions and orchestrate workflows, effectively treating the model as a reasoning engine within a larger software application. Its primary strength is seamless integration with existing enterprise codebases, particularly in .NET and Python environments. The conceptual overhead of its plugin-and-planner architecture can present a steeper learning curve than more straightforward agent frameworks.

### Strands Agents

Strands Agents is an AWS lightweight and flexible SDK that uses a model-driven approach for building and running AI agents. It is designed to be simple and scalable, supporting everything from basic conversational assistants to complex multi-agent autonomous systems. The framework is model-agnostic, offering broad support for various LLM providers, and includes native integration with the Model Context Protocol (MCP) for easy access to external tools. Its core advantage is simplicity and flexibility, with a customizable agent loop that is easy to get started with. A potential trade-off is that its lightweight design means developers may need to build out more of the surrounding operational infrastructure — such as advanced monitoring or lifecycle management — that more comprehensive frameworks might provide out of the box.

## Choosing a Framework

The frameworks span a spectrum from low-level libraries that define agent logic to high-level platforms that orchestrate multi-agent collaboration. The central decision is a trade-off between the granular control of graph-based systems and the streamlined development of more opinionated platforms. Use these reference points:

- **Need a simple, predictable sequence?** Reach for a foundational, linear tool like LangChain (with LCEL).
- **Need a dynamic reasoning loop** — tool use, reflection, retries, human-in-the-loop? Use a stateful, cyclical graph framework like LangGraph.
- **Need a managed team of specialists?** Use a higher-level orchestration framework such as CrewAI (role/task/crew model) or Google's ADK (opinionated, production-oriented agent teams).
- **Is the core challenge data retrieval and synthesis?** Specialize with a data framework like LlamaIndex, or for large-scale, production search systems, Haystack.
- **Other fits:** conversation-driven multi-agent problem solving (AutoGen); SOP-driven, software-company-style collaboration for domains like code generation (MetaGPT); full autonomous-agent lifecycle management and observability (SuperAGI); deep integration with existing enterprise (.NET/Python) codebases via plugins and planners (Semantic Kernel); a lightweight, model-agnostic SDK with native MCP support (Strands Agents).

In short, selecting the right framework hinges on whether the application requires a simple sequence, a dynamic reasoning loop, or a managed team of specialists — and on choosing the precise level of abstraction the project demands.

## Key Takeaways

- Agentic frameworks form a spectrum from low-level logic libraries to high-level multi-agent orchestration platforms.
- **LangChain** is the most foundational: linear (DAG) workflows via LCEL chains, generally stateless per run; best for simple, predictable sequences.
- **LangGraph** builds on LangChain to add stateful, cyclical graphs of nodes and edges; best for complex, dynamic agents that loop, retry, and reflect.
- **Google's ADK** is opinionated and production-oriented, providing pre-built multi-agent patterns (e.g., `SequentialAgent`, `ParallelAgent`) and implicit state/session management — a "factory" for fleets of collaborating agents.
- **CrewAI** models a human team through Agents (role/goal/backstory), Tasks, and a Crew running a sequential or hierarchical Process; you design a team charter rather than a state machine.
- **AutoGen** orchestrates agents via conversation; **LlamaIndex** specializes in data ingestion/retrieval for RAG; **Haystack** targets scalable production search; **MetaGPT** structures agents around SOPs for domains like code generation; **SuperAGI** focuses on autonomous-agent lifecycle management; **Semantic Kernel** integrates LLMs into enterprise code via plugins and planners; **Strands Agents** is a lightweight, model-agnostic AWS SDK with native MCP support.
- The recurring trade-off is granular control (graph-based) versus streamlined, opinionated development; match the abstraction level to the task.

## References

1. LangChain — https://www.langchain.com/
2. LangGraph — https://www.langchain.com/langgraph
3. Google's ADK — https://google.github.io/adk-docs/
4. CrewAI — https://docs.crewai.com/en/introduction
