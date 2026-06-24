# Learning and Adaptation

> A pattern in which agents improve autonomously over time by changing their thinking, actions, or knowledge in response to new experiences, data, and environmental interaction, rather than remaining bound to predefined parameters.

## Overview

Learning and adaptation are pivotal for enhancing the capabilities of AI agents. These processes let agents evolve beyond predefined parameters, improving autonomously through experience and interaction with their environment. By learning and adapting, agents can effectively handle novel situations and optimize their performance without constant manual intervention.

The core distinction the chapter draws is between *learning* and *adaptation*:
- **Learning** is the underlying process of acquiring knowledge or skill from experience and data.
- **Adaptation** is the visible change in an agent's behavior, strategy, understanding, or goals that results from that learning.

Agents move from simply following instructions to becoming smarter over time. Adaptation is especially vital for agents operating in unpredictable, changing, or entirely new environments, where pre-programmed logic alone is insufficient and performance would otherwise degrade when confronted with situations not anticipated at design time.

## How It Works

The chapter surveys several learning mechanisms that agents can draw on, then dives into two reinforcement-learning-based alignment algorithms (PPO and DPO) and three real systems (SICA, AlphaEvolve, OpenEvolve).

### Categories of learning

- **Reinforcement Learning (RL):** The agent tries actions and receives rewards for positive outcomes and penalties for negative ones, learning optimal behaviors in changing situations. Well suited to agents controlling robots or playing games.
- **Supervised Learning:** The agent learns from labeled examples, mapping inputs to desired outputs. Enables decision-making and pattern recognition; ideal for agents sorting emails or predicting trends.
- **Unsupervised Learning:** The agent discovers hidden connections and patterns in unlabeled data, supporting insight generation, organization, and building a "mental map" of its environment. Useful for exploring data without specific guidance.
- **Few-Shot / Zero-Shot Learning with LLM-based agents (in-context learning):** Agents leveraging LLMs can rapidly adapt to new tasks given only minimal examples or clear instructions, enabling fast responses to new commands or situations without retraining.
- **Online Learning:** The agent continuously updates its knowledge as new data arrives. This is essential for real-time reactions and ongoing adaptation in dynamic environments, and is critical for agents processing continuous data streams.
- **Memory-Based Learning:** The agent recalls past experiences to adjust its current actions in similar situations, improving context awareness and decision quality. Effective for agents that have memory-recall capabilities.

### Proximal Policy Optimization (PPO)

PPO is a reinforcement learning algorithm used to train agents in environments with a continuous range of actions, such as controlling a robot's joints or a character in a game. Its goal is to reliably and stably improve an agent's decision-making strategy (its *policy*).

The core idea is to make small, careful updates to the policy, avoiding drastic changes that could cause performance to collapse. It proceeds in three conceptual steps:

1. **Collect data.** The agent interacts with its environment using its current policy and gathers a batch of experiences, each consisting of a state, an action, and a reward.
2. **Evaluate a "surrogate" goal.** PPO estimates how a candidate policy update would change the expected reward. Instead of simply maximizing this reward, it uses a special *clipped* objective function.
3. **Apply the clipping mechanism.** This is the key to PPO's stability. Clipping creates a "trust region" — a safe zone around the current policy — and prevents the algorithm from making an update that is too different from the current strategy. It acts as a safety brake so the agent doesn't take a huge, risky step that undoes its prior learning.

In short, PPO balances improving performance with staying close to a known, working strategy, preventing catastrophic failures during training and yielding more stable learning.

### Direct Preference Optimization (DPO)

DPO is a more recent method designed specifically for aligning LLMs with human preferences. It is a simpler, more direct alternative to using PPO for alignment.

To appreciate DPO, the chapter first describes the traditional **PPO-based alignment**, a two-step process:

1. **Train a reward model.** Human feedback is collected in which people rate or compare different LLM responses (e.g., "Response A is better than Response B"). This data trains a separate AI model — the *reward model* — whose job is to predict the score a human would give to any new response.
2. **Fine-tune with PPO.** The LLM is then fine-tuned with PPO so that it generates responses earning the highest possible score from the reward model. The reward model acts as the "judge" in the training game.

This two-step approach can be complex and unstable. A notable failure mode is *reward hacking*: the LLM may find a loophole and learn to exploit the reward model, earning high scores for genuinely bad responses.

