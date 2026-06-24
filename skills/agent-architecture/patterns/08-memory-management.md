# Memory Management

> Equipping agents with short-term (contextual) and long-term (persistent) memory so they can retain and reuse information from past interactions, observations, and learning experiences.

## Overview

Effective memory management is crucial for intelligent agents to retain information. Like humans, agents require different types of memory to operate efficiently. In agent systems, "memory" refers to an agent's ability to retain and utilize information from past interactions, observations, and learning experiences. This capability lets agents make informed decisions, maintain conversational context, and improve over time. Without a memory mechanism, agents are stateless — unable to maintain conversational context, learn from experience, or personalize responses — which fundamentally limits them to simple, one-shot interactions and prevents them from handling multi-step processes or evolving user needs.

The core problem the pattern addresses is how to effectively manage two distinct things at once: the immediate, temporary information of a single conversation, and the vast, persistent knowledge gathered over time. Agent memory is generally categorized into two main types:

- **Short-Term Memory (Contextual Memory):** Analogous to human working memory, this holds information currently being processed or recently accessed. For agents built on large language models (LLMs), short-term memory primarily exists within the LLM's context window. This window contains recent messages, agent replies, tool-usage results, and the agent's own reflections from the current interaction — all of which inform the LLM's subsequent responses and actions. The context window has limited capacity, restricting how much recent information an agent can directly access. Efficient short-term memory management means keeping the most relevant information within this limited space, often via techniques such as summarizing older conversation segments or emphasizing key details. Models with "long context" windows simply expand the size of this short-term memory, allowing more information to be held within a single interaction. However, this context is still ephemeral — it is lost once the session concludes, and reprocessing it every time can be costly and inefficient. Consequently, agents require separate memory types to achieve true persistence, recall information from past interactions, and build a lasting knowledge base.

- **Long-Term Memory (Persistent Memory):** This acts as a repository for information that agents need to retain across various interactions, tasks, or extended periods, akin to a long-term knowledge base. Data is typically stored outside the agent's immediate processing environment — often in databases, knowledge graphs, or vector databases. In vector databases, information is converted into numerical vectors and stored, enabling retrieval based on semantic similarity rather than exact keyword matches (a process known as semantic search). When an agent needs information from long-term memory, it queries the external storage, retrieves relevant data, and integrates it into the short-term context for immediate use, thereby combining prior knowledge with the current interaction.

## How It Works

The standardized solution is a dual-component memory system that distinguishes between short-term and long-term storage.

**Short-term memory** holds recent interaction data within the LLM's context window to maintain conversational flow. Because the full history of a conversation can overflow an LLM's context window — leading to errors or degraded performance — frameworks manage how this context is passed, sometimes summarizing or truncating it. Some frameworks (e.g., LangGraph) manage short-term memory as part of the agent's state, persisted via a checkpointer so a conversation thread can be resumed at any time.

**Long-term memory** stores information that must persist, using external databases (often vector stores) for efficient, semantic retrieval. The retrieval flow is: the agent queries the external store, gets back relevant data, and incorporates it into its current context. This is the same machinery underlying Retrieval Augmented Generation (RAG).

### Memory in Google ADK (Session, State, Memory)

The Google Agent Developer Kit (ADK) offers a structured method for managing context and memory, built on three core concepts and their associated services. Every interaction with an agent is treated as a unique conversation thread.

- **Session** — an individual chat thread that logs messages and actions (as Event objects) for that specific interaction, and also stores temporary data (State) relevant to that conversation. A Session object encapsulates unique identifiers (id, app_name, user_id), a chronological record of events, the state storage area, and a last-update timestamp. Developers typically interact with Session objects indirectly through the SessionService.

- **State (session.state)** — data stored within a Session, relevant only to the current, active chat thread. It functions as the agent's temporary working memory ("scratchpad") for the duration of that conversation.

- **Memory** — a searchable repository of information sourced from various past chats or external sources, serving as a resource for data retrieval beyond the immediate conversation.

ADK provides dedicated services to manage these:

- **SessionService** manages the lifecycle of conversation sessions: initiating new sessions, resuming previous ones, recording session activity (including state updates), identifying active sessions, and removing session data. ADK offers several implementations with different storage backends:
  - *InMemorySessionService* — suitable for local development and testing, but does not persist data across application restarts.
  - *DatabaseSessionService* — reliable saving to a database you manage (e.g., SQLite, PostgreSQL), suitable for production or development needing persistent storage.
  - *VertexAiSessionService* — uses Vertex AI infrastructure for scalable production on Google Cloud; the app name corresponds to a Reasoning Engine resource.

  Choosing the right SessionService is important because it determines how interaction history and temporary data are stored and how persistent they are.

  Each message exchange is a cyclical process: a message is received; the **Runner** retrieves or establishes a Session via the SessionService; the agent processes the message using the Session's context (state and historical interactions); the agent generates a response and may update state; the Runner encapsulates this as an Event; and the `append_event` method records the new event and updates state in storage. The Session then awaits the next message. Ideally, a delete-session method terminates the session when the interaction concludes. This is how the SessionService maintains continuity.

