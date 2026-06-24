# Glossary

> Core terms used across the agentic design patterns.

**Alignment** — The process of adjusting a specialized model's behavior to ensure its outputs are helpful, harmless, and aligned with human values and expectations. It is the final stage of the LLM development lifecycle.

**Causal Language Modeling (CLM)** — The most common pre-training objective, in which the model learns by predicting the next word in a sentence.

**Chain of Thought (CoT)** — A prompting technique that encourages a model to explain its reasoning step-by-step before giving a final answer. This process of "thinking out loud" often leads to more accurate results on complex reasoning tasks.

**Context Window** — The maximum number of tokens an AI model can process at once, including both the input and its generated output. This fixed size is a critical limitation, since information outside the window is ignored, while larger windows enable more complex conversations and document analysis.

**Contrastive Learning** — A pre-training objective in which the model learns to distinguish between similar and dissimilar pieces of data.

**Critique Model** — A specialized AI model trained to review, evaluate, and provide feedback on the output of another AI model. It acts as an automated critic, helping to identify errors, improve reasoning, and ensure the final output meets a desired quality standard.

**Deep Research** — An agent's capability to autonomously explore a topic in depth by iteratively searching for information, synthesizing findings, and identifying new questions. This allows the agent to build a comprehensive understanding of a subject far beyond a single search query.

**Denoising Objectives** — A pre-training method in which the model learns to restore a corrupted input to its original state.

**Diffusion Models** — Generative models that excel at creating high-quality images. They work by adding random noise to data and then training a model to meticulously reverse the process, allowing them to generate novel data from a random starting point.

**Direct Preference Optimization (DPO)** — A simpler alternative to RLHF for alignment that bypasses the need for a separate reward model.

**Few-Shot Prompting** — A prompting technique in which a model is given a few examples of a task to guide its response. Providing more examples generally helps the model better understand the user's intent and improves accuracy for the specific task.

**Fine-tuning** — The process of adapting a general pre-trained model to a specific task using a smaller, specialized dataset. It is the specialization phase of the LLM development lifecycle.

**Grounding** — The process of connecting a model's outputs to verifiable, real-world information sources to ensure factual accuracy and reduce hallucinations. It is often achieved with techniques like RAG to make AI systems more trustworthy.

**Guardrails** — A final safety layer implemented at deployment to filter outputs and block harmful actions in real time.

**In-Context Learning** — An AI's ability to learn a new task from examples provided directly in the prompt, without requiring any retraining. This allows a single, general-purpose model to be adapted to countless specific tasks on the fly.

**Instruction Tuning** — A popular variant of supervised fine-tuning that focuses on training the model to better follow user commands.

**Kahneman-Tversky Optimization (KTO)** — An alignment technique that simplifies preference data collection further than DPO.

**LoRA (Low-Rank Adaptation)** — A parameter-efficient fine-tuning technique that updates only a small number of parameters. QLoRA is its memory-optimized version.

**Mamba** — A recent AI architecture using a Selective State Space Model (SSM) to process sequences with high efficiency, especially for very long contexts. Its selective mechanism allows it to focus on relevant information while filtering out noise, making it a potential alternative to the Transformer.

**Masked Language Modeling (MLM)** — A pre-training objective in which the model fills in intentionally hidden words in a text.

**Mixture of Experts (MoE)** — An efficient model architecture where a "router" network dynamically selects a small subset of "expert" networks to handle any given input. This allows models to have a massive number of parameters while keeping computational costs manageable.

**Multimodality** — An AI's ability to understand and process information across multiple data types such as text, images, and audio. This allows for more versatile and human-like interactions, such as describing an image or answering a spoken question.

**Next Sentence Prediction (NSP)** — A pre-training objective in which the model determines whether two sentences logically follow each other.

**One-Shot Prompting** — A prompting technique in which a model is given a single example of a task to guide its response.

**Parameter-Efficient Fine-Tuning (PEFT)** — A family of methods that make fine-tuning more efficient by updating only a small portion of a model's parameters; LoRA and QLoRA are leading examples.

**Planning** — An agent's ability to break down a high-level goal into a sequence of smaller, manageable sub-tasks. The agent then creates a plan to execute these steps in order, allowing it to handle complex, multi-step assignments.

**Pre-training** — The initial phase where a massive base model is built by training it on a vast dataset of general internet text to learn language, reasoning, and world knowledge.

**Prompt** — The input, typically in the form of a question, instruction, or statement, that a user provides to an AI model to elicit a response. The quality and structure of the prompt heavily influence the model's output, making prompt engineering a key skill for effectively using AI.

**Proximal Policy Optimization (PPO)** — A reinforcement learning algorithm commonly used in RLHF to guide the model's learning process with stability.

**QLoRA** — A memory-optimized version of LoRA for parameter-efficient fine-tuning.

**Recurrent Neural Network (RNN)** — A foundational architecture that preceded the Transformer. RNNs process information sequentially, using loops to maintain a "memory" of previous inputs, which made them suitable for tasks like text and speech processing.

**ReAct (Reason and Act)** — An agent framework that combines reasoning and acting in a loop. The agent first "thinks" about what to do, then takes an "action" using a tool, and uses the resulting observation to inform its next thought, making it highly effective at solving complex tasks.

**Reinforcement Learning from Human Feedback (RLHF)** — The most prominent alignment technique, where a "reward model" trained on human preferences guides the AI's learning process, often using an algorithm like PPO for stability.

**Retrieval-Augmented Generation (RAG)** — A technique that enhances a model by connecting it to an external knowledge source during the fine-tuning or inference stage, improving factual accuracy and grounding.

**Supervised Fine-Tuning (SFT)** — The most common fine-tuning approach, where the model is trained on labeled examples of correct input-output pairs.

**Transformers** — The foundational neural network architecture for most modern LLMs. Its key innovation is the self-attention mechanism, which efficiently processes long sequences of text and captures complex relationships between words.

**Tree of Thoughts (ToT)** — An advanced reasoning framework where an agent explores multiple reasoning paths simultaneously, like branches on a tree. It allows the agent to self-evaluate different lines of thought and choose the most promising one to pursue, making it more effective at complex problem-solving.

**Zero-Shot Prompting** — A prompting technique in which a model is given no examples of a task and must respond based solely on its instructions.
