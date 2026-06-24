# Routing

> Routing introduces conditional logic into an agent's operational framework, letting the agent dynamically evaluate criteria and direct the flow of control to one of several specialized functions, tools, or sub-processes rather than following a single fixed path.

## Overview

Sequential processing via prompt chaining is a foundational technique for executing deterministic, linear workflows with language models, but its applicability is limited in scenarios that require adaptive responses. Real-world agentic systems must often arbitrate between multiple potential actions based on contingent factors such as the state of the environment, user input, or the outcome of a preceding operation. This capacity for dynamic decision-making — which governs the flow of control to different specialized functions, tools, or sub-processes — is achieved through a mechanism known as routing.

Routing introduces conditional logic into an agent's operational framework, enabling a shift from a fixed execution path to a model where the agent dynamically evaluates specific criteria to select from a set of possible subsequent actions. This allows for more flexible and context-aware system behavior.

As a concrete example, an agent designed for customer inquiries, when equipped with a routing function, can first classify an incoming query to determine the user's intent. Based on this classification, it can then direct the query to a specialized agent for direct question-answering, a database retrieval tool for account information, or an escalation procedure for complex issues — rather than defaulting to a single, predetermined response pathway.

A more sophisticated agent using routing could:
1. Analyze the user's query.
2. Route the query based on its intent:
   - If the intent is "check order status," route to a sub-agent or tool chain that interacts with the order database.
   - If the intent is "product information," route to a sub-agent or chain that searches the product catalog.
   - If the intent is "technical support," route to a different chain that accesses troubleshooting guides or escalates to a human.
   - If the intent is unclear, route to a clarification sub-agent or prompt chain.

The implementation of routing enables a system to move beyond deterministic sequential processing. It facilitates the development of more adaptive execution flows that can respond dynamically and appropriately to a wider range of inputs and state changes — transforming an agent from a static executor of predefined sequences into a dynamic system that can make decisions about the most effective method for accomplishing a task under changing conditions.

## How It Works

The core component of the routing pattern is a mechanism that performs the evaluation and directs the flow. This mechanism can be implemented in several ways:

- **LLM-based routing.** The language model itself is prompted to analyze the input and output a specific identifier or instruction that indicates the next step or destination. For example, a prompt might ask the LLM to "Analyze the following user query and output only the category: 'Order Status', 'Product Info', 'Technical Support', or 'Other'." The agentic system then reads this output and directs the workflow accordingly. This approach is flexible and handles nuanced or novel inputs well, since the decision is made by a generative model at inference time.

- **Embedding-based routing.** The input query is converted into a vector embedding (related to Retrieval-Augmented Generation, covered in Chapter 14). This embedding is compared to embeddings that represent different routes or capabilities, and the query is routed to the route whose embedding is most similar. This is useful for semantic routing, where the decision is based on the *meaning* of the input rather than just keywords.

- **Rule-based routing.** Predefined rules or logic (e.g., if-else statements, switch cases) operate on keywords, patterns, or structured data extracted from the input. This can be faster and more deterministic than LLM-based routing, but is less flexible for handling nuanced or novel inputs.

- **Machine learning model-based routing.** This employs a discriminative model, such as a classifier, that has been specifically trained on a small corpus of labeled data to perform the routing task. While conceptually similar to embedding-based methods, its key distinguishing characteristic is the *supervised fine-tuning* process, which adjusts the model's parameters to create a specialized routing function. It is distinct from LLM-based routing because the decision-making component is not a generative model executing a prompt at inference time; instead, the routing logic is encoded within the fine-tuned model's learned weights. LLMs may be used in a pre-processing step to generate synthetic data for augmenting the training set, but they are not involved in the real-time routing decision itself.

Routing mechanisms can be implemented at multiple junctures within an agent's operational cycle. They can be applied at the outset to classify a primary task, at intermediate points within a processing chain to determine a subsequent action, or during a subroutine to select the most appropriate tool from a given set.

Computational frameworks such as LangChain, LangGraph, and Google's Agent Developer Kit (ADK) provide explicit constructs for defining and managing this conditional logic. With its state-based graph architecture, LangGraph is particularly well-suited for complex routing scenarios where decisions are contingent upon the accumulated state of the entire system. Google's ADK provides foundational components for structuring an agent's capabilities and interaction models, which serve as the basis for implementing routing logic. Within these execution environments, developers define the possible operational paths and the functions or model-based evaluations that dictate the transitions between nodes in the computational graph.