**DPO's direct approach** skips the reward model entirely. Rather than translating human preferences into a reward score and then optimizing for that score, DPO uses the preference data directly to update the LLM's policy. It relies on a mathematical relationship that directly links preference data to the optimal policy. Conceptually, it teaches the model: "Increase the probability of generating responses like the preferred one, and decrease the probability of generating responses like the disfavored one."

By directly optimizing the language model on human preference data, DPO avoids the complexity and potential instability of training and using a separate reward model, making alignment more efficient and robust.

### Self-modification and evolutionary discovery

Beyond RL fine-tuning, the chapter highlights more advanced learning strategies in which agents change their own code or evolve solutions. These are illustrated through the SICA, AlphaEvolve, and OpenEvolve case studies (detailed below). The unifying idea is an iterative loop: generate candidate changes, evaluate them against benchmarks or scoring criteria, record results, and select the best version to seed the next iteration — enabling improvement without traditional retraining paradigms.

## Practical Applications & Use Cases

Adaptive agents perform better in variable environments because they update iteratively based on experiential data. Representative applications:

- **Personalized assistant agents** refine their interaction protocols through longitudinal analysis of individual user behavior, producing highly optimized responses.
- **Trading bot agents** dynamically adjust model parameters in response to high-resolution, real-time market data, aiming to maximize returns and mitigate risk.
- **Application agents** modify their user interface and functionality based on observed user behavior, increasing engagement and intuitiveness.
- **Robotic and autonomous vehicle agents** enhance navigation and response by integrating sensor data with historical action analysis, enabling safe, efficient operation across diverse conditions.
- **Fraud detection agents** improve anomaly detection by refining predictive models with newly identified fraudulent patterns, strengthening security and reducing losses.
- **Recommendation agents** improve content-selection precision via user-preference learning, delivering individualized, contextually relevant recommendations.
- **Game AI agents** dynamically adapt strategic algorithms to increase game complexity and challenge, boosting player engagement.
- **Knowledge Base Learning agents** use Retrieval Augmented Generation (RAG) to maintain a dynamic knowledge base of problem descriptions and proven solutions. By storing successful strategies and challenges encountered, an agent can reference this data during decision-making, applying previously successful patterns and avoiding known pitfalls.

### Case Study: The Self-Improving Coding Agent (SICA)

SICA, developed by Maxime Robeyns, Laurence Aitchison, and Martin Szummer, demonstrates an agent that modifies its own source code. This contrasts with traditional approaches where one agent trains another; SICA is simultaneously the *modifier* and the *modified entity*, iteratively refining its own codebase to improve performance across coding challenges.

**The self-improvement cycle:** SICA keeps an archive of its past versions and their benchmark performance. Each iteration, it (1) reviews the archive and selects the highest-performing version, scored by a weighted formula combining success, time taken, and computational cost; (2) has that version analyze the archive to identify potential improvements and then directly alter its own codebase; (3) tests the modified agent against benchmarks and records the results back into the archive. Repeating this loop lets SICA learn directly from past performance and evolve its capabilities without conventional training.

**What SICA evolved (illustrating real adaptation):**
- *Code editing.* It began with a basic file-overwriting approach, then developed a "Smart Editor" for more intelligent, contextual edits, which evolved into a "Diff-Enhanced Smart Editor" (using diffs for targeted, pattern-based edits) plus a "Quick Overwrite Tool" to reduce processing demands. It later added "Minimal Diff Output Optimization" and "Context-Sensitive Diff Minimization," using Abstract Syntax Tree (AST) parsing for efficiency, along with a "SmartEditor Input Normalizer."
- *Code navigation.* It independently created an "AST Symbol Locator" that uses the code's structural map (AST) to find definitions, then a "Hybrid Symbol Locator" combining quick search with AST checking, later refined as "Optimized AST Parsing in Hybrid Symbol Locator" to focus on relevant code sections and improve search speed.

**SICA's architecture:** A foundational toolkit handles basic file operations, command execution, and arithmetic, plus mechanisms for result submission. It invokes specialized **sub-agents** (coding, problem-solving, and reasoning agents), which the main agent calls much like tools. Sub-agents decompose complex tasks and help manage the LLM's context length, especially during extended improvement cycles.

An **asynchronous overseer** — a separate LLM running concurrently — monitors SICA's behavior for pathological patterns such as loops or stagnation. It receives a detailed textual report of the system's state, including a callgraph and an event stream of LLM messages, tool calls, and responses, allowing it to detect inefficient or repeated work. It can intervene by sending notifications or even cancelling the agent's execution.