**Working with State.** While `session.events` logs the entire chat history, `session.state` stores and updates dynamic data points relevant to the active chat — user preferences, task progress, incremental data collection, or conditional flags that influence subsequent agent actions. State is fundamentally a dictionary of key-value pairs, where keys are strings and values are serializable basic types (strings, numbers, booleans, lists, and dictionaries of these). State is dynamic and evolves throughout the conversation; the permanence of changes depends on the configured SessionService.

State organization uses **key prefixes** to define scope and persistence:
- No prefix — session-specific data.
- `user:` — data associated with a user ID across all that user's sessions.
- `app:` — data shared among all users of the application.
- `temp:` — data valid only for the current processing turn, not persistently stored.

The agent accesses all state through the single `session.state` dictionary; the SessionService handles retrieval, merging, and persistence. State should be updated when adding an Event to the session history (via `append_event`), ensuring accurate tracking, proper saving, and safe handling of changes.

ADK supports two recommended ways to update state:
1. **The simple way — `output_key`** (for an agent's final text replies): when configuring an LlmAgent, you specify an `output_key`. The Runner automatically saves the agent's final text response into that state key (behind the scenes it builds a `state_delta` when it appends the event). This is the easiest method when you just want to capture the agent's final text.
2. **The standard way — `EventActions.state_delta`** (for more complex updates): for updating several keys at once, saving non-text data, targeting specific scopes like `user:` or `app:`, or making updates not tied to the agent's final text reply, you manually build a dictionary of state changes (the state_delta) and include it within the EventActions of the event you append.

The chapter illustrates the recommended pattern of encapsulating state changes inside a **tool**. A login-tracking tool, for example, receives a ToolContext (supplied automatically by ADK) that gives it access to the session state; inside the tool it increments a `user:login_count`, sets a `task_status`, records a `user:last_login_ts` timestamp, and adds a `temp:validation_needed` flag — then returns a confirmation. Co-locating state logic inside tools makes the code cleaner and more robust than manipulating state externally.

**Direct modification of the `session.state` dictionary after retrieving a session is strongly discouraged.** It bypasses the standard event-processing mechanism, so the changes are not recorded in the event history, may not be persisted by the chosen SessionService, can cause concurrency issues, and won't update essential metadata such as timestamps. `session.state` should primarily be used for *reading* existing data; updates should always go through the append-event process via `output_key` or `state_delta`. Design guidance: keep state simple, use basic data types, give keys clear names and correct prefixes, avoid deep nesting, and always update via the append-event process.

**MemoryService (long-term knowledge).** Whereas Session and State are short-term memory for a single chat, the long-term knowledge managed by the MemoryService is a persistent, searchable repository that may contain information from multiple past interactions or external sources. The MemoryService interface (BaseMemoryService) defines a standard for managing this knowledge, with two primary functions: **adding information** (extracting content from a session and storing it, via an `add_session_to_memory` method) and **retrieving information** (querying the store to receive relevant data, via a `search_memory` method). Implementations include:
- *InMemoryMemoryService* — temporary storage for testing; content is lost when the app stops.
- *VertexAiRagMemoryService* — the typical production choice, leveraging Google Cloud's RAG service for scalable, persistent, semantic search. It can be configured with retrieval parameters such as the number of top results to retrieve and a vector-distance/similarity threshold.

### Memory in LangChain and LangGraph

In LangChain and LangGraph, memory is critical for creating intelligent, natural-feeling conversational applications, letting an agent remember past interactions, learn from feedback, and adapt to user preferences. LangChain's memory feature references a stored history to enrich current prompts and then records the latest exchange for future use.

- **Short-term memory** is thread-scoped — it tracks the ongoing conversation within a single session or thread, providing immediate context. A full history can overflow the LLM's context window. LangGraph manages short-term memory as part of the agent's state, persisted via a checkpointer so a thread can be resumed at any time.
- **Long-term memory** stores user-specific or application-level data across sessions, shared between conversational threads. It is saved in custom "namespaces" and can be recalled at any time in any thread. LangGraph provides stores to save and recall long-term memories, enabling agents to retain knowledge indefinitely.

LangChain provides several tools for managing conversation history, ranging from manual control to automated chain integration:
- **ChatMessageHistory** — for direct, simple control over a conversation's history outside a formal chain; it allows manual tracking of dialogue exchanges (adding user and AI messages, accessing the message list).
- **ConversationBufferMemory** — for integrating memory directly into chains; it holds a buffer of the conversation and makes it available to the prompt. Two key parameters customize its behavior: `memory_key` (a string naming the prompt variable that will hold the history; defaults to "history") and `return_messages` (a boolean controlling format — `False`/default returns a single formatted string ideal for standard LLMs, while `True` returns a list of message objects, the recommended format for chat models). The chapter shows it wired into an LLMChain so the model can access conversation history (e.g., a travel-agent chain that remembers the user's name across turns), and demonstrates the chat-model variant using a ChatPromptTemplate with a MessagesPlaceholder and `return_messages=True`.

**Types of long-term memory** (LangChain/LangGraph frame three types analogous to human memory):
- **Semantic Memory — remembering facts:** retaining specific facts and concepts, such as user preferences or domain knowledge, used to ground an agent's responses for more personalized, relevant interactions. It can be managed as a continuously updated user "profile" (a single JSON document) or as a "collection" of individual factual documents.
- **Episodic Memory — remembering experiences:** recalling past events or actions. For agents, this is often used to remember *how* to accomplish a task, frequently implemented through few-shot example prompting, where the agent learns from past successful interaction sequences.
- **Procedural Memory — remembering rules:** the memory of how to perform tasks — the agent's core instructions and behaviors, often contained in its system prompt. Agents commonly modify their own prompts to adapt and improve. An effective technique is **"Reflection,"** where an agent is prompted with its current instructions plus recent interactions and asked to refine its own instructions. The chapter sketches (in pseudocode) a LangGraph flow with an "update_instructions" node that reads current instructions from a BaseStore, asks the LLM to reflect on the conversation and generate improved instructions, and writes them back; and a "call_model" node that retrieves the latest instructions from the store to format its prompt.

LangGraph stores long-term memories as **JSON documents in a store**, organized under a custom **namespace** (like a folder) and a distinct **key** (like a filename) — a hierarchical structure for easy organization and retrieval. The chapter demonstrates an InMemoryStore (which can be configured with an embedding function and vector dimensions) supporting three operations: *put* a memory under a namespace and key (e.g., storing rules like "User likes short, direct language"), *get* a memory by namespace and key, and *search* within a namespace by filtering on content and sorting by vector similarity to a query. For production, a database-backed store is used instead of the in-memory one.

### Vertex Memory Bank

Memory Bank, a managed service in the Vertex AI Agent Engine, provides agents with persistent, long-term memory. It uses Gemini models to **asynchronously analyze conversation histories** to extract key facts and user preferences. This information is stored persistently, organized by a defined scope such as user ID, and **intelligently updated to consolidate new data and resolve contradictions**. When a new session starts, the agent retrieves relevant memories through either a full data recall or a similarity search using embeddings, allowing it to maintain continuity across sessions and personalize responses.

In ADK, the agent's runner interacts with a VertexAiMemoryBankService (initialized with project, location, and an agent-engine ID). This service handles automatic storage of memories generated during conversations; each memory is tagged with a unique user ID and app name to ensure accurate future retrieval. The flow involves getting the session and calling `add_session_to_memory`. Memory Bank integrates out-of-the-box with Google ADK and also supports other frameworks such as LangGraph and CrewAI through direct API calls.

## Practical Applications & Use Cases

Memory management lets agents track information and act intelligently over time, surpassing basic question-answering. Applications include:

- **Chatbots and Conversational AI:** Short-term memory maintains conversation flow by remembering prior user inputs for coherent responses. Long-term memory lets chatbots recall user preferences, past issues, or prior discussions, offering personalized, continuous interactions.
- **Task-Oriented Agents:** Agents managing multi-step tasks need short-term memory to track previous steps, current progress, and overall goals (held in the task's context or temporary storage). Long-term memory is crucial for accessing specific user-related data not in the immediate context.
- **Personalized Experiences:** Agents use long-term memory to store and retrieve user preferences, past behaviors, and personal information, adapting their responses and suggestions.
- **Learning and Improvement:** Agents refine performance by learning from past interactions — storing successful strategies, mistakes, and new information in long-term memory. Reinforcement-learning agents store learned strategies or knowledge this way.
- **Information Retrieval (RAG):** Question-answering agents access a knowledge base (their long-term memory), often implemented as Retrieval Augmented Generation, retrieving relevant documents or data to inform responses.
- **Autonomous Systems:** Robots or self-driving cars need memory for maps, routes, object locations, and learned behaviors — short-term memory for immediate surroundings and long-term memory for general environmental knowledge.

## Trade-offs & When to Use

**Rule of thumb:** Use this pattern whenever an agent needs to do more than answer a single question. It is essential for agents that must maintain context throughout a conversation, track progress in multi-step tasks, or personalize interactions by recalling user preferences and history. Implement memory management whenever the agent is expected to learn or adapt based on past successes, failures, or newly acquired information.

Key trade-offs surfaced in the chapter:
- **Short-term memory is fast but ephemeral and bounded.** The context window is limited in capacity; even "long context" models only enlarge it. Context is lost when the session ends, and reprocessing large contexts on every turn is costly and inefficient.
- **Long-term memory is persistent and scalable but external.** It requires separate infrastructure (databases, knowledge graphs, vector stores) and a retrieval step (semantic search) to bring relevant data back into context.
- **Storage choices trade convenience for durability.** In-memory services are convenient for testing but lose data on restart; database-backed and cloud services (e.g., Vertex AI) provide persistence and scalability at the cost of setup and infrastructure.

## Pitfalls

- **Directly mutating `session.state` in ADK after retrieving a session.** This bypasses the standard event-processing mechanism: changes are not recorded in the event history, may not be persisted by the chosen SessionService, can cause concurrency issues, and won't update metadata such as timestamps. Always update through `output_key` or `EventActions.state_delta` via the append-event process; treat `session.state` as read-mostly.
- **Overflowing the context window.** Passing a full conversation history can exceed the LLM's context window, leading to errors or degraded performance. Mitigate with summarization, truncation, or framework-managed state.
- **Poor state design.** Avoid deep nesting and non-serializable values; use basic data types, clear key names, and correct prefixes (`user:`, `app:`, `temp:`).

## Relationships to Other Patterns

- **Retrieval Augmented Generation (RAG):** Long-term memory for question-answering agents is often implemented as RAG; ADK's production MemoryService (VertexAiRagMemoryService) is built directly on Google Cloud's RAG service. (The book devotes a separate chapter, Chapter 14, to RAG.)
- **Learning and Adaptation:** Memory is the foundation that enables agents to learn and adapt; procedural memory updated via Reflection is an example of an agent changing its own behavior based on experience. The chapter explicitly leads into the "Learning and Adaptation" pattern as the next step after memory.
- **Tool Use:** ADK recommends encapsulating state changes inside tools (using a ToolContext), tying memory updates to the tool-use pattern.
- **Reflection:** Used to refine an agent's procedural memory (its own instructions) based on its current instructions and recent interactions.

## Key Takeaways

- Memory is essential for agents to keep track of things, learn, and personalize interactions.
- Conversational AI relies on both short-term memory (immediate context within a single chat) and long-term memory (persistent knowledge across multiple sessions).
- Short-term memory is temporary, often limited by the LLM's context window or how the framework passes context.
- Long-term memory persists across chats using external storage such as vector databases and is accessed by searching (semantic similarity).
- Frameworks like ADK provide specific parts — Session (the chat thread), State (temporary chat data), and MemoryService (searchable long-term knowledge) — to manage memory.
- ADK's SessionService handles a chat session's whole lifecycle, including its history (events) and temporary data (state). Implementations range from in-memory (testing) to database-backed and Vertex AI (production).
- ADK's `session.state` is a dictionary for temporary chat data; prefixes (`user:`, `app:`, `temp:`) indicate scope and persistence.
- In ADK, update state via `EventActions.state_delta` or `output_key` when adding events — never by changing the state dictionary directly.
- ADK's MemoryService stores info in long-term storage and lets agents search it, often via tools.
- LangChain offers practical tools like ConversationBufferMemory to automatically inject a single conversation's history into a prompt, recalling immediate context.
- LangGraph enables advanced long-term memory via a store that saves and retrieves semantic facts, episodic experiences, or even updatable procedural rules across user sessions, organized by namespace and key.
- Vertex Memory Bank is a managed service that provides persistent long-term memory by automatically extracting, storing, and recalling user-specific information for personalized, continuous conversations across frameworks like Google ADK, LangGraph, and CrewAI.

## References

1. ADK Memory — https://google.github.io/adk-docs/sessions/memory/
2. LangGraph Memory — https://langchain-ai.github.io/langgraph/concepts/memory/
3. Vertex AI Agent Engine Memory Bank — https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-memory-bank-in-public-preview
