# Advanced Prompting Techniques

> A catalogue of prompting methods — from zero-shot through Chain of Thought, ReAct, and automatic prompt engineering — that turn a general-purpose language model into a reliable, controllable component of an agentic system.

## Overview

Prompting is the primary interface for interacting with language models: the process of crafting inputs that guide the model toward a desired output. It involves structuring requests, providing relevant context, specifying the output format, and demonstrating expected response types. Well-designed prompts maximize a model's potential, producing accurate, relevant, and creative responses; poorly designed prompts lead to ambiguous, irrelevant, or erroneous output.

The objective of **prompt engineering** is to consistently elicit high-quality responses. This requires understanding the capabilities and limitations of the models and effectively communicating intended goals — developing expertise in instructing the AI. This appendix details techniques beyond basic interaction: methodologies for structuring complex requests, enhancing reasoning, controlling output formats, and integrating external information. They apply across a range of applications, from simple chatbots to complex multi-agent systems, and directly improve the performance and reliability of agentic applications, whose efficacy depends on their ability to interact meaningfully with language models.

### Core Principles for Effective Prompting

Several fundamental principles underlie all the techniques that follow, applicable across models and task complexities:

- **Clarity and Specificity.** Instructions should be unambiguous and precise. Models interpret patterns, and multiple interpretations lead to unintended responses. Define the task, the desired output format, and any limitations or requirements. Avoid vague language and unstated assumptions — inadequate prompts yield ambiguous, inaccurate output.
- **Conciseness.** Specificity should not compromise directness. Unnecessary wording or complex sentence structures can confuse the model or obscure the primary instruction. A useful heuristic: what is confusing to a human reader is likely confusing to the model. Use direct phrasing and active verbs.
- **Using Verbs.** Verb choice is a key prompting tool — action verbs signal the expected operation. "Summarize the following text" outperforms "Think about summarizing this," because precise verbs activate the relevant training data and processes. Effective verbs include *Act, Analyze, Categorize, Classify, Compare, Contrast, Create, Define, Describe, Evaluate, Extract, Find, Generate, Identify, List, Measure, Organize, Parse, Pick, Predict, Provide, Rank, Recommend, Return, Retrieve, Rewrite, Select, Show, Sort, Summarize, Translate, Write*.
- **Instructions Over Constraints.** Positive instructions (what to do) are generally more effective than negative constraints (what not to do). Constraints have their place for safety or strict formatting, but excessive reliance makes the model focus on avoidance rather than the objective. Positive framing aligns with human guidance preferences and reduces confusion.
- **Experimentation and Iteration.** Prompt engineering is iterative. Begin with a draft, test it, analyze the output, identify shortcomings, and refine. Model variations, configuration changes (temperature, top-p), and slight phrasing changes all yield different results, so documenting attempts is vital for learning and improvement.

## Techniques

### Zero-Shot Prompting

The most basic form of prompting: the model is given an instruction and input data **without any examples** of the desired input-output pair. It relies entirely on pre-training to understand the task and generate a relevant response — essentially a task description plus the initial text. **When to use:** tasks the model has likely encountered extensively during training — simple question answering, text completion, or basic summarization of straightforward text. It is the quickest approach to try first (e.g., "Translate the following English sentence to French: 'Hello, how are you?'").

### One-Shot Prompting

Provides the model with a **single example** of an input and its corresponding desired output before presenting the actual task. The example serves as a demonstration illustrating the pattern the model is expected to replicate, giving it a concrete template. **When to use:** when the desired output format or style is specific or less common. It can improve performance over zero-shot for tasks requiring a particular structure or tone.

### Few-Shot Prompting

Enhances one-shot prompting by supplying **several examples** — typically three to five — of input-output pairs, demonstrating a clearer pattern and improving the likelihood the model replicates it on new inputs. **When to use:** when the output must adhere to a specific format, style, or nuanced variation; it excels at classification, data extraction with specific schemas, or generating text in a particular style, especially where zero- or one-shot results are inconsistent. Three to five examples is a rule of thumb, adjusted to task complexity and model token limits. Key considerations:

- **Example quality and diversity.** Effectiveness relies heavily on examples being accurate, representative of the task, and covering potential variations or edge cases. Even a small mistake in an example can confuse the model; diverse examples help it generalize to unseen inputs.
- **Mix up classes in classification tasks.** When few-shot prompting for classification, mix the order of examples from different classes. This prevents the model from overfitting to the specific sequence and ensures it learns each class's key features independently, yielding more robust, generalizable performance.
- **Evolution to "many-shot" learning.** As modern long-context models grow stronger, they become highly effective at "many-shot" learning — optimal performance on complex tasks can now come from including a much larger number of examples (sometimes hundreds) directly in the prompt, letting the model learn more intricate patterns.

### System Prompting

Sets the **overall context and purpose** for a model, defining its intended behavior for an interaction or session. Unlike specific user queries, a system prompt provides foundational guidelines — establishing rules, a persona, or overall behavior — that influence the model's tone, style, and general approach throughout the interaction (e.g., "You are a helpful and harmless AI assistant. Respond to all queries in a polite and informative manner."). System prompts are also used for **safety and toxicity control** by including guidelines such as maintaining respectful language. To maximize effectiveness, system prompts can undergo automatic optimization through LLM-based iterative refinement; services such as the Vertex AI Prompt Optimizer systematically improve prompts based on user-defined metrics and target data.

### Role Prompting

Assigns a specific **character, persona, or identity** to the model, often in conjunction with system or contextual prompting. The model is instructed to adopt the knowledge, tone, and communication style associated with a role — e.g., "Act as a travel guide" or "You are an expert data analyst." Defining a role provides a framework for the tone, style, and focused expertise, enhancing the quality and relevance of output. The desired style within the role can also be specified (for instance, "a humorous and inspirational style").

### Using Delimiters