**Context-window organization:** SICA's LLM structures its context window (its short-term memory) deliberately, which is crucial to operation. The structure includes a **System Prompt** (agent goals, tool and sub-agent documentation, system instructions), a **Core Prompt** (the problem statement or instruction, contents of open files, and a directory map), and **Assistant Messages** (the agent's step-by-step reasoning, records and results of tool/sub-agent calls, and overseer communications). File changes were initially recorded as diffs showing only modifications, periodically consolidated. Good organization improves information flow and reduces processing time and cost.

**Engineering and safety choices:** SICA is built with a modular architecture, is actively developed as a framework for post-training LLMs on tool use and agentic tasks, and emphasizes **Docker containerization** so the agent runs in an isolated container — a crucial safeguard given its ability to execute shell commands, mitigating risks like inadvertent host file-system manipulation. It provides observability via an interactive webpage that visualizes events on an event bus and the agent's callgraph, letting users inspect events, read overseer messages, and collapse sub-agent traces. The framework supports LLMs from multiple providers for experimentation.

**Open challenge:** A notable difficulty in the initial implementation was getting the LLM-based agent to independently propose modifications that were novel, innovative, feasible, and engaging in each meta-improvement iteration. Fostering genuine open-ended learning and authentic creativity in LLM agents remains an active research area.

### AlphaEvolve

AlphaEvolve is a Google AI agent designed to discover and optimize algorithms. It combines LLMs (specifically Gemini Flash and Pro models), automated evaluation systems, and an evolutionary algorithm framework, with the aim of advancing both theoretical mathematics and practical computing.

**How it works:** It uses an ensemble of Gemini models — Flash generates a wide range of initial algorithm proposals, while Pro provides deeper analysis and refinement. Proposed algorithms are automatically evaluated and scored against predefined criteria; this feedback drives iterative improvement toward optimized, novel algorithms.

**Practical-computing results inside Google:** improved data-center scheduling (a 0.7% reduction in global compute resource usage); hardware design contributions (suggested optimizations for Verilog code in upcoming TPUs); and AI performance acceleration, including a 23% speedup in a core kernel of the Gemini architecture and up to 32.5% optimization of low-level GPU instructions for FlashAttention.

**Fundamental-research results:** discovery of new matrix-multiplication algorithms, including a method for 4x4 complex-valued matrices using 48 scalar multiplications (surpassing previously known solutions). Across more than 50 open mathematical problems, it rediscovered existing state-of-the-art solutions in about 75% of cases and improved on existing solutions in about 20% of cases, including advances on the kissing-number problem.

### OpenEvolve

OpenEvolve is an open evolutionary coding agent that uses LLMs to iteratively optimize code. It orchestrates a pipeline of LLM-driven code generation, evaluation, and selection to continuously improve programs across many tasks. A key capability is that it can evolve **entire code files**, not just single functions. It is designed for versatility: it supports multiple programming languages, is compatible with OpenAI-compatible APIs for any LLM, incorporates multi-objective optimization, allows flexible prompt engineering, and supports distributed evaluation for complex challenges.

Its internal architecture is managed by a **controller** that orchestrates several components: a **program sampler**, a **Program Database**, an **Evaluator Pool**, and **LLM Ensembles**, working together to facilitate learning and adaptation that enhance code quality. In practice, a user initializes the system with paths to an initial program, an evaluation file, and a configuration file, then runs the evolutionary process for a set number of iterations (e.g., 1000) and inspects the metrics of the best program found.

## Trade-offs & When to Use

**The problem this pattern solves:** AI agents often operate in dynamic, unpredictable environments where pre-programmed logic is insufficient. Performance degrades on novel situations not anticipated at design time, and without learning, agents cannot optimize strategies or personalize interactions over time. This rigidity limits effectiveness and prevents true autonomy.

**Why the pattern helps:** Integrating learning and adaptation transforms static agents into dynamic, evolving systems that autonomously refine knowledge and behavior from new data and interactions. Methods range from reinforcement learning to advanced techniques like self-modification (SICA) and evolutionary discovery (AlphaEvolve). Continuous learning lets agents master new tasks, improve performance, and adapt to changing conditions without constant manual reprogramming.

**Rule of thumb:** Use this pattern when building agents that must operate in dynamic, uncertain, or evolving environments. It is essential for applications requiring personalization, continuous performance improvement, and the ability to handle novel situations autonomously.

