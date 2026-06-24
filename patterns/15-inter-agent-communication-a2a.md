# Inter-Agent Communication (A2A)

> An open, HTTP-based standard (Google's Agent2Agent protocol) that lets independent AI agents — even ones built on different frameworks — discover one another, delegate tasks, and exchange information so they can collaborate as a single system.

## Overview

Individual AI agents, even capable ones, often hit limits when tackling complex, multifaceted problems on their own. Inter-Agent Communication (A2A) addresses this by enabling diverse AI agents — potentially built with different frameworks — to collaborate effectively. That collaboration involves seamless coordination, task delegation, and information exchange.

The Agent2Agent (A2A) protocol is the open standard, introduced by Google, designed to facilitate this universal communication. Its central promise is interoperability: agents developed with technologies such as LangGraph, CrewAI, or Google's Agent Development Kit (ADK) can work together regardless of their origin or framework differences. The primary challenge it solves is the absence of a common language or protocol; without a standardized approach, integrating disparate agents is costly and time-consuming, and agents remain isolated, unable to combine their specialized skills into larger solutions.

A2A is backed by a broad set of technology companies and service providers, including Atlassian, Box, LangChain, MongoDB, Salesforce, SAP, and ServiceNow. Microsoft plans to integrate A2A into Azure AI Foundry and Copilot Studio, and Auth0 and SAP are integrating A2A support into their platforms and agents. As an open-source protocol, A2A welcomes community contributions to support its evolution and adoption.

The protocol is built on several foundational pillars: Core Actors, the Agent Card, Agent Discovery, Communication and Tasks, Interaction Mechanisms, and Security. A thorough grasp of these is essential for anyone developing or integrating with A2A-compliant systems.

## How It Works

### Core actors

A2A involves three main entities:

- **User** — initiates the request for agent assistance.
- **A2A Client (Client Agent)** — an application or AI agent that acts on the user's behalf to request actions or information.
- **A2A Server (Remote Agent)** — an AI agent or system that exposes an HTTP endpoint to process client requests and return results. Crucially, the remote agent operates as an "opaque" system: the client does not need to understand its internal operational details. This opacity is what makes cross-framework collaboration possible — the client only needs the contract, not the implementation.

### The Agent Card

An agent's digital identity is defined by its **Agent Card**, usually a JSON file. The card contains the key information a client needs to interact with the agent and to discover it automatically:

- The agent's identity (name, description), its endpoint URL, and its version.
- The capabilities it supports — for example, whether it can stream results, send push notifications, or maintain state-transition history.
- Its specific **skills**, each described with an identifier, a human-readable name and description, the input and output modes it accepts, illustrative example prompts, and tags for categorization.
- Its default input and output modes (for example, text).
- Its authentication requirements (for example, an API-key scheme).

As an illustration, the chapter describes an Agent Card for a "WeatherBot." Its card names the bot and describes it as providing accurate weather forecasts and historical data, gives the service URL of its A2A endpoint and a version number, and declares its capabilities — streaming enabled, push notifications disabled, state-transition history enabled. It declares an API-key authentication scheme and text as the default input and output mode. It then lists two skills: one to "Get Current Weather" (retrieve real-time conditions for any location, with example queries like asking the weather in Paris or current conditions in Tokyo, tagged as weather/current/real-time) and one to "Get Forecast" (five-day predictions, with examples like a five-day forecast for New York or whether it will rain in London this weekend, tagged weather/forecast/prediction). Each skill specifies text as its input and output mode.

### Agent discovery

Discovery is the process by which clients find Agent Cards describing the capabilities of available A2A Servers. The chapter lays out three strategies:

- **Well-Known URI** — an agent hosts its Agent Card at a standardized path (for example, a path under `/.well-known/`). This offers broad, often automated accessibility, suited to public or domain-specific use.
- **Curated Registries** — a centralized catalog where Agent Cards are published and can be queried against specific criteria. This fits enterprise environments that need centralized management and access control.
- **Direct Configuration** — Agent Card information is embedded or privately shared. Appropriate for closely coupled or private systems where dynamic discovery is not crucial.

Whichever method is chosen, the Agent Card endpoint should be secured — through access control, mutual TLS, or network restrictions — especially when the card contains sensitive (though non-secret) information.

### Communication and tasks

In A2A, communication is structured around asynchronous **tasks**, the fundamental units of work for long-running processes. Each task is assigned a unique identifier and moves through a series of states — for example, *submitted*, *working*, *completed* (and *failed*). This state-machine design supports parallel processing in complex operations. The protocol also supports multi-turn conversations through an *input-required* state, which lets an agent pause to request additional information from the client and maintain context across the exchange.

Communication between agents occurs through a **Message**. A message carries:

- **Attributes** — key-value metadata describing the message (such as its priority or creation time).
- One or more **parts** — the actual content being delivered, which can be plain text, files, or structured JSON data.

The tangible outputs an agent produces during a task are called **artifacts**. Like messages, artifacts are composed of one or more parts and can be streamed incrementally as results become available.

All A2A communication is conducted over HTTP(S) using the JSON-RPC 2.0 protocol for payloads. To maintain continuity across multiple interactions, a server-generated **context identifier** is used to group related tasks and preserve context.

### Interaction mechanisms

A2A offers multiple interaction methods so that different application needs can each use the most appropriate mechanism:

- **Synchronous Request/Response** — for quick, immediate operations. The client sends a request and actively waits for the server to process it and return a complete response in a single synchronous exchange.
- **Asynchronous Polling** — for tasks that take longer. The client sends a request; the server immediately acknowledges it with a "working" status and a task ID. The client is then free to do other work and periodically polls the server with new requests to check the task's status until it is marked "completed" or "failed."
- **Streaming Updates (Server-Sent Events, SSE)** — for real-time, incremental results. This establishes a persistent, one-way connection from server to client, letting the remote agent continuously push updates (status changes, partial results) without the client making repeated requests.
- **Push Notifications (Webhooks)** — for very long-running or resource-intensive tasks where holding a constant connection or polling frequently is inefficient. The client registers a webhook URL, and the server sends an asynchronous notification (a "push") to that URL when the task's status changes significantly, such as on completion.

Whether an agent supports streaming or push notifications is declared in its Agent Card. A2A is also **modality-agnostic**: these interaction patterns apply not only to text but to other data types such as audio and video, enabling rich, multimodal applications.

The chapter contrasts two request examples in prose. A *synchronous request* invokes a "send task" method, supplying a task ID, a session ID, a user message whose part is the text question (for example, asking for the USD-to-EUR exchange rate), the accepted output modes (plain text), and a desired history length; the client expects a single, complete answer. A *streaming request* instead invokes a "send task and subscribe" method with a similar structure (for example, asking the JPY-to-GBP rate today). The subscribe variant establishes a persistent connection so the agent can send back multiple incremental updates or partial results over time. (The chapter notes the same operations elsewhere by the names `tasks/send` for the synchronous case and `tasks/sendSubscribe` for the streaming case.)

### Security

A2A treats secure, seamless data exchange among agents as a core architectural concern, with several built-in mechanisms ensuring robustness and integrity:

- **Mutual Transport Layer Security (mTLS)** — establishes encrypted, mutually authenticated connections to prevent unauthorized access and data interception.
- **Comprehensive Audit Logs** — all inter-agent communications are recorded in detail (information flow, agents involved, actions taken), providing an audit trail essential for accountability, troubleshooting, and security analysis.
- **Agent Card Declaration** — authentication requirements are declared explicitly in the Agent Card, which centralizes and simplifies authentication management alongside the agent's identity, capabilities, and security policies.
- **Credential Handling** — agents typically authenticate using secure credentials such as OAuth 2.0 tokens or API keys, passed via HTTP headers rather than in URLs or message bodies, which prevents credential exposure.

### Building an A2A agent (conceptual sketch)

The chapter's hands-on example, drawn from Google's A2A sample repository, sets up an A2A-compliant "Calendar Agent" backed by an ADK agent that uses Google-authenticated calendar tools. Conceptually, the build proceeds in stages: construct an ADK language-model agent configured with a model, a name, instructions for managing a user's calendar (including injecting the current date for temporal context), and a calendar toolset created from client credentials so it can reach the Google Calendar API. The agent's capabilities — such as a "check availability" skill (checking whether a user is free during a given time, with an example like "Am I free from 10am to 11am tomorrow?") — are declared in an Agent Card that also specifies the agent's network address and that it supports streaming. The agent is then wrapped with in-memory services for artifacts, sessions, and memory, fronted by an A2A protocol request handler with a task store, and exposed as a web service (with an added authentication-callback route) so it is reachable over HTTP. The takeaway is the workflow itself: define capabilities in an Agent Card, back them with an agent and its tools, and run it as a discoverable A2A web service — yielding an interoperable agent that can join a multi-agent ecosystem.

## Practical Applications & Use Cases

A2A is indispensable for building sophisticated AI solutions across domains, enabling modularity, scalability, and enhanced intelligence:

- **Multi-Framework Collaboration** — A2A's primary use case: letting independent agents collaborate regardless of their underlying frameworks (ADK, LangChain, CrewAI, and others). This is fundamental for complex multi-agent systems where different agents specialize in different aspects of a problem.
- **Automated Workflow Orchestration** — in enterprise settings, agents delegate and coordinate tasks across a workflow. For example, one agent handles initial data collection, delegates to a second for analysis, and then to a third for report generation, all communicating via A2A.
- **Dynamic Information Retrieval** — agents communicate to retrieve and exchange real-time information. A primary agent might request live market data from a specialized "data-fetching agent," which calls external APIs to gather it and returns the result.

The chapter also points to Google's A2A sample repository (with examples in Java, Go, and Python showing frameworks such as LangGraph, CrewAI, Azure AI Foundry, and AG2 communicating via A2A, released under Apache 2.0) and to a Trickle.so walkthrough offering sample A2A clients and servers in Python and JavaScript, multi-agent web applications, command-line interfaces, and example implementations for various frameworks.

## Trade-offs & When to Use

A2A's stated goals are to enhance efficiency, reduce integration costs, and foster innovation and interoperability when building complex, multi-agent AI systems. It encourages a modular architecture where specialized agents operate independently (for example, on different ports), which enables system scalability and distribution. Its flexible interaction patterns — synchronous request/response, asynchronous polling, streaming, and push notifications — let a single standard serve everything from instant lookups to very long-running jobs and multimodal exchanges.

**Rule of thumb.** Use A2A when you need to orchestrate collaboration between two or more AI agents, especially if they are built using different frameworks (for example, Google ADK, LangGraph, CrewAI). It is ideal for complex, modular applications where specialized agents handle distinct parts of a workflow — such as delegating data analysis to one agent and report generation to another — and is essential when an agent must dynamically discover and consume the capabilities of other agents to complete a task. For interactions confined to a single agent reaching its own tools and data, A2A is unnecessary (that is the role of MCP; see below).

## Relationships to Other Patterns

- **Model Context Protocol (MCP)** — A2A complements Anthropic's MCP rather than competing with it. MCP focuses on structuring context for an agent and governing its interaction with external data and tools (a standardized interface for an LLM to reach external resources). A2A focuses on coordination and communication *among agents*, enabling task delegation and collaboration. Put differently, A2A is a high-level protocol for managing tasks and workflows *between* different agents, while MCP provides a standardized interface for an LLM to interface with external resources. The two operate at different layers and are designed to work together.
- **Multi-Agent Systems** — A2A is the communication substrate that makes multi-agent collaboration practical across heterogeneous frameworks. It turns isolated specialist agents into a composable, distributed system in which work is delegated and coordinated.
- **Tool Use** — within an individual A2A agent, the agent still uses tools (often via MCP) to do its actual work; A2A governs how the resulting capabilities are exposed to and invoked by *other* agents, not how a single agent calls its own functions.
- **Observability / monitoring** — tools such as Trickle AI help visualize and track A2A communications, aiding developers in monitoring, debugging, and optimizing multi-agent systems.

## Key Takeaways

- The Google A2A protocol is an open, HTTP-based standard for communication and collaboration between AI agents built with different frameworks.
- An Agent Card is an agent's digital identity (typically a JSON file) describing its identity, endpoint, version, capabilities, skills, input/output modes, and authentication requirements — enabling automatic discovery and understanding by other agents.
- Agents are discovered via a well-known URI, a curated registry, or direct configuration; the card endpoint should be secured.
- Communication is organized around asynchronous tasks with unique IDs that progress through states (submitted, working, completed/failed) and support parallel processing; an input-required state supports multi-turn conversation and context retention.
- Messages carry metadata attributes plus one or more parts (text, files, structured data); agent outputs are artifacts, also made of parts and streamable incrementally. All traffic is HTTP(S) with JSON-RPC 2.0 payloads, grouped by a server-generated context identifier.
- A2A supports synchronous request/response, asynchronous polling, SSE streaming, and webhook push notifications, and is modality-agnostic (text, audio, video). The chapter pairs the synchronous and streaming requests with the `tasks/send` and `tasks/sendSubscribe` operations.
- Security is built in: mutual TLS, comprehensive audit logs, authentication declared in the Agent Card, and credentials passed in HTTP headers.
- A2A and MCP are complementary: A2A handles high-level coordination and task delegation between agents; MCP standardizes how an individual LLM/agent interfaces with external resources.
- The pattern encourages modular, independently deployable specialist agents, enabling scalable and distributed multi-agent systems, with broad industry backing accelerating its adoption.

## References

1. Chen, B. (2025, April 22). How to Build Your First Google A2A Project: A Step-by-Step Tutorial. Trickle.so Blog. https://www.trickle.so/blog/how-to-build-google-a2a-project
2. Google A2A GitHub Repository. https://github.com/google-a2a/A2A
3. Google Agent Development Kit (ADK). https://google.github.io/adk-docs/
4. Getting Started with Agent-to-Agent (A2A) Protocol. https://codelabs.developers.google.com/intro-a2a-purchasing-concierge#0
5. A2A Protocol (Agent Discovery). https://a2a-protocol.org/latest/
6. Designing Collaborative Multi-Agent Systems with the A2A Protocol. https://www.oreilly.com/radar/designing-collaborative-multi-agent-systems-with-the-a2a-protocol/