Effective prompting requires clear distinction of instructions, context, examples, and input. **Delimiters** — such as triple backticks (` ``` `), XML-style tags (`<instruction>`, `<context>`), or markers (`---`) — visually and programmatically separate these sections. Widely used in prompt engineering, this practice minimizes misinterpretation by the model, ensuring clarity about the role of each part of the prompt (e.g., wrapping an article to be summarized in `<article>...</article>` tags so the model knows which text is the instruction and which is the content).

### Contextual Engineering

Unlike static system prompts, **context engineering** dynamically provides background information crucial to a task or conversation. This ever-changing information helps models grasp nuances, recall past interactions, and integrate relevant details, leading to grounded responses and smoother exchanges. Examples include previous dialogue, relevant documents (as in Retrieval Augmented Generation), or specific operational parameters — e.g., asking for three family-friendly activities in Tokyo while leveraging the existing conversational context of a Japan trip. In agentic systems it is fundamental to core behaviors like memory persistence, decision-making, and coordination across sub-tasks, enabling agents to sustain goals over time, adapt strategies, and collaborate.

The core methodology posits that output quality depends more on the **richness of the provided context** than on the model's architecture. It is a significant evolution from traditional prompt engineering (which focused on optimizing the phrasing of immediate queries), expanding scope to multiple layers of information:

- **System prompts** — foundational instructions defining operational parameters (e.g., "You are a technical writer; your tone must be formal and precise").
- **External data** — *retrieved documents* actively fetched from a knowledge base to inform responses, and *tool outputs* (results from calling an external API for real-time data, such as querying a calendar for availability).
- **Implicit data** — critical information such as user identity, interaction history, and environmental state. Incorporating implicit context raises privacy and ethical data-management challenges, so robust governance is essential, especially in enterprise, healthcare, and finance.

The principle is that even advanced models underperform with a limited or poorly constructed view of their operational environment. The practice reframes the task from merely *answering a question* to *building a comprehensive operational picture* for the agent — for example, integrating a user's calendar availability (tool output), the professional relationship with an email recipient (implicit data), and notes from previous meetings (retrieved documents) before responding. The "engineering" aspect involves building robust pipelines to fetch and transform this data at runtime and establishing feedback loops to continually improve context quality. Specialized tuning systems (such as Google's Vertex AI prompt optimizer) can automate this improvement at scale by evaluating responses against sample inputs and predefined metrics, adapting prompts across models without extensive manual rewriting. Ultimately, context engineering transforms stateless chatbots into highly capable, situationally-aware systems.

### Structured Output

Often the goal is not free-form text but information in a specific, **machine-readable format** — JSON, XML, CSV, or Markdown tables. By explicitly requesting a particular format and potentially providing a schema or example of the desired structure, you guide the model to organize its response so it can be easily parsed and used by other parts of an agentic system. Returning JSON objects for data extraction is beneficial because it forces the model to create a structure and can limit hallucinations. Experimenting with output formats is recommended, especially for non-creative tasks like extracting or categorizing data. Structured output is crucial for pipelines where one model's output is the input to a subsequent processing step.

A powerful complementary technique is to use the model's generated data to **populate validated objects** (the appendix illustrates this with Python's Pydantic library, which validates data using type annotations). Defining a schema creates a clear, enforceable contract — effectively an object-oriented facade over the prompt's output — transforming raw or semi-structured text into validated, type-hinted objects. Parsing and validation can happen in a single step, with errors surfaced when the output is malformed or mismatched. XML can be converted to a dictionary and mapped onto the same schema using field aliases. This methodology ("parse, don't validate" at component boundaries) ensures interoperability: an encapsulated, validated object can be reliably passed to other functions, APIs, or pipelines with assurance that the data conforms to expected structure and types, leading to more robust and maintainable applications.

### Chain of Thought (CoT)

A powerful method for improving reasoning by explicitly prompting the model to generate **intermediate reasoning steps before arriving at a final answer** — instructing it to "think step by step." This mirrors how a human breaks a problem into smaller, manageable parts worked through sequentially. CoT helps produce more accurate answers, particularly for tasks requiring calculation or logical deduction where models might otherwise struggle, because generating intermediate steps keeps the model on track. Two main variations:

- **Zero-Shot CoT.** Simply add a phrase like "Let's think step by step" to the prompt, without providing any reasoning examples. For many tasks this simple addition significantly improves performance by triggering the model's ability to expose its internal reasoning trace.
- **Few-Shot CoT.** Combines CoT with few-shot prompting — examples show the input, the step-by-step reasoning, and the final output, giving the model a clearer template for performing and structuring its reasoning. This often produces even better results on complex tasks than zero-shot CoT.

**Advantages:** low-effort to implement, effective with off-the-shelf models without fine-tuning, and increases *interpretability* (you can see the reasoning steps, aiding understanding and debugging). It also improves prompt *robustness* across model versions, so performance is less likely to degrade on updates. **Disadvantage:** generating reasoning increases output length and token usage, raising cost and response time. **Best practices:** present the final answer *after* the reasoning (the reasoning influences the subsequent token predictions for the answer); and for tasks with a single correct answer (e.g., math), set temperature to 0 (greedy decoding) for deterministic selection of the most probable next token.

### Self-Consistency

Builds on Chain of Thought to improve reliability by leveraging the probabilistic nature of models. Instead of a single greedy reasoning path, it **generates multiple diverse reasoning paths for the same problem and selects the most consistent answer** via three steps:

1. **Generate diverse reasoning paths.** Send the same (often CoT) prompt to the model multiple times, using a higher temperature to encourage varied step-by-step explanations and reasoning approaches.
2. **Extract the answer** from each generated reasoning path.
3. **Choose the most common answer** by majority vote across the paths.

This improves accuracy and coherence, particularly where multiple valid reasoning paths exist or where the model is error-prone in a single attempt, yielding a pseudo-probability that the answer is correct. **Cost:** it requires running the model multiple times per query, leading to much higher computation and expense. (A simple illustration: asking whether "All birds can fly" is true — different runs reason about most birds, about penguins/ostriches, etc.; the final answer is the majority vote, though a more sophisticated approach would weigh reasoning quality.)

### Step-Back Prompting

Enhances reasoning by **first asking the model to consider a general principle or concept** related to the task before addressing specific details; the response to the broader question is then used as context for solving the original problem. This activates relevant background knowledge and wider reasoning strategies. By focusing on underlying principles or higher-level abstractions, the model generates more accurate, insightful answers, less influenced by superficial elements — and it can provide a stronger basis for specific creative outputs. Step-back prompting encourages critical thinking and can mitigate biases by emphasizing general principles. (Example: first ask "What are the key factors that make a good detective story?", then use that response as context to write a plot summary for a new mystery novel.)

### Tree of Thoughts (ToT)

An advanced reasoning technique that extends Chain of Thought by enabling the model to **explore multiple reasoning paths concurrently** rather than a single linear progression. It uses a tree structure where each node is a "thought" — a coherent language sequence acting as an intermediate step — and from each node the model can branch out to explore alternative reasoning routes. ToT is particularly suited to complex problems requiring **exploration, backtracking, or evaluation of multiple possibilities** before reaching a solution. It is more computationally demanding and intricate to implement than linear CoT, but can achieve superior results on tasks needing deliberate, exploratory problem-solving, letting an agent consider diverse perspectives and recover from initial errors by investigating alternative branches. (Example: for "Develop three different possible endings for a story," ToT explores distinct narrative branches from a key turning point rather than one linear continuation.)

### Tool Use / Function Calling

A crucial agent ability: **calling external tools or functions** to perform actions beyond internal capabilities — web searches, database access, sending email, calculations, or interacting with external APIs. Effective prompting instructs the model on the appropriate timing and methodology for tool use. Modern models are often fine-tuned for "function calling": they interpret descriptions of available tools (purpose and parameters), determine whether a tool is needed, identify the appropriate one, and format the required arguments. Critically, **the model does not execute the tool directly** — it generates structured output (typically JSON) specifying the tool and parameters. The surrounding agentic system processes that output, executes the tool, and feeds the result back to the model, integrating it into the ongoing interaction. (Example: given a `get_current_weather` tool taking a `city` parameter, the model emits a structured call with `{"city": "London"}` rather than answering directly.)

### ReAct (Reason & Act)

Short for **Reason and Act**, a paradigm combining CoT-style reasoning with the ability to perform actions using tools in an **interleaved** manner — mimicking how humans reason verbally and take actions to gather information or make progress. The pattern is a loop:

1. **Thought** — the model generates a thought process explaining its current understanding and plan.
2. **Action** — based on the thought, it decides to act, often using a tool (Search, Calculator, API call), outputting the tool name and required input.
3. **Observation** — the agentic system executes the tool and provides the result back to the model.
4. The loop continues: the model generates a new Thought based on the latest Observation, leading to further Actions and Observations, until the task is complete and the model outputs a **Final Answer**.

This interleaving of thinking and acting lets the agent dynamically gather information, react to tool outputs, and refine its approach, making it especially effective for tasks requiring interaction with dynamic environments or external knowledge sources. (Illustrative trace: asked for the capital of France and its population, the model reasons it needs a search, searches "capital of France" → observes "Paris," reasons it now needs the population, searches again → observes the figure, then produces the final answer.)

### Automatic Prompt Engineering (APE)

Recognizing that crafting effective prompts is complex and iterative, APE uses **language models themselves to generate, evaluate, and refine prompts**, automating prompt writing and potentially improving performance without extensive human effort. The general idea: a "meta-model" or process takes a task description and generates multiple candidate prompts, which are evaluated by the quality of output they produce on a set of inputs (using metrics like BLEU or ROUGE, or human evaluation). The best-performing prompts are selected, optionally refined further, and used. (Example: a developer asks for "a prompt that extracts the date and sender from an email"; the APE system generates candidates, tests them on sample emails, and selects the one that consistently extracts correctly.)

A related, more systematic approach — notably promoted by the **DSPy framework** — treats prompts not as static text but as **programmatic modules that can be automatically optimized**, moving from manual trial-and-error to a data-driven methodology. It relies on two key components:

1. **A Goldset (high-quality dataset)** — a representative set of high-quality input-and-output pairs serving as the "ground truth" defining a successful response.
2. **An Objective Function (scoring metric)** — a function that automatically evaluates the model's output against the corresponding "golden" output, returning a quality/accuracy/correctness score.

An optimizer (such as a Bayesian optimizer) then systematically refines the prompt via two strategies, used independently or together:

- **Few-Shot Example Optimization.** Instead of a developer manually selecting examples, the optimizer programmatically samples different combinations of examples from the goldset and tests them to identify the set that most effectively guides the model.
- **Instructional Prompt Optimization.** The optimizer uses an LLM as a meta-model to iteratively mutate and rephrase the prompt's core instructions — adjusting wording, tone, or structure — to discover which phrasing yields the highest objective-function scores.

The goal of both is to maximize objective-function scores, effectively "training" the prompt to produce results closer to the goldset. Combined, they simultaneously optimize *what instructions to give* and *which examples to show*, yielding a machine-optimized prompt for the task.

### Iterative Prompting / Refinement

Start with a simple, basic prompt and **iteratively refine it based on the model's responses**. If output isn't quite right, analyze the shortcomings and modify the prompt to address them. Unlike the automated APE, this is a human-driven iterative design loop. (Example: a generic "Write a product description for a coffee maker" is progressively sharpened by adding the features to highlight, the product name, specific selling points like "brew a pot in under 2 minutes," and the target audience.)

### Providing Negative Examples

While "Instructions over Constraints" generally holds, there are situations where **negative examples** help — used carefully. A negative example shows the model an input paired with an undesired output, or output that should not be generated, clarifying boundaries or preventing specific incorrect responses. (Example: "Generate a list of popular tourist attractions in Paris. Do NOT include the Eiffel Tower," accompanied by an explicit "example of what NOT to do.")

### Using Analogies

Framing a task using an **analogy** can help the model understand the desired output or process by relating it to something familiar — particularly useful for creative tasks or explaining complex roles. (Example: "Act as a 'data chef' — take the raw ingredients (data points) and prepare a 'summary dish' (report) that highlights the key flavors (trends) for a business audience.")

### Factored Cognition / Decomposition

For very complex tasks, **break the overall goal into smaller, manageable sub-tasks** and prompt the model separately on each, then combine the results to achieve the final outcome. Related to prompt chaining and planning, it emphasizes deliberate problem decomposition. (Example: to write a research paper — first prompt for a detailed outline, then prompt to write the introduction from the outline, then each section in turn, then a final prompt to combine the sections and write a conclusion.)

### Retrieval Augmented Generation (RAG)

Enhances models by giving them access to **external, up-to-date, or domain-specific information during prompting**. When a user asks a question, the system first retrieves relevant documents or data from a knowledge base (a database, document set, or the web), then includes that retrieved information in the prompt as context, allowing the model to generate a response *grounded in external knowledge*. This mitigates hallucination and provides access to information the model wasn't trained on or that is very recent — a key pattern for agentic systems working with dynamic or proprietary information. (Example: a query about new features in the latest version of a software library triggers a documentation search, and the retrieved snippets are inserted into the prompt as the basis for the answer.)

### Persona Pattern (User Persona)

Whereas role prompting assigns a persona to the *model*, the Persona Pattern involves **describing the user or target audience** for the model's output. This helps the model tailor its response in language, complexity, tone, and the kind of information it provides. (Example: "You are explaining quantum physics. The target audience is a high school student with no prior knowledge. Explain it simply and use analogies they might understand.")

### Using Google Gems

Google's AI "Gems" are a user-configurable feature in which each Gem functions as a **specialized instance of the core model, tailored for specific, repeatable tasks**. A user creates a Gem by giving it explicit instructions that establish its operational parameters — designated purpose, response style, and knowledge domain — which the model consistently adheres to throughout a conversation. This enables highly specialized agents (e.g., a code interpreter that references only specific libraries; a data analyzer that summarizes without speculative commentary; a translator following a particular style guide). The effect is a **persistent, task-specific context**, so the user avoids re-establishing the same information with each query — reducing conversational redundancy and producing focused, consistently aligned output. It represents a shift from general-purpose interaction to specialized, pre-defined AI functionalities.

### Using LLMs to Refine Prompts (The Meta Approach)

A "meta" application where the model **assists in optimizing the instructions given to the model** — a form of AI-assisted improvement of human-AI interaction. In practice, you provide the model with an existing prompt you want to improve, the task it should accomplish, and perhaps examples of the current (unsatisfactory) output and why it falls short, then ask the model to analyze the prompt and suggest improvements. A capable model can flag ambiguity, lack of specificity, or inefficient phrasing, and suggest techniques such as adding delimiters, clarifying the output format, choosing a more effective persona, or including few-shot examples. **Benefits:** accelerated iteration; identification of blind spots (ambiguities you overlooked); a learning opportunity (seeing what makes prompts effective); and scalability (automating parts of optimization across many prompts). The model's suggestions are not always perfect and should be evaluated and tested like any manually engineered prompt, but they provide a powerful starting point.

### Code Prompting

Models trained on large code datasets are powerful assistants for developers. Common use cases:

- **Writing code** — generating snippets or functions from a description of desired functionality.
- **Explaining code** — providing a snippet and asking for a line-by-line or summary explanation.
- **Translating code** — converting code from one programming language to another.
- **Debugging and reviewing code** — providing code with an error or improvement opportunity and asking the model to identify issues, suggest fixes, or recommend refactoring.

Effective code prompting requires providing sufficient context, specifying the desired language and version, and being clear about the functionality or issue (e.g., supplying the code and traceback when asking about an error).

### Multimodal Prompting

As models move toward processing and generating information across modalities (text, images, audio, video), **multimodal prompting uses a combination of input formats** rather than text alone to guide the model. Examples: providing an image of a diagram with a text prompt asking the model to explain the process shown, or providing an image and asking the model to generate a descriptive caption (image input + text prompt → text output). As multimodal capabilities mature, prompting techniques will evolve to leverage these combined inputs and outputs.

## Best Practices

Skilled prompt engineering is iterative and improves with practice. Valuable practices worth emphasizing:

- **Provide examples.** One- or few-shot examples are among the most effective ways to guide the model.
- **Design with simplicity.** Keep prompts concise, clear, and easy to understand; avoid unnecessary jargon or overly complex phrasing.
- **Be specific about the output.** Clearly define the desired format, length, style, and content of the response.
- **Use instructions over constraints.** Tell the model what to do rather than what not to do.
- **Control the max token length.** Use model configurations or explicit instructions to manage output length.
- **Use variables in prompts.** For application prompts, use variables to keep them dynamic and reusable, avoiding hardcoded values.
- **Experiment with input formats and writing styles.** Try different phrasings (question, statement, instruction) and different tones or styles to see what works best.
- **For few-shot classification tasks, mix up the classes.** Randomize the order of examples from different categories to prevent overfitting.
- **Adapt to model updates.** Test existing prompts on new model versions and adjust to leverage new capabilities or maintain performance.
- **Experiment with output formats.** Especially for non-creative tasks, try requesting structured output like JSON or XML.
- **Experiment together with other prompt engineers.** Different perspectives lead to discovering more effective prompts.
- **Apply CoT best practices.** Place the answer after the reasoning, and set temperature to 0 for tasks with a single correct answer.
- **Document the various prompt attempts.** Keep a structured record of prompts, configurations, and results to track what works and why.
- **Save prompts in codebases.** Store prompts in separate, well-organized files for easier maintenance and version control.
- **Rely on automated tests and evaluation.** For production systems, implement automated tests and evaluation procedures to monitor prompt performance and ensure generalization to new data.

## Key Takeaways

- Prompting is a disciplined **engineering practice**, not a simple act of asking questions; its purpose is to transform general-purpose models into specialized, reliable, capable tools for specific tasks.
- The foundation is **core principles** — clarity, conciseness, action verbs, positive instructions, and iterative experimentation — which reduce natural-language ambiguity and steer probabilistic output toward a single correct intention.
- **Basic techniques** (zero-, one-, few-shot, and now many-shot) demonstrate expected behavior through examples, providing varying levels of contextual guidance that shape response style, tone, and format.
- **Structuring techniques** — system prompts, role assignment, delimiters, contextual engineering, and structured/validated output — provide the architectural layer for fine-grained control and reliable data passing between components.
- **Reasoning techniques** (Chain of Thought, Self-Consistency, Step-Back, Tree of Thoughts) compel the model to externalize its logic, breaking complex goals into manageable sub-tasks and improving accuracy on multi-step problems.
- **Action and interaction techniques** (Tool Use / Function Calling, ReAct) give an agent its "hands" — the ability to perceive and act upon its environment by calling tools and APIs.
- **Knowledge-integration techniques** (RAG, Context Engineering) act as the agent's "senses," grounding decisions in current, factual, external information and preventing operation in a vacuum of static training data.
- **Optimization techniques** (APE, DSPy-style programmatic optimization, iterative refinement, and the meta approach of using LLMs to refine prompts) reduce the manual burden of crafting effective prompts.
- For agentic systems, output **predictability is paramount**: requesting structured data (JSON) and validating it programmatically is a necessity, not a convenience — without it, an agent's internal components cannot communicate reliably, risking catastrophic workflow failures.
- Mastering this full spectrum is the definitive skill that elevates a generalist model from a simple text generator into a sophisticated agent capable of autonomous, aware, and intelligent task performance.

## References

1. Prompt Engineering — https://www.kaggle.com/whitepaper-prompt-engineering
2. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models — https://arxiv.org/abs/2201.11903
3. Self-Consistency Improves Chain of Thought Reasoning in Language Models — https://arxiv.org/pdf/2203.11171
4. ReAct: Synergizing Reasoning and Acting in Language Models — https://arxiv.org/abs/2210.03629
5. Tree of Thoughts: Deliberate Problem Solving with Large Language Models — https://arxiv.org/pdf/2305.10601
6. Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models — https://arxiv.org/abs/2310.06117
7. DSPy: Programming—not prompting—Foundation Models — https://github.com/stanfordnlp/dspy
