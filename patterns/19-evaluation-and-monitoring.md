# Evaluation and Monitoring

> The continuous, often external, measurement of an agent's effectiveness, efficiency, and compliance — defining metrics, establishing feedback loops, and implementing reporting systems so that agent performance stays aligned with expectations in operational environments.

## Overview

This pattern examines the methodologies that let intelligent agents systematically assess their performance, monitor progress toward goals, and detect operational anomalies. Where goal setting and monitoring (Chapter 11) covers how an agent works toward and tracks its own objectives, and reasoning (Chapter 17) covers internal reasoning mechanisms, this chapter focuses on the continuous, frequently external measurement of an agent's effectiveness, efficiency, and compliance with requirements. That measurement spans defining metrics, establishing feedback loops, and building reporting systems that ensure agent performance aligns with expectations once the agent is operating in a real environment.

The motivation is rooted in the nature of agentic systems. Agents and LLMs operate in complex, dynamic environments where their performance can degrade over time. Because they are probabilistic and non-deterministic, traditional software testing — which yields predictable pass/fail results — is insufficient for ensuring reliability. Problems such as data drift, unexpected interactions, faulty tool calling, and deviations from intended goals can all arise after deployment. Continuous assessment is therefore necessary to measure an agent's effectiveness, efficiency, and adherence to operational and safety requirements.

The chapter is candid that building a comprehensive evaluation framework for AI agents is genuinely hard — comparable in complexity to an academic discipline or a substantial publication — because of the multitude of factors involved: model performance, user interaction, ethical implications, and broader societal impact. For practical purposes, though, the focus can be narrowed to a handful of critical use cases that matter most to the efficient and effective functioning of agents.

## How It Works

The pattern layers several complementary evaluation and monitoring techniques, ranging from simple objective metrics to sophisticated qualitative judgments and trajectory analysis.

**Agent response assessment.** The core process is evaluating the quality and accuracy of an agent's outputs — determining whether the agent delivers pertinent, correct, logical, unbiased, and accurate information in response to a given input. Assessment metrics may include factual correctness, fluency, grammatical precision, and adherence to the user's intended purpose.

A naive approach is a simple exact-match check: comparing the agent's output against an expected ("ground truth") output after normalizing whitespace and case, scoring 1.0 for an exact match and 0.0 otherwise. The chapter uses this deliberately to expose its weakness. Given the response "The capital of France is Paris." and the ground truth "Paris is the capital of France." — two sentences that convey identical meaning — a strict character-for-character comparison returns 0.0, incorrectly marking a correct answer as wrong. The lesson is that straightforward string comparison cannot assess semantic similarity; it succeeds only when the response exactly matches the expected output. Thorough real-world evaluation therefore demands more advanced NLP techniques that discern meaning between sentences. More sophisticated metrics include:

- **String similarity measures** such as Levenshtein distance and Jaccard similarity.
- **Keyword analysis** for the presence or absence of specific keywords.
- **Semantic similarity** using cosine similarity over embeddings produced by embedding models.
- **LLM-as-a-Judge evaluations** for assessing nuanced correctness and helpfulness (detailed below).
- **RAG-specific metrics** such as faithfulness and relevance.

**Latency monitoring.** In applications where the speed of an agent's response or action is a critical factor, latency monitoring measures the duration required for an agent to process requests and generate outputs. Elevated latency degrades user experience and the agent's overall effectiveness, especially in real-time or interactive settings. The chapter stresses that simply printing latency data to the console is insufficient for practical use — this information should be logged to persistent storage. Recommended destinations include structured log files (e.g., JSON), time-series databases (e.g., InfluxDB, Prometheus), data warehouses (e.g., Snowflake, BigQuery, PostgreSQL), and observability platforms (e.g., Datadog, Splunk, Grafana Cloud).

**Token usage tracking.** For LLM-powered agents, tracking token usage is crucial for managing cost and optimizing resource allocation, because billing typically depends on the number of tokens processed (both input and output). Efficient token usage directly reduces operational expense, and monitoring token counts also helps identify opportunities to improve prompt engineering or response generation. The chapter describes a conceptual monitor that maintains running counters for cumulative input and output tokens: each interaction records the tokens used for that prompt and response, accumulating totals that can be queried at any point. The illustrative version approximates counts by splitting text on whitespace, but a real implementation would use the specific LLM API's tokenizer for precise counts.

