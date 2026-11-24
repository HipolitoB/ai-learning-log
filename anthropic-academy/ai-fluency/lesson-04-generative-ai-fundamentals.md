# Lesson 4: Generative AI Fundamentals

**Course:** AI Fluency: Framework and foundations (Anthropic Academy)  
**Date:** 2026-11-24

## Key Takeaways
- **Traditional vs. Generative AI:** Traditional AI analyzes and classifies existing data (e.g., spam detection), whereas generative AI creates new content statistically.
- **Large Language Models (LLMs):** Neural networks with billions of parameters trained to predict and generate human language.
- **Three Catalysts Behind Modern LLMs:**
  1. **Transformer Architecture (2017):** Enabled parallel sequence processing and long-range contextual relationships.
  2. **Digital Data Explosion:** Massive corpora of web text, books, and open-source code.
  3. **Compute Scale:** Distributed clusters of GPUs and TPUs.
- **Scaling Laws:** Increasing model parameters (`N`), training tokens (`D`), and compute (`C`) predictably reduces prediction loss and unlocks **emergent capabilities** (e.g., step-by-step reasoning, few-shot adaptation).

## Lifecycle & Runtime Mechanics
1. **Pre-training:** Next-token prediction across billions of text examples to build a statistical map of language and knowledge.
2. **Fine-tuning & RL:** Alignment with human feedback to follow instructions helpfully, honestly, and harmlessly.
3. **Inference & Context Window:** Models generate text on the fly rather than querying a static answer database, bounded by their **context window** (working memory).
4. **In-Context Learning:** Adapting to new tasks immediately from instructions and examples inside the prompt without retraining.
