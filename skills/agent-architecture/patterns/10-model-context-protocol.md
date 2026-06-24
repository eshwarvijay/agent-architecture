# Model Context Protocol (MCP)

> An open, standardized client-server protocol that defines how LLMs and agents discover, communicate with, and use external tools, data, and prompt templates, so any compliant tool can be accessed by any compliant LLM.

## Overview

For an LLM to act as an effective agent, its capabilities must extend beyond generating text (including multimodal generation). It needs to interact with the external environment: access current data, use external software, and execute specific operational tasks. The Model Context Protocol (MCP) addresses this by providing a standardized interface for LLMs to connect to external resources, serving as the mechanism that makes that integration consistent and predictable.

The core idea is a universal adapter. MCP lets any LLM plug into any external system, database, or tool without writing a bespoke integration for each one. It is an open standard that standardizes how models such as Gemini, OpenAI's GPT models, Mixtral, and Claude communicate with external applications, data sources, and tools. Think of it as a universal connection mechanism that simplifies how LLMs obtain context, execute actions, and interact with various systems.

MCP operates on a client-server architecture. It defines how three kinds of elements are exposed by an MCP server and consumed by an MCP client:

- **Resources** — data (for example, a PDF file or a database record).
- **Prompts** — interactive templates that guide how the LLM interacts with a resource or tool.
- **Tools** — actionable functions that perform an action (for example, sending an email or querying an API).

The client can be an LLM host application or an AI agent itself. By standardizing this interface, MCP dramatically reduces the complexity of integrating LLMs into diverse operational environments and fosters interoperability, composability, and reusability across different systems and implementations.

A critical caveat: MCP is a contract for an "agentic interface," and its effectiveness depends heavily on the design of the underlying APIs it exposes. There is a real risk that developers simply wrap pre-existing, legacy APIs without modification, which can be suboptimal for an agent. For example, if a ticketing system's API only allows retrieving full ticket details one at a time, an agent asked to summarize high-priority tickets will be slow and inaccurate at high volume. To be truly effective, the underlying API should be improved with deterministic features such as filtering and sorting to help the non-deterministic agent work efficiently. The broader lesson: agents do not magically replace deterministic workflows; they often require stronger deterministic support to succeed.

A second caveat concerns data format. MCP can wrap an API whose input or output is still not inherently understandable by the agent, and MCP itself does not guarantee an agent-friendly format. For instance, an MCP server for a document store that returns files as PDFs is mostly useless if the consuming agent cannot parse PDF content; a better approach is an API that returns a textual version of the document, such as Markdown, that the agent can actually read and process. Developers must consider not just the connection but the nature of the data being exchanged to ensure true compatibility.

## How It Works

MCP uses a client-server model to standardize information flow. Four components participate (the fourth is optional):

1. **Large Language Model (LLM)** — the core intelligence. It processes user requests, formulates plans, and decides when it needs to access external information or perform an action.
2. **MCP Client** — an application or wrapper around the LLM that acts as the intermediary. It translates the LLM's intent into a formal request conforming to the MCP standard, and it is responsible for discovering, connecting to, and communicating with MCP Servers.
3. **MCP Server** — the gateway to the external world. It exposes a set of tools, resources, and prompts to any authorized MCP Client. Each server is typically responsible for a specific domain, such as a connection to a company's internal database, an email service, or a public API.
4. **Optional Third-Party (3P) Service** — the actual external tool, application, or data source that the MCP Server manages and exposes. It is the ultimate endpoint that performs the requested action, such as querying a proprietary database, interacting with a SaaS platform, or calling a public weather API.

The interaction flows through five steps:

1. **Discovery** — The MCP Client, on behalf of the LLM, queries an MCP Server to ask what capabilities it offers. The server responds with a manifest listing its available tools (e.g., a `send_email` tool), resources (e.g., a `customer_database` resource), and prompts.
2. **Request Formulation** — The LLM decides it needs one of the discovered tools (for example, to send an email) and formulates a request specifying the tool to use and the necessary parameters (such as recipient, subject, body).
3. **Client Communication** — The MCP Client takes the LLM's formulated request and sends it as a standardized call to the appropriate MCP Server.
4. **Server Execution** — The MCP Server receives the request, authenticates the client, validates the request, and then executes the specified action by interfacing with the underlying software (for example, calling the send function of an email API).
5. **Response and Context Update** — After execution, the MCP Server sends a standardized response back to the MCP Client, indicating whether the action succeeded and including any relevant output (such as a confirmation ID). The client passes this result back to the LLM, updating its context and enabling it to proceed with the next step of its task.

### Discoverability

A key advantage of MCP is that an MCP client can dynamically query a server to learn what tools and resources it offers. This "just-in-time" discovery mechanism is powerful for agents that need to adapt to new capabilities without being redeployed.

### Transport mechanisms

The protocol also defines the underlying transport layers for communication:

- **Local interactions** use JSON-RPC over STDIO (standard input/output) for efficient inter-process communication.
- **Remote connections** leverage web-friendly protocols like Streamable HTTP and Server-Sent Events (SSE) to enable persistent and efficient client-server communication.

### Deployment dimensions

- **Local vs. Remote Server** — MCP servers can be deployed locally on the same machine as the agent or remotely on a different server. A local server might be chosen for speed and security with sensitive data, while a remote server architecture allows shared, scalable access to common tools across an organization.
- **On-demand vs. Batch** — MCP supports both on-demand, interactive sessions and larger-scale batch processing. The choice depends on the application, ranging from a real-time conversational agent needing immediate tool access to a data-analysis pipeline that processes records in batches.

### Security, error handling, and implementation

- **Security** — Exposing tools and data via any protocol requires robust security. An MCP implementation must include authentication and authorization to control which clients can access which servers and what specific actions they are permitted to perform.
- **Error Handling** — A comprehensive error-handling strategy is critical. The protocol must define how errors (tool execution failure, unavailable server, invalid request) are communicated back to the LLM so it can understand the failure and potentially try an alternative approach.
- **Implementation** — Although MCP is an open standard, its implementation can be complex. Providers are simplifying this: model providers such as Anthropic, and frameworks like FastMCP, offer SDKs that abstract away much of the boilerplate, making it easier to create and connect MCP clients and servers. FastMCP is a high-level Python framework that streamlines MCP server development, lets developers define tools, resources, and prompts quickly, and performs automatic schema generation by interpreting function signatures, type hints, and documentation strings to construct the interface specifications the model needs. It also supports advanced patterns such as server composition and proxying for modular, distributed, scalable systems. The Agent Development Kit (ADK) supports both using existing MCP servers and exposing ADK tools via an MCP server.

## Practical Applications & Use Cases

MCP significantly broadens AI/LLM capabilities. Nine key use cases:

- **Database Integration** — Agents seamlessly access and interact with structured data in databases. Using the MCP Toolbox for Databases, an agent can query datasets (e.g., Google BigQuery) to retrieve real-time information, generate reports, or update records, all driven by natural-language commands.
- **Generative Media Orchestration** — Agents integrate with advanced generative media services. Through MCP Tools for Genmedia Services, an agent can orchestrate workflows involving Google's Imagen (image generation), Veo (video creation), Chirp 3 HD (realistic voices), or Lyria (music composition) for dynamic content creation.
- **External API Interaction** — A standardized way for LLMs to call and receive responses from any external API: fetch live weather data, pull stock prices, send emails, or interact with CRM systems, extending capabilities far beyond the core model.
- **Reasoning-Based Information Extraction** — Leveraging an LLM's reasoning, MCP enables query-dependent extraction that surpasses conventional search and retrieval. Instead of returning an entire document, an agent can analyze text and extract the precise clause, figure, or statement that directly answers a complex question.
- **Custom Tool Development** — Developers can build custom tools and expose them via an MCP server (e.g., using FastMCP), making specialized internal functions or proprietary systems available to LLMs and other agents in a standardized, consumable format without modifying the LLM directly.
- **Standardized LLM-to-Application Communication** — MCP ensures a consistent communication layer between LLMs and the applications they interact with, reducing integration overhead, promoting interoperability across providers and host applications, and simplifying development of complex agentic systems.
- **Complex Workflow Orchestration** — By combining various MCP-exposed tools and data sources, an agent can orchestrate multi-step workflows: e.g., retrieve customer data from a database, generate a personalized marketing image, draft a tailored email, and send it, all via different MCP services.
- **IoT Device Control** — MCP can facilitate LLM interaction with Internet of Things devices, sending commands to smart home appliances, industrial sensors, or robotics for natural-language control and automation of physical systems.
- **Financial Services Automation** — MCP enables LLMs to interact with financial data sources, trading platforms, and compliance systems: analyzing market data, executing trades, generating personalized financial advice, or automating regulatory reporting, all over secure, standardized communication.

In short, MCP lets agents access real-time information from databases, APIs, and web resources; perform actions like sending emails, updating records, and controlling devices; execute complex multi-source tasks; and drive media generation tools.

## Trade-offs & When to Use

**MCP vs. tool function calling.** Both extend LLMs beyond text generation, but they differ in approach and level of abstraction.

Tool function calling is a direct request from an LLM to a specific, pre-defined tool or function ("tool" and "function" are used interchangeably). It is a one-to-one communication model: the LLM formats a request based on its understanding of user intent, the application code executes it and returns the result to the LLM. This process is often proprietary and varies across LLM providers.

MCP, by contrast, is a standardized interface for LLMs to discover, communicate with, and use external capabilities. It is an open protocol aiming to establish an ecosystem where any compliant tool can be accessed by any compliant LLM, fostering interoperability, composability, and reusability. By adopting a federated model, organizations can bring disparate and legacy services into a modern ecosystem simply by wrapping them in an MCP-compliant interface; those services keep operating independently but can be composed into new applications and workflows orchestrated by LLMs, gaining agility and reusability without costly rewrites of foundational systems.