**Costs and considerations:**
- Building agents that learn typically requires hooking them up with machine-learning tooling and carefully managing how data flows.
- PPO-based alignment is powerful but can be complex and unstable, and is vulnerable to reward hacking; DPO trades some of that machinery away for simplicity and robustness.
- Self-modifying agents that execute shell commands need strong isolation (e.g., Docker containerization) and observability/oversight (e.g., an asynchronous overseer) to stay safe and on track.
- For coordinated improvement in multi-agent systems, tuning data must accurately reflect the *complete interaction trajectory*, capturing the individual inputs and outputs of each participating agent.

## Pitfalls

- **Reward hacking:** In PPO-based alignment, the LLM may exploit loopholes in the reward model to earn high scores for genuinely bad responses.
- **Training instability / catastrophic collapse:** Large, unconstrained policy updates can undo prior learning — the motivation for PPO's clipped "trust region" and for DPO's reward-model-free approach.
- **Loops and stagnation in self-improving agents:** Without monitoring, a self-modifying agent can fall into repetitive or unproductive behavior; SICA addresses this with an asynchronous overseer that can detect inefficiency and intervene.
- **Limited open-ended creativity:** Prompting an LLM agent to reliably propose genuinely novel, feasible, and useful self-modifications each iteration is hard and remains an open research problem.
- **Safety of self-executing code:** An agent that can run shell commands and edit files risks inadvertent host damage; containerized isolation is a crucial mitigation.

## Relationships to Other Patterns

- **Memory Management:** Memory-based learning and SICA's structured context window (system prompt, core prompt, assistant messages) tie directly to memory patterns; the chapter references memory management as a foundational agentic component.
- **Knowledge Retrieval (RAG):** Knowledge-base learning agents use RAG to maintain a dynamic store of problems and proven solutions (the chapter points to its RAG chapter, Ch. 14).
- **Multi-Agent Collaboration:** SICA's specialized sub-agents (coding, problem-solving, reasoning) and AlphaEvolve's LLM ensembles show learning combined with multi-agent decomposition; the chapter notes learning principles are especially vital for coordinated improvement across multi-agent systems.
- **Planning and Tool Use:** Self-improving agents are built on top of basic coding/tool-use capabilities, and the framework is positioned for post-training LLMs on tool use.
- **Composability:** These patterns can be combined to construct sophisticated AI systems; AlphaEvolve is presented as an example of what such combinations make attainable.

## Key Takeaways

- Learning and adaptation are about agents getting better at their tasks and handling new situations by using their experiences.
- "Adaptation" is the visible change in an agent's behavior or knowledge that results from learning.
- SICA self-improves by modifying its own code based on past performance, which produced tools like the Smart Editor and AST Symbol Locator.
- Specialized sub-agents and an overseer help self-improving systems manage large tasks and stay on track.
- How an LLM's context window is structured (system prompts, core prompts, assistant messages) is critical to how efficiently agents operate.
- This pattern is vital for agents operating in environments that are always changing, uncertain, or that require personalization.
- Building learning agents often means integrating machine-learning tooling and managing data flow.
- An agent equipped with basic coding tools can autonomously edit itself and thereby improve its benchmark performance.
- AlphaEvolve is Google's AI agent that leverages LLMs and an evolutionary framework to autonomously discover and optimize algorithms, advancing both fundamental research and practical computing.
- PPO stabilizes RL training via clipped, trust-region updates; DPO simplifies LLM alignment by optimizing directly on preference data without a separate reward model.
- Autonomous algorithmic discovery and optimization by AI agents (as in AlphaEvolve) is demonstrably attainable.

## References

1. Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. MIT Press.
2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
3. Mitchell, T. M. (1997). *Machine Learning*. McGraw-Hill.
4. Schulman, J., Wolski, F., Dhariwal, P., Radford, A., & Klimov, O. *Proximal Policy Optimization Algorithms*. arXiv:1707.06347 — https://arxiv.org/abs/1707.06347
5. Robeyns, M., Aitchison, L., & Szummer, M. (2025). *A Self-Improving Coding Agent*. arXiv:2504.15228v2 — https://arxiv.org/pdf/2504.15228 ; https://github.com/MaximeRobeyns/self_improving_coding_agent
6. AlphaEvolve blog — https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
7. OpenEvolve — https://github.com/codelion/openevolve
