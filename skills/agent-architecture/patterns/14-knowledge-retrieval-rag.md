# Knowledge Retrieval (RAG)

> Retrieval-Augmented Generation (RAG) lets an LLM consult an external knowledge base before answering, grounding its output in current, verifiable, domain-specific data instead of relying solely on static training knowledge.

## Overview

LLMs generate fluent, human-like text, but their knowledge is confined to the data they were trained on. That makes them blind to real-time information, private company data, and highly specialized details, and it leaves their answers prone to being outdated, inaccurate, or lacking the context a specialized task demands. The Knowledge Retrieval (RAG) pattern addresses this by granting the model access to external knowledge bases at query time, so it can "look up" information much as a human might consult a book or search the internet.

The core idea is a two-step flow — **Retrieval** followed by **Augmentation** — wrapped around generation. When a user poses a question, the query is not sent straight to the LLM. Instead the system first searches a large external knowledge base (a library of documents, databases, or web pages) for relevant information, pulls out the most pertinent snippets or "chunks," and adds (augments) them to the original prompt. This enriched prompt is then handed to the LLM, which produces a response that is fluent and natural but also factually grounded in the retrieved data. In effect, RAG transforms the LLM from a closed-book reasoner into an open-book one.

For AI agents this is especially important: it lets them ground actions and responses in real-time, verifiable data rather than static training. An agent can pull the latest company policy to answer a specific question, or check current inventory before placing an order, turning it from a simple conversationalist into a data-driven tool capable of meaningful work.

The benefits the chapter emphasizes:
- **Up-to-date information** — overcomes the constraints of static training data.
- **Reduced hallucination** — grounding responses in verifiable data lowers the risk of fabricated information.
- **Specialized knowledge** — the LLM can draw on internal company documents or wikis.
- **Citations / attribution** — RAG can pinpoint the exact source of information, making answers trustworthy and verifiable.

The chapter also covers two advanced evolutions of the base pattern — **GraphRAG** (retrieval over a knowledge graph) and **Agentic RAG** (a reasoning layer that actively validates and refines retrieved knowledge) — plus the practical limitations and challenges of all three.

## How It Works

### Core concepts behind retrieval

**Embeddings.** Embeddings are numerical representations of text — words, phrases, or whole documents — expressed as a vector (a list of numbers). They capture the semantic meaning of and relationships between pieces of text within a mathematical space, such that text with similar meanings ends up close together in the vector space. The chapter uses an illustrative 2D analogy: "cat" might sit at coordinates (2, 3), "kitten" very close at (2.1, 3.1), while "car" sits far away at (8, 1), reflecting its different meaning. In reality, embeddings live in much higher-dimensional spaces — hundreds or thousands of dimensions — enabling a very nuanced understanding of language.

**Text similarity.** A measure of how alike two pieces of text are. This can be surface-level (lexical similarity — overlap of words) or deeper and meaning-based. In RAG, text similarity is crucial for finding the knowledge-base content most relevant to a query. Example: "What is the capital of France?" and "Which city is the capital of France?" are worded differently but ask the same thing; a good similarity model assigns them a high similarity score even though they share few words. This is typically computed using the texts' embeddings.

**Semantic similarity and semantic distance.** Semantic similarity is a more advanced form of text similarity focused purely on meaning and context rather than the specific words used — it asks whether two texts convey the same concept or idea. Semantic distance is its inverse: high semantic similarity means low semantic distance, and vice versa. Semantic search in RAG works by finding documents with the smallest semantic distance to the user's query. Example: "a furry feline companion" and "a domestic cat" share no words besides "a," yet a semantically aware model recognizes they refer to the same thing because their embeddings sit close together in vector space. This "smart search" is what lets RAG find relevant material even when the user's wording does not match the source text.

### Chunking of documents

Chunking breaks large documents into smaller, manageable pieces ("chunks"). A RAG system cannot feed whole large documents into the LLM, so it processes chunks instead. How documents are chunked matters for preserving context and meaning. Rather than treat a 50-page user manual as one block of text, a chunking strategy might split it into sections, paragraphs, or even sentences — so a "Troubleshooting" section becomes a separate chunk from the "Installation Guide." When a user asks about a specific problem, the system retrieves the relevant troubleshooting chunk rather than the entire manual, making retrieval faster and the context fed to the LLM more focused and relevant.

