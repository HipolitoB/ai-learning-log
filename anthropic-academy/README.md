# Anthropic Academy — Prompting & AI Engineering Log

Structured notes, prompt design patterns, and small validation experiments from Anthropic Academy—applied to international trade, customs compliance, and procurement data workflows.

## Modules Queue

| Course / Module | Focus | Status | Lab / Notes |
| :--- | :--- | :---: | :--- |
| AI Fluency: Framework and foundations | 4D Framework, Automation/Augmentation/Agency, LLM & Transformer fundamentals | Completed (ID `66661851764b88f32535b613dd371f34`) | [Lesson 1](ai-fluency/lesson-01-intro-ai-fluency.md) · [Lesson 2](ai-fluency/lesson-02-why-ai-fluency.md) · [Lesson 3](ai-fluency/lesson-03-4d-framework.md) · [Lesson 4](ai-fluency/lesson-04-generative-ai-fundamentals.md) · [Transformers](ai-fluency/transformer-architecture-notes.md) |
| AI Fluency for Small Businesses | Operational AI workflows, customer data, and risk/value trade-offs via 4Ds | Completed (ID `1eafe614b7fb90a973ec315193f9b52d`) | `_badge earned_` |
| Introduction to Evals | LLM judges, calibration, traffic distribution, `unknown` verdicts & regression CI | Completed (ID `7690e4492bbc6a5f7a981676c9afead5`) | [Production Evals & LLM Judges](evals/production-evals-and-llm-judges.md) |
| Building with the Claude API | Prompting, `usage` token accounting, prompt caching, code execution & Files API, tool use, RAG, agents & MCP | In Progress (46/67) | [Lesson 44: Caching Rules](claude-api/api-lesson-44-rules-of-prompt-caching.md) · [Lesson 45: Caching in Action](claude-api/api-lesson-45-prompt-caching-in-action.md) · [Lesson 46: Code Execution & Files API](claude-api/api-lesson-46-code-execution-and-files-api.md) |
| Claude 101 / Prompt Engineering | Clear instructions, XML tags, few-shot examples & verification | In Progress | `_notes pending_` |

## Experiment Checklist
- Keep all sample trade documents (invoices, POs, charterparty recaps) **100% synthetic** before testing prompts or pushing examples here.
- Record prompt input/output structure, edge cases caught, and latency/accuracy trade-offs.
