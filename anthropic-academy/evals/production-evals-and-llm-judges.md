# Production Evals, LLM Judges & Regression Testing

**Course:** Anthropic Academy — Introduction to Evals / Building with the Claude API  
**Date:** 2026-11-26

## Key Scenarios & Takeaways

| # | Scenario | Decision / Answer | Why It Works |
|---:|---|---|---|
| **3** | Trusting an LLM judge's automated scores | Validate/calibrate the judge against **human ground-truth labels** on a sample first | Uncalibrated LLM judges can correlate poorly with actual domain standards; measuring human-judge agreement comes before trusting scores. |
| **4** | Phone carrier — static PR eval passes, but new plans cause live routing errors | Have an LLM judge sample and grade **live production chats each night** | Static PR suites miss distribution shift (new products/plans); production sampling catches real-world drift quickly. |
| **5** | Sales team — measuring token counts on a newer model run | Read the **`usage` block** returned in each response from the newer model's run | Tokenizers and generation length vary across models; every Messages API response includes exact input/output token counts in `usage`. |
| **6** | Furniture shop — forwarded email chains (~1 in 10 in live traffic) | Include forwarded chains as **~10% (1 in 10)** of the eval dataset | Eval datasets should mirror real production traffic proportions so aggregate metrics predict real-world accuracy. |
| **7** | HR handbook — binary judge verdicts flip on vague pages | Add a third **`unknown` / insufficient-evidence** verdict | Forcing Pass/Fail on ambiguous evidence creates coin-flip variance; an explicit `unknown` class stabilizes grading. |
| **8** | Online store — fixed category + one-sentence explanation | **Code checks category (exact match)** + **LLM judge grades explanation** | Deterministic rules are fast, free, and 100% consistent for structured fields; reserve LLM judges for open-ended prose. |
| **9** | Supplier contracts — model fabricates dates when missing | Specify the exact **missing-date fallback** in the prompt, then rerun | Try a clear prompt contract (explicit `null` / `"not specified"` fallback) before adding extra API calls or larger models. |
| **10** | Software company — choosing among 3 models with an accuracy floor | Pick the **middle model** (cheapest option above the accuracy floor) | Disqualify any model below the quality bar, then select the lowest cost-per-completed-task among passing models. |
| **11** | Meal-planning app — 6 production failures on single-paragraph recipes | Write expected outputs and add **all 6 as regression test cases** | Production edge-case failures belong in ground-truth regression suites so future prompt edits never break that pattern again. |
| **12** | Hotel chain — teammate merged a PR while the eval CI check failed | Enable **GitHub branch protection requiring the eval check** on `main` | Required status checks enforce that broken prompts or regressions cannot be merged to production. |