### Retrieval techniques

Once documents are chunked, the system needs a retrieval technique to find the most relevant pieces for a query:

- **Vector search** — the primary method. It uses embeddings and semantic distance to find chunks conceptually similar to the user's question.
- **BM25** — an older but still valuable keyword-based algorithm that ranks chunks by term frequency, without understanding semantic meaning.
- **Hybrid search** — combines BM25's keyword precision with semantic search's contextual understanding. This fusion captures both literal matches and conceptual relevance, giving more robust and accurate retrieval.

### Vector databases

A vector database is a specialized database built to store and query embeddings efficiently. After documents are chunked and converted into embeddings, those high-dimensional vectors are stored there. Traditional keyword-based search is good at finding exact-word matches but lacks deep language understanding — it would not recognize that "furry feline companion" means "cat." Vector databases are built for semantic search: by storing text as numerical vectors they find results by conceptual meaning, not keyword overlap. When the user's query is also converted to a vector, the database uses highly optimized algorithms — the chapter names **HNSW (Hierarchical Navigable Small World)** — to rapidly search through millions of vectors and find the ones closest in meaning. The chapter's summary phrase: other techniques search for words, vector databases search for meaning.

The chapter lists representative tooling:
- **Managed vector databases:** Pinecone, Weaviate.
- **Open-source vector databases:** Chroma DB, Milvus, Qdrant.
- **Existing databases augmented with vector search:** Redis, Elasticsearch, Postgres (via the pgvector extension).
- **Underlying retrieval libraries** that power the core mechanisms: Meta AI's FAISS and Google Research's ScaNN, which are fundamental to these systems' efficiency.

### The end-to-end flow

1. **Pre-process:** chunk source documents, embed each chunk, and store the embeddings in a vector database (or knowledge graph).
2. **Query time — retrieve:** embed the user's query, then search the store for the chunks with the smallest semantic distance (optionally combined with keyword/BM25 scoring in hybrid search).
3. **Augment:** append the retrieved snippets to the original prompt to build a richer, more informed query.
4. **Generate:** send the augmented prompt to the LLM, which answers grounded in the retrieved context — and can cite its sources.

### GraphRAG

GraphRAG is an advanced form of RAG that uses a **knowledge graph** instead of a simple vector database for retrieval. It answers complex queries by navigating the explicit relationships (edges) between data entities (nodes) within a structured knowledge base. Its key advantage is the ability to synthesize answers from information fragmented across multiple documents — a common failing of traditional RAG — and by understanding these connections it provides more contextually accurate, nuanced responses. Its effectiveness is entirely dependent on the quality and completeness of the underlying graph structure. GraphRAG offers superior contextual reasoning for intricate questions, but at much higher implementation and maintenance cost; it excels where deep, interconnected insight matters more than the speed and simplicity of standard RAG.

### Agentic RAG

Agentic RAG adds a reasoning and decision-making layer to substantially improve the reliability of information extraction. Instead of passively retrieving and augmenting, a specialized AI component — an "agent" — acts as a gatekeeper and refiner of knowledge. Rather than accepting the initially retrieved data at face value, the agent actively interrogates its quality, relevance, and completeness. The chapter illustrates four agent capabilities:

1. **Reflection and source validation.** Asked "What is our company's policy on remote work?", standard RAG might surface a 2020 blog post alongside the official 2025 policy. The agent analyzes document metadata, recognizes the 2025 policy as the most current and authoritative source, discards the outdated blog post, and sends only the correct context to the LLM.

2. **Reconciling knowledge conflicts.** Asked "What was Project Alpha's Q1 budget?", the system retrieves an initial proposal stating €50,000 and a finalized financial report listing €65,000. The agent identifies the contradiction, prioritizes the finalized report as the more reliable source, and gives the LLM the verified figure.