### Conceptual walk-through: the LangChain example

The chapter's first hands-on example builds a simple agent-like "coordinator" system using LangChain together with Google's Generative AI model (Gemini 2.5 Flash). It routes user requests to different *simulated* sub-agent handlers based on the request's intent — booking, information, or unclear — demonstrating a basic delegation pattern of the kind often seen in multi-agent architectures.

The example defines three simulated sub-agent handlers, one for each intent category: a booking handler, an info handler, and an unclear/fallback handler. Each handler simulates processing its specific type of request (the booking handler simulates a booking action, the info handler simulates information retrieval, and the unclear handler returns a message asking the user to clarify).

A core component is a "coordinator router chain." It uses a chat prompt template to instruct the language model to categorize each incoming request into exactly one of three labels — `booker`, `info`, or `unclear` — and to output only that single word. The prompt's rules state: requests about booking flights or hotels yield `booker`; all other general information questions yield `info`; and unclear or non-fitting requests yield `unclear`.

The output of this router chain (the "decision") then drives a branching construct (LangChain's `RunnableBranch`) that delegates the *original* request to the corresponding handler function. The branch checks the decision string — routing to the booking handler when it equals `booker`, to the info handler when it equals `info`, and otherwise falling through to the unclear handler as the default branch. (The example trims whitespace from the decision string to make the matching robust.)

The full coordinator agent combines these pieces: it first runs the router chain to obtain a decision while carrying the original request along, passes both into the delegation branch, and finally extracts the chosen handler's response as the output. The demonstration runs three example requests — a booking request ("Book me a flight to London"), an information request ("What is the capital of Italy?"), and an unclear request ("Tell me about quantum physics") — to show how different inputs are routed and processed by the appropriate simulated agent. Error handling around language-model initialization is included for robustness. Conceptually, the structure mimics a basic multi-agent framework in which a central coordinator delegates tasks to specialized agents based on intent.

### Conceptual walk-through: the Google ADK example

The chapter's second hands-on example accomplishes the same coordinator/sub-agent routing using Google's Agent Development Kit (ADK). The ADK is a framework for engineering agentic systems that provides a structured environment for defining an agent's capabilities and behaviors. In contrast to architectures based on explicit computational graphs (like LangGraph), routing within the ADK paradigm is typically implemented by defining a discrete set of "tools" that represent the agent's functions. The framework's internal logic — leveraging an underlying model — selects the appropriate tool in response to a user query by matching user intent to the correct functional handler.

The example defines tool functions that simulate the specialist actions: a booking handler that simulates handling flight and hotel bookings, an info handler that simulates retrieving general information, and an unclear handler included as a fallback (though the example's coordinator logic does not explicitly invoke the unclear handler for delegation failures in its main execution path). The booking and info functions are wrapped as ADK function tools.

Two specialized sub-agents are defined, each equipped with its respective tool: a "Booker" agent that handles flight and hotel booking requests by calling the booking tool, and an "Info" agent that provides general information by calling the info tool. A parent "Coordinator" agent is then defined with an explicit instruction telling it that its only task is to analyze incoming user requests and delegate them to the appropriate specialist — booking-related requests go to the Booker agent, all other general information questions go to the Info agent — and explicitly not to answer the user directly.

A key mechanism the example highlights is ADK's *Auto-Flow*: because the Coordinator agent has sub-agents defined, the framework automatically enables LLM-driven delegation by default. The execution logic uses an in-memory runner that creates a user and session, sends the request through the coordinator, and processes the resulting stream of events, extracting the final response text from the event content. The demonstration runs several requests (booking a hotel in Paris, asking the highest mountain in the world, asking for a random fact, and finding flights to Tokyo) to show how booking requests are delegated to the Booker and information requests to the Info agent.

The two examples illustrate two different but effective approaches: LangGraph's graph-based structure provides a visual and explicit way to define states and transitions (ideal for complex, multi-step workflows with intricate routing logic), while Google ADK focuses on defining distinct capabilities (tools) and relies on the framework to route user requests to the appropriate tool handler (often simpler for agents with a well-defined set of discrete actions).

## Practical Applications & Use Cases

Routing is a critical control mechanism in the design of adaptive agentic systems, enabling them to dynamically alter their execution path in response to variable inputs and internal states. Its utility spans multiple domains by providing a necessary layer of conditional logic.

- **Human-computer interaction (virtual assistants, AI-driven tutors).** Routing interprets user intent. An initial analysis of a natural language query determines the most appropriate subsequent action — whether invoking a specific information retrieval tool, escalating to a human operator, or selecting the next module in a curriculum based on user performance. This lets the system move beyond linear dialogue flows and respond contextually.

- **Automated data and document processing pipelines.** Routing serves as a classification and distribution function. Incoming data — such as emails, support tickets, or API payloads — is analyzed based on content, metadata, or format, and the system directs each item to a corresponding workflow: for example, a sales-lead ingestion process, a specific data transformation function for JSON or CSV formats, or an urgent issue escalation path.

- **Complex multi-tool / multi-agent systems (high-level dispatcher).** A research system composed of distinct agents for searching, summarizing, and analyzing information uses a router to assign tasks to the most suitable agent based on the current objective. Similarly, an AI coding assistant uses routing to identify the programming language and the user's intent — to debug, explain, or translate — before passing a code snippet to the correct specialized tool.

Ultimately, routing provides the capacity for logical arbitration that is essential for creating functionally diverse and context-aware systems.

## Trade-offs & When to Use

Use the routing pattern when an agent must decide between multiple distinct workflows, tools, or sub-agents based on the user's input or the current state. It is essential for applications that need to triage or classify incoming requests to handle different types of tasks — such as a customer support bot distinguishing between sales inquiries, technical support, and account management questions.

A simple sequential workflow lacks the ability to make decisions based on context. Without a mechanism to choose the correct tool or sub-process for a specific task, the system remains rigid and non-adaptive, making it difficult to build sophisticated applications that can manage the complexity and variability of real-world user requests. Routing solves this by transforming a static, predetermined execution path into a flexible, context-aware workflow capable of selecting the best possible action.

Trade-offs across the routing mechanisms:
- **Rule-based routing** is faster and more deterministic, but less flexible for nuanced or novel inputs.
- **LLM-based routing** is highly flexible and handles nuance and novelty, at the cost of inference-time latency and the inherent variability of generative output.
- **Embedding-based routing** decides on semantic similarity (meaning) rather than keywords, useful when surface form varies.
- **ML model-based routing** offers a specialized, learned classifier whose logic lives in fixed weights — predictable at inference time but requiring upfront labeled training data and a fine-tuning process.

The frameworks themselves embody an architectural trade-off: LangGraph's graph structure suits complex, multi-step workflows with intricate, state-dependent routing; ADK's tool/Auto-Flow approach can be simpler for agents with a well-defined set of discrete actions.

## Relationships to Other Patterns

- **Prompt chaining (sequential processing).** Routing is presented as the adaptive counterpart to prompt chaining. Chaining executes deterministic, linear workflows; routing introduces the conditional branching that chaining lacks, and the two combine — a route can lead into a dedicated prompt chain or sub-process.
- **Multi-agent / delegation architectures.** Both code examples explicitly frame routing as the basis of a coordinator-and-sub-agents delegation pattern, where a central coordinator dispatches tasks to specialized agents.
- **Tool use.** In the ADK paradigm, routing is implemented as tool selection — the framework matches user intent to the correct functional handler (tool).
- **Retrieval-Augmented Generation (Chapter 14).** Embedding-based routing reuses the same vector-embedding machinery introduced for RAG.

## Key Takeaways

- Routing enables agents to make dynamic decisions about the next step in a workflow based on conditions.
- It allows agents to handle diverse inputs and adapt their behavior, moving beyond linear execution.
- Routing logic can be implemented using LLMs, rule-based systems, embedding similarity, or a fine-tuned ML classifier.
- Routing can be applied at multiple junctures: at the outset to classify a primary task, at intermediate points in a chain, or within a subroutine to select a tool.
- Frameworks like LangGraph and Google ADK provide structured ways to define and manage routing within agent workflows, albeit with different architectural approaches (explicit state graphs vs. tool-based Auto-Flow delegation).
- Mastering routing is essential for building agents that can intelligently navigate different scenarios and provide tailored responses or actions based on context.

## References

1. LangGraph / LangChain Documentation: https://www.langchain.com/
2. Google Agent Developer Kit (ADK) Documentation: https://google.github.io/adk-docs/
