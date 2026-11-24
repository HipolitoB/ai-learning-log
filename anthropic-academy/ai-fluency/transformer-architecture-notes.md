# Transformer Architecture & Scaling Deep Dive

**Sources:** Lesson 4 (*Generative AI fundamentals*), *Attention Is All You Need* (2017), and *The Annotated Transformer* (Alexander Rush / Harvard NLP)  
**Date:** 2026-11-24

## Why Transformers Replaced RNNs
- Earlier recurrent models (RNNs) processed text strictly sequentially left-to-right, causing:
  - **Long-range memory decay** over long paragraphs.
  - **Sequential training bottlenecks** that could not fully exploit parallel hardware.
- **Self-Attention** computes attention weights between every token and all other tokens simultaneously in a constant number of path-length operations, using **Multi-Head Attention** to preserve resolution across different relationship types.

## Hardware & Scaling Laws
- **GPUs / TPUs:** Unlike CPUs (few fast cores for sequential tasks), GPUs and TPUs provide thousands of parallel cores suited for massive matrix multiplications—matching the Transformer's parallel sequence processing.
- **Scaling Laws (`N`, `D`, `C`):** Smooth, predictable power-law loss improvements as parameters (`N`), dataset tokens (`D`), and compute FLOPs (`C`) scale together, accompanied by sharp **emergent abilities** past certain scale thresholds.