3. **Multi-step reasoning to synthesize complex answers.** Asked "How do our product's features and pricing compare to Competitor X's?", the agent decomposes the question into separate sub-queries (own features, own pricing, Competitor X's features, Competitor X's pricing), runs distinct searches, then synthesizes the results into a structured comparative context before feeding it to the LLM — enabling a comprehensive answer a single retrieval could not produce.

4. **Identifying knowledge gaps and using external tools.** Asked "What was the market's immediate reaction to our product launched yesterday?", the agent searches the internal knowledge base (updated only weekly), finds nothing relevant, recognizes the gap, and activates an external tool — such as a live web-search API — to gather recent news and social-media sentiment, then uses that fresh data to give an up-to-the-minute answer.

In short, Agentic RAG turns the pattern from a passive data pipeline into an active, problem-solving framework: a reasoning layer that evaluates sources, reconciles conflicts, decomposes complex questions, and uses external tools.

### Implementation notes (described, not coded)

The chapter walks through three implementations conceptually:

- **Google Search grounding via ADK.** Because RAG is about accessing external information, a built-in search tool is itself a retrieval mechanism. An ADK agent is given a Google Search tool and an instruction to use it when researching topics, grounding the LLM in live search results.
- **Vertex AI RAG via ADK.** ADK's Vertex AI RAG memory service connects an agent to a Google Cloud Vertex AI RAG Corpus. It is configured with the corpus resource name plus optional retrieval parameters: a *similarity top-k* setting (how many of the most-similar chunks to retrieve) and a *vector distance threshold* (the maximum semantic distance allowed, filtering out results beyond it). This enables scalable, persistent semantic retrieval from the designated corpus.
- **A full LangChain + LangGraph pipeline.** A text document is loaded, split into overlapping chunks, embedded (OpenAI embeddings), and stored in a Weaviate vector store, which exposes a retriever. A LangGraph state graph manages a two-node workflow: a retrieve node queries the vector store for chunks relevant to the question, then a generate node feeds those chunks plus the question into a prompt template and an OpenAI LLM to produce a concise, context-grounded answer. The prompt instructs the assistant to answer only from the retrieved context and to say it does not know when the answer is absent.

## Practical Applications & Use Cases

- **Enterprise search and Q&A:** internal chatbots answering employee questions from HR policies, technical manuals, and product specs by extracting the relevant sections to inform the LLM.
- **Customer support and helpdesks:** precise, consistent answers drawn from product manuals, FAQs, and support tickets — reducing the need for human intervention on routine issues.
- **Personalized content recommendation:** retrieving articles or products semantically related to a user's preferences or past interactions, rather than relying on basic keyword matching.
- **News and current-events summarization:** integrating LLMs with real-time news feeds so that, when prompted about a current event, the system retrieves recent articles and produces an up-to-date summary.
- **Legal research** and other knowledge-intensive domains (noted among the practical applications).

GraphRAG-specific use cases highlighted in the chapter: complex financial analysis, connecting companies to market events, and scientific research such as discovering relationships between genes and diseases — situations where explicit relationships across many documents are central.

By incorporating external knowledge, RAG extends LLMs beyond simple communication into knowledge-processing systems.

## Trade-offs & When to Use

**Rule of thumb (from the chapter):** Use RAG when you need an LLM to answer questions or generate content based on specific, up-to-date, or proprietary information that was not part of its training data. It is ideal for Q&A systems over internal documents, customer-support bots, and any application that needs verifiable, fact-based responses with citations.

**Standard RAG vs. GraphRAG vs. Agentic RAG:**
- **Standard (vector) RAG** is the simplest and fastest; best when relevant facts tend to live in individual chunks and low latency/cost matters.
- **GraphRAG** gives superior contextual reasoning for intricate, interconnected questions and can synthesize across fragmented sources — but adds significant complexity, cost, and expertise to build/maintain the graph, is less flexible, and can introduce higher latency. Choose it when deep, interconnected insight outweighs speed and simplicity.
- **Agentic RAG** dramatically improves reliability and depth by validating sources, reconciling conflicts, decomposing questions, and calling tools — but adds complexity, cost, and latency, and the agent itself becomes a new potential source of error. Its trade-offs in complexity, latency, and cost must be carefully managed.