**LLM-as-a-Judge for subjective qualities.** Evaluating subjective qualities like an agent's "helpfulness" presents challenges that objective metrics cannot meet. The LLM-as-a-Judge approach uses an LLM as an evaluator that assesses another agent's output against predefined criteria. By leveraging the advanced linguistic capabilities of LLMs, this method produces nuanced, human-like evaluations of subjective qualities, surpassing simple keyword matching or rule-based assessments. The chapter frames it as a promising and still-developing technique for automating and scaling qualitative evaluation.

The worked example is a "judge" that evaluates the quality of legal survey questions. The judge is given a detailed rubric (its persona being an expert legal survey methodologist and critical legal reviewer) instructing it to score a question from 1 to 5 across five criteria, each with anchored descriptions:

1. **Clarity & precision** — from extremely vague/ambiguous (1) to perfectly clear, unambiguous, and precise in terminology and intent (5).
2. **Neutrality & bias** — from highly leading/biased (1) to completely neutral, objective, and free of loaded terms (5).
3. **Relevance & focus** — from irrelevant/out of scope (1) to directly relevant and well-focused on a single concept (5).
4. **Completeness** — from omitting critical information (1) to providing all necessary context (5).
5. **Appropriateness for audience** — from inaccessible jargon or oversimplification (1) to perfectly tailored to the audience's assumed knowledge (5).

The rubric also dictates a structured (JSON) output containing an overall score, a concise rationale of major strengths and weaknesses, detailed per-criterion feedback with specific suggested improvements, a list of any legal/ethical/methodological concerns, and a recommended action (e.g., "Revise for neutrality," "Approve as is," "Clarify scope"). The judge is run at a low generation temperature to keep evaluation deterministic, and is demonstrated against a strong question, a clearly biased/leading one, and a vague one — illustrating how the LLM grades each against the criteria. The example also handles practical failure modes such as the response being blocked by content moderation (an empty response with safety ratings) or the output failing to parse as valid structured data.

**Comparing the evaluation methods.** The chapter weighs three families of evaluation against their strengths and weaknesses:

- **Human evaluation** — captures subtle behavior and subjective human factors, but is difficult to scale, expensive, and time-consuming.
- **LLM-as-a-Judge** — consistent, efficient, and scalable, but may overlook intermediate steps and is limited by the underlying LLM's own capabilities.
- **Automated metrics** — scalable, efficient, and objective, but potentially limited in capturing an agent's complete capabilities.

**Evaluating agent trajectories and tool use.** Because traditional software tests are insufficient for probabilistic agents, evaluation must assess not just the final output but also the agent's *trajectory* — the sequence of steps taken to reach a solution. This means examining the quality of decisions, the reasoning process, and the overall outcome; automated trajectory evaluation becomes especially valuable for development beyond the prototype stage. Trajectory and tool-use analysis evaluates the steps an agent employs to achieve a goal: tool selection, strategies, and task efficiency. For example, an agent answering a customer's product query might ideally follow a trajectory of intent determination → database search tool use → result review → report generation. The agent's actual actions are compared against this expected, ground-truth trajectory to surface errors and inefficiencies.

Comparison methods for trajectories include:

- **Exact match** — requires a perfect match to the ideal sequence.
- **In-order match** — the correct actions appear in the correct order, but extra steps are allowed.
- **Any-order match** — the correct actions appear in any order, with extra steps allowed.
- **Precision** — measures the relevance of the predicted actions.
- **Recall** — measures how many of the essential actions are captured.
- **Single-tool use** — checks for the presence of one specific action.

Metric selection depends on the agent's requirements: high-stakes scenarios may demand an exact match, while more flexible situations may accept an in-order or any-order match.

**Test files vs. evalset files.** Evaluation can be organized using two complementary artifact types:

- **Test files** (in JSON format) each represent a single, simple agent-model interaction or session and are ideal for unit testing during active development, prioritizing rapid execution and simple session complexity. A test file holds one session with multiple turns, where each turn is a user-agent interaction capturing the user's query, the expected tool-use trajectory, intermediate agent responses, and the final response. For instance, a test file might encode a request to "Turn off device_2 in the Bedroom," specifying the agent's use of a `set_device_info` tool with parameters (location: Bedroom, device_id: device_2, status: OFF) and an expected final response confirming the device was turned off. Test files can be organized into folders and may include a configuration file (e.g., `test_config.json`) that defines evaluation criteria.
- **Evalset files** use a dataset called an "evalset" to evaluate interactions and contain multiple, potentially lengthy sessions suited to simulating complex, multi-turn conversations and integration tests. An evalset comprises multiple "evals," each a distinct session with one or more turns that include user queries, expected tool use, intermediate responses, and a reference final response. An example evalset session might have the user first ask "What can you do?" and then issue a compound request to roll a ten-sided die twice and check whether a number is prime — defining the expected dice-roll tool calls and prime-check tool call along with a final response summarizing the results.

**Evaluating multi-agent systems.** Assessing a complex system of multiple agents is much like evaluating a team project. Multi-agent systems are challenging to evaluate because they are constantly in flux, and the environments themselves are not static — so evaluation methods, including test cases, must adapt over time. Sophisticated metrics are needed that go beyond individual performance to measure the effectiveness of communication and teamwork. The complexity is also an advantage: the many steps and handoffs let you check the quality of work at each stage as well as the system as a whole. The chapter poses key diagnostic questions, each with a concrete travel-planning illustration:

- **Are the agents cooperating effectively?** After a Flight-Booking Agent secures a flight, does it correctly pass the dates and destination to the Hotel-Booking Agent? A cooperation failure could book a hotel for the wrong week.
- **Did they create a good plan and stick to it?** If the plan is to book a flight before a hotel, does the Hotel Agent improperly try to book a room before the flight is confirmed? You also check whether an agent gets stuck — for example, endlessly searching for a "perfect" rental car and never moving on.
- **Is the right agent chosen for the right task?** A weather question should route to a specialized Weather Agent with live data, not a General Knowledge Agent that returns a generic answer like "it's usually warm in summer."
- **Does adding more agents improve performance?** Adding a Restaurant-Reservation Agent should make trip planning better and more efficient — not create conflicts and slow the system down, which would signal a scalability problem.

**Google's ADK as a concrete framework.** As an example of tooling that supports evaluation, the chapter describes Google's Agent Development Kit (ADK), which offers three methods:

- A **web-based UI** (`adk web`) for interactive evaluation and dataset generation — enabling interactive session creation, saving sessions into existing or new eval sets, and displaying evaluation status.
- **Programmatic integration** using `pytest`, which incorporates evaluation into testing pipelines by running test files as part of integration tests (via ADK's agent-evaluator entry point), specifying the agent module and test file path.
- A **command-line interface** (`adk eval`) for automated evaluations suited to regular build, generation, and verification processes. It takes the agent module path and the evalset file, with options to specify a configuration file or print detailed results; specific evals within a larger evalset can be selected by listing them (comma-separated) after the evalset filename.

## Practical Applications & Use Cases

- **Performance tracking in live systems.** Continuously monitoring the accuracy, latency, and resource consumption of an agent deployed in production — for example, a customer-service chatbot's resolution rate and response time.
- **A/B testing for agent improvements.** Systematically comparing the performance of different agent versions or strategies in parallel to identify optimal approaches — e.g., trying two different planning algorithms for a logistics agent.
- **Compliance and safety audits.** Generating automated audit reports that track an agent's compliance with ethical guidelines, regulatory requirements, and safety protocols over time. These reports can be verified by a human-in-the-loop or by another agent, and can generate KPIs or trigger alerts when issues are identified.
- **Enterprise systems.** To govern agentic AI in corporate systems, a new control instrument — the AI "Contract" — is needed: a dynamic agreement that codifies the objectives, rules, and controls for AI-delegated tasks.
- **Drift detection.** Monitoring the relevance or accuracy of an agent's outputs over time, detecting when performance degrades because of changes in the input data distribution (concept drift) or environmental shifts.
- **Anomaly detection in agent behavior.** Identifying unusual or unexpected actions that might indicate an error, a malicious attack, or an emergent undesired behavior.
- **Learning progress assessment.** For agents designed to learn, tracking their learning curve, improvement in specific skills, or generalization across different tasks or datasets.

## Trade-offs & When to Use

**Why use it.** A standardized evaluation and monitoring framework provides a systematic way to assess and ensure the ongoing performance of intelligent agents. It involves defining clear metrics for accuracy, latency, and resource consumption (such as token usage for LLMs); applying advanced techniques like trajectory analysis to understand the reasoning process; and employing LLM-as-a-Judge for nuanced, qualitative assessments. By establishing feedback loops and reporting systems, the framework enables continuous improvement, A/B testing, and the detection of anomalies or performance drift — keeping the agent aligned with its objectives.

**Rule of thumb.** Use this pattern when:

- Deploying agents in live, production environments where real-time performance and reliability are critical.
- You need to systematically compare different versions of an agent or its underlying models to drive improvements.
- Operating in regulated or high-stakes domains that require compliance, safety, and ethical audits.
- An agent's performance may degrade over time due to data or environmental changes (drift).
- You need to evaluate complex agentic behavior — including the sequence of actions (trajectory) and the quality of subjective outputs such as helpfulness.

**Choosing among methods.** The three evaluation families trade off coverage against cost and scale. Human evaluation captures the subtlest behavior but does not scale; automated metrics scale and are objective but may miss the full picture; LLM-as-a-Judge sits in between, scalable and consistent but bounded by the judging model's own capability and prone to overlooking intermediate steps. A mature framework typically combines them rather than relying on one.

## Pitfalls

- **Exact-match comparison misses semantic equivalence.** A character-for-character string comparison will mark a correct, paraphrased answer as wrong; semantic similarity (via embeddings or an LLM judge) is needed for meaning-level correctness.
- **Console output is not monitoring.** Printing latency or token data to the console is insufficient in production; metrics must be logged to persistent, queryable storage (log files, time-series databases, warehouses, or observability platforms).
- **Approximate token counting misleads cost analysis.** Splitting text on whitespace only approximates token counts; precise cost and optimization decisions require the actual LLM tokenizer.
- **LLM judges have blind spots.** They may overlook intermediate steps and are limited by the judging model's own capabilities; they can also return blocked or unparseable responses that the evaluation harness must handle gracefully.
- **Static evaluation goes stale.** Because agents and their environments constantly change, test cases and evaluation methods must adapt over time, or they will stop reflecting real behavior.
- **Single performance metrics hide multi-agent failures.** Measuring individual agents alone can miss breakdowns in cooperation, planning adherence, task routing, and scalability that only surface at the system level.

## From Agents to Advanced Contractors

The chapter closes its conceptual arc by describing a proposed evolution (from the *Agent Companion* whitepaper, Gulli et al.) from simple AI agents toward advanced "contractors" — a shift from probabilistic, often unreliable systems to more deterministic and accountable ones designed for complex, high-stakes environments. Today's common agents operate on brief, underspecified instructions, which makes them fine for demos but brittle in production, where ambiguity leads to failure. The contractor model establishes a rigorous, formalized relationship between the user and the AI, built on clearly defined and mutually agreed-upon terms — much like a legal service agreement. It rests on four pillars:

1. **The Formalized Contract.** A detailed specification that is the single source of truth for a task, going far beyond a simple prompt. Rather than "analyze last quarter's sales," a contract would demand, for example, "a 20-page PDF report analyzing European market sales from Q1 2025, including five specific data visualizations, a comparative analysis against Q1 2024, and a risk assessment based on the included dataset of supply-chain disruptions." It explicitly defines deliverables, precise specifications, acceptable data sources, scope of work, and even expected computational cost and completion time — making the outcome objectively verifiable.
2. **A Dynamic Lifecycle of Negotiation and Feedback.** The contract is the start of a dialogue, not a static command. The contractor agent can analyze the terms and negotiate — for instance, if a required proprietary data source is inaccessible, it can ask for credentials or propose an alternative public database while flagging that granularity may change. This negotiation phase, which also lets the agent flag ambiguities or risks, resolves misunderstandings before execution begins, preventing costly failures and ensuring the output matches the user's actual intent.
3. **Quality-Focused Iterative Execution.** Unlike agents tuned for low-latency responses, a contractor prioritizes correctness and quality through self-validation and correction. For a code-generation contract, it would generate multiple algorithmic approaches, compile and run them against a suite of unit tests defined in the contract, score each on metrics like performance, security, and readability, and submit only the version that passes all validation. This internal loop of generating, reviewing, and improving its own work until specifications are met is crucial for building trust.
4. **Hierarchical Decomposition via Subcontracts.** For highly complex tasks, a primary contractor agent can act as a project manager, breaking the main goal into smaller sub-tasks expressed as new formal "subcontracts." A master contract to "build an e-commerce mobile application" could decompose into subcontracts for UI/UX design, a user-authentication module, a product database schema, and payment-gateway integration — each a complete, independent contract with its own deliverables, assignable to specialized agents. This structured decomposition lets the system tackle immense, multifaceted projects in an organized, scalable way.

Together these pillars reimagine AI interaction by embedding formal specification, negotiation, and verifiable execution directly into the agent's core logic — elevating AI from an unpredictable assistant into a dependable system that can autonomously manage complex projects with auditable precision, paving the way for deployment in mission-critical domains where trust and accountability are paramount.

## Relationships to Other Patterns

- **Goal Setting and Monitoring (Ch. 11).** That pattern covers how an agent tracks progress toward its own goals; this pattern provides the external, continuous measurement of whether the agent actually performs effectively, efficiently, and compliantly over time.
- **Reasoning (Ch. 17).** Trajectory evaluation assesses the quality of the agent's reasoning process and decisions, not just its final answer.
- **Reflection / Self-Correction.** The contractor model's "quality-focused iterative execution" — generate, self-validate against tests, score, and resubmit only passing work — is a self-correction loop driven by explicit acceptance criteria.
- **Tool Use.** Trajectory and tool-use analysis evaluates tool selection and efficiency, and test/evalset files encode expected tool-call trajectories as part of the ground truth.
- **Multi-Agent Collaboration.** Evaluating multi-agent systems requires metrics for cooperation, planning adherence, correct agent routing, and scalability; the contractor model's subcontract decomposition assigns formal subcontracts to specialized agents.
- **Human-in-the-Loop.** Human evaluation captures subtle, subjective behavior, and compliance/safety audit reports can be verified by a human reviewer (or another agent).

## Key Takeaways

- Evaluating intelligent agents goes beyond traditional tests to continuously measure their effectiveness, efficiency, and adherence to requirements in real-world environments.
- Practical applications include performance tracking in live systems, A/B testing for improvements, compliance audits, and detecting drift or anomalies in behavior.
- Basic evaluation assesses response accuracy, but real-world scenarios demand more sophisticated metrics like latency monitoring and token-usage tracking for LLM-powered agents.
- Agent trajectories — the sequence of steps an agent takes — are crucial for evaluation, comparing actual actions against an ideal, ground-truth path to identify errors and inefficiencies, using comparison methods such as exact, in-order, and any-order match plus precision and recall.
- Three evaluation families trade off against each other: human evaluation (captures subtlety, doesn't scale), LLM-as-a-Judge (scalable and consistent, but limited by the judge model), and automated metrics (scalable and objective, but may miss full capability).
- Frameworks like Google's ADK provide structured evaluation through individual test files (unit testing) and comprehensive evalset files (integration testing), both defining expected agent behavior, and runnable via a web UI, programmatically with `pytest` for CI/CD, or via a command-line interface for automated workflows.
- To make AI reliable for complex, high-stakes tasks, the paradigm shifts from simple prompts to formal "contracts" that precisely define verifiable deliverables and scope, allowing agents to negotiate, clarify ambiguities, and iteratively validate their own work — transforming them from unpredictable tools into accountable, trustworthy systems.

## References

1. ADK Web. https://github.com/google/adk-web
2. ADK Evaluate. https://google.github.io/adk-docs/evaluate/
3. Survey on Evaluation of LLM-based Agents. https://arxiv.org/abs/2503.16416
4. Agent-as-a-Judge: Evaluate Agents with Agents. https://arxiv.org/abs/2410.10934
5. Agent Companion, Gulli et al. https://www.kaggle.com/whitepaper-agent-companion