The fundamental distinctions:

| Feature | Tool Function Calling | Model Context Protocol (MCP) |
|---|---|---|
| **Standardization** | Proprietary and vendor-specific; format and implementation differ across LLM providers. | An open, standardized protocol promoting interoperability between different LLMs and tools. |
| **Scope** | A direct mechanism for an LLM to request execution of a specific, predefined function. | A broader framework for how LLMs and external tools discover and communicate with each other. |
| **Architecture** | A one-to-one interaction between the LLM and the application's tool-handling logic. | A client-server architecture where LLM-powered applications (clients) connect to and use various MCP servers (tools). |
| **Discovery** | The LLM is explicitly told which tools are available within a specific conversation. | Enables dynamic discovery: a client can query a server to see what capabilities it offers. |
| **Reusability** | Tool integrations are often tightly coupled to the specific application and LLM. | Promotes reusable, standalone MCP servers accessible by any compliant application. |

An analogy: tool function calling is like giving an AI a specific set of custom-built tools (a particular wrench and screwdriver) — efficient for a workshop with a fixed set of tasks. MCP is like a universal, standardized power-outlet system; it doesn't provide the tools itself, but it lets any compliant tool from any manufacturer plug in and work, enabling a dynamic, ever-expanding workshop.

**Rule of thumb.** Use MCP when building complex, scalable, or enterprise-grade agentic systems that must interact with a diverse and evolving set of external tools, data sources, and APIs; when interoperability between different LLMs and tools is a priority; and when agents need to dynamically discover new capabilities without being redeployed. For simpler applications with a fixed, limited number of predefined functions, direct tool function calling may be sufficient.

## Pitfalls

- **Wrapping legacy APIs unchanged.** MCP only exposes whatever the underlying API offers. Wrapping a poorly designed legacy API (e.g., one that only returns full records one at a time) yields slow, inaccurate agent behavior at volume. Add deterministic features such as filtering and sorting to support the non-deterministic agent. Agents do not replace deterministic workflows — they often need more deterministic support.
- **Non-agent-friendly data formats.** MCP does not enforce that exchanged data is understandable by the agent. Returning PDFs to an agent that cannot parse them is useless; prefer agent-readable formats such as Markdown/text. Consider the nature of the data, not just the connection.
- **Inadequate security.** Exposing tools and data demands authentication and authorization controlling which clients reach which servers and which actions they may perform.
- **Weak error handling.** Failures (tool errors, unavailable servers, invalid requests) must be communicated back to the LLM so it can understand and recover or try alternatives.
- **Implementation complexity.** The open standard can be complex to implement directly; SDKs (Anthropic's, FastMCP) mitigate this boilerplate.

## Relationships to Other Patterns

- **Tool Function Calling** — MCP is the standardized, discoverable, client-server superset of direct function calling. Function calling gives direct access to a few specific functions; MCP is the communication framework that lets LLMs discover and use a vast, evolving range of external resources.
- **Multi-agent / A2A-style orchestration** — MCP's federated model lets independently operating services be composed into new applications and workflows whose collaboration is orchestrated by LLMs, complementing higher-level agent coordination.
- **Agent Development Kit (ADK)** — ADK can act as an MCP client to consume existing MCP servers (local via STDIO, remote via HTTP) and can also expose ADK tools through an MCP server. FastMCP is a complementary framework for authoring MCP servers in Python.

## Key Takeaways

- MCP is an open standard for standardized communication between LLMs and external applications, data sources, and tools.
- It uses a client-server architecture defining how resources, prompts, and tools are exposed and consumed.
- Its three primitives are distinct: resources are static data, tools are executable actions, and prompts are templates that structure how the LLM interacts with a resource or tool.
- Dynamic, just-in-time discovery lets agents adapt to new capabilities without redeployment.
- Transports are JSON-RPC over STDIO for local use and web-friendly protocols (Streamable HTTP, SSE) for remote use.
- MCP's value depends on well-designed, agent-friendly underlying APIs and data formats, plus robust security and error handling.
- ADK supports both consuming existing MCP servers and exposing ADK tools via MCP; FastMCP simplifies building MCP servers in Python.
- MCP Tools for Genmedia Services let agents integrate with Google Cloud generative media (Imagen, Veo, Chirp 3 HD, Lyria).
- MCP lets LLMs and agents interact with real-world systems, access dynamic information, and perform actions beyond text generation.

## References

1. Model Context Protocol (MCP) Documentation. https://google.github.io/adk-docs/mcp/
2. FastMCP Documentation. https://github.com/jlowin/fastmcp
3. MCP Tools for Genmedia Services. https://google.github.io/adk-docs/mcp/#mcp-servers-for-google-cloud-genmedia
4. MCP Toolbox for Databases Documentation. https://google.github.io/adk-docs/mcp/databases/