## Pitfalls

Challenges of standard RAG:
- **Fragmented information.** When the answer is spread across multiple chunks or documents rather than confined to one, the retriever may fail to gather all the necessary context, yielding incomplete or inaccurate answers.
- **Quality dependence.** Effectiveness hinges on the quality of chunking and retrieval; retrieving irrelevant chunks introduces noise and confuses the LLM.
- **Contradictory sources.** Synthesizing information from potentially conflicting sources remains a significant, unsolved hurdle.
- **Pre-processing burden.** The entire knowledge base must be pre-processed and stored in specialized (vector or graph) databases — a considerable undertaking — and it requires periodic reconciliation to stay current, which is especially crucial for evolving sources like company wikis.
- **Performance cost.** The retrieval-and-augment process can noticeably increase latency, operational cost, and the number of tokens used in the final prompt.

Challenges specific to GraphRAG:
- High complexity, cost, and expertise to build and maintain a high-quality knowledge graph; less flexible; higher latency than simple vector search; and effectiveness entirely dependent on graph quality and completeness.

Challenges specific to Agentic RAG:
- Significant increase in complexity and cost (designing, implementing, and maintaining the agent's decision logic and tool integrations).
- Increased latency from the agent's cycles of reflection, tool use, and multi-step reasoning.
- The agent as a new error source — flawed reasoning can get it stuck in useless loops, misinterpret a task, or improperly discard relevant information, degrading the final answer.

## Relationships to Other Patterns

- **Tool Use / Function Calling.** Agentic RAG depends on calling external tools — for example a live web-search API — when the agent detects a knowledge gap in its internal store; the built-in Google Search grounding example is itself retrieval-as-tool.
- **Reflection.** The agentic layer's source validation and conflict reconciliation are an applied form of the reflection pattern — the agent critiques and refines retrieved data before trusting it.
- **Planning / Multi-step reasoning.** Agentic RAG decomposes a complex question into sub-queries, runs them, and synthesizes the results, mirroring planning and decomposition patterns.
- **Memory.** RAG is implemented in ADK as a memory service (the Vertex AI RAG memory service), tying external knowledge retrieval to the agent's memory layer.
- **Knowledge graphs.** GraphRAG connects RAG to graph-structured knowledge bases, navigating explicit entity relationships rather than vector similarity alone.

## Key Takeaways

- RAG enhances LLMs by giving them access to external, up-to-date, and specific information, overcoming the limits of static training data.
- The process is two parts: **Retrieval** (searching a knowledge base for relevant snippets) and **Augmentation** (adding those snippets to the LLM's prompt).
- RAG reduces hallucinations, enables domain-specific knowledge integration, and allows attributable, citable answers grounded in retrieved sources.
- Foundational technologies are embeddings, semantic similarity/distance, chunking, semantic (and hybrid) search, and vector databases — which find information by meaning rather than keywords, at scale across millions of embeddings.
- **GraphRAG** uses a knowledge graph to understand relationships between pieces of information, answering complex questions that require synthesizing data from multiple sources.
- **Agentic RAG** goes beyond simple retrieval, using an intelligent agent to actively reason about, validate, reconcile, and refine external knowledge for more accurate and reliable answers.
- These advanced methods add complexity and latency but drastically improve the depth and trustworthiness of responses.
- Ultimately, RAG transforms LLMs from closed-book conversationalists into open-book reasoning tools; practical applications already span enterprise search, customer support, legal research, and personalized recommendations.

## References

1. Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* https://arxiv.org/abs/2005.11401
2. Google AI for Developers Documentation — *Retrieval Augmented Generation.* https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview
3. *Retrieval-Augmented Generation with Graphs (GraphRAG).* https://arxiv.org/abs/2501.00309
4. Leonie Monigatti, *"Retrieval-Augmented Generation (RAG): From Theory to LangChain Implementation."* https://medium.com/data-science/retrieval-augmented-generation-rag-from-theory-to-langchain-implementation-4e9bd5f6a4f2
5. Google Cloud Vertex AI RAG Corpus. https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/manage-your-rag-corpus#corpus-management
