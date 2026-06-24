# Building an Agent with AgentSpace

> Google AgentSpace is a platform for the "agent-driven enterprise," embedding intelligent, autonomous agents directly into organizational workflows through a no-code interface.

## Overview

AgentSpace is a platform designed to facilitate an "agent-driven enterprise" by integrating artificial intelligence into daily workflows. At its core it provides a unified search capability across an organization's entire digital footprint, including documents, emails, and databases, using advanced AI models (such as Google's Gemini) to comprehend and synthesize information from these varied sources.

The platform enables the creation and deployment of specialized AI "agents" that perform complex tasks and automate processes. These agents are more than chatbots; they can reason, plan, and execute multi-step actions autonomously. For instance, an agent could research a topic, compile a report with citations, and even generate an audio summary.

## Key Concepts

- **Enterprise Knowledge Graph:** AgentSpace constructs a knowledge graph mapping the relationships between people, documents, and data, allowing the AI to understand context and deliver more relevant, personalized results.
- **Agent Designer:** A no-code interface for creating custom agents without deep technical expertise.
- **Multi-Agent Collaboration via A2A:** AgentSpace supports a multi-agent system where different agents communicate and collaborate through an open protocol, the Agent2Agent (A2A) Protocol. This interoperability enables more complex, orchestrated workflows.
- **Security as a foundation:** Features such as role-based access controls and data encryption protect sensitive enterprise information.
- **Goal:** Enhance productivity and decision-making by embedding intelligent, autonomous systems directly into an organization's operational fabric.

## Building an Agent (UI Walkthrough, prose)

The book illustrates the build process through a series of console screenshots, summarized here without the images:

- **Access:** AgentSpace is reached by selecting AI Applications from the Google Cloud Console.
- **Connect services:** An agent can be connected to various services, including Calendar, Google Mail, Workday, Jira, Outlook, and ServiceNow, integrating both Google and third-party platforms.
- **Choose or write a prompt:** The agent can use a prompt selected from Google's gallery of pre-assembled prompts, or the user can create a custom prompt that the agent will then use.
- **Advanced features:** AgentSpace offers integration with datastores (to store your own data), integration with the Google Knowledge Graph or a private knowledge graph, a web interface for exposing the agent to the web, and analytics to monitor usage, among others.
- **Use the agent:** Upon completion, the AgentSpace chat interface becomes accessible for initiating a chat with the agent.

## Key Takeaways

- AgentSpace provides a functional framework for developing and deploying AI agents within an organization's existing digital infrastructure.
- Its architecture links complex backend processes, such as autonomous reasoning and enterprise knowledge-graph mapping, to a graphical interface for agent construction.
- Through this interface, users configure agents by integrating data services and defining operational parameters via prompts, producing customized, context-aware automated systems.
- The approach abstracts underlying technical complexity, enabling specialized multi-agent systems without deep programming expertise.
- The primary objective is to embed automated analytical and operational capabilities directly into workflows, increasing process efficiency and enhancing data-driven analysis.
- Hands-on learning is available, such as the "Build a Gen AI Agent with Agentspace" lab on Google Cloud Skills Boost, which offers a structured environment for skill acquisition.
