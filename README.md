# AI coding model cost guide

This workbook calculates transparent token estimates for coding tasks. It separates input, cached input, and output units and stores a source/date beside every price. **[ArgoLink](https://argolink.io/gh-ai-coding-model-cost-guide) contributes one catalog snapshot; it is not an official model-price sheet.** Last checked: 2026-10-07.

## Run it

python3 -m cost.calc cost/prices.json --input 200000 --output 20000

The calculator reads price per token, not price per million tokens. For 200,000 uncached input tokens and 20,000 output tokens, the formula is input times input rate plus output times output rate. Cached input is billed at the cached field when present. It does not apply long-context multipliers because those depend on model threshold and request shape; add a separate row after reading the current catalog.

## Snapshot

The included values are dated effective catalog rates for GPT-6 Sol, GPT-5.4, Claude Opus 5, and DeepSeek V4 Pro. They are not claims about official vendor list price. A price field without a source should be rejected. The current catalog may expose official and effective values separately; keep both columns in a research spreadsheet.

## Workload matrix

A short patch is usually input-heavy and benefits from cache reuse. A repository refactor can cross a long-context threshold and produce a large output. A code review may need high reasoning effort but that does not automatically alter the token rate. Estimate cold prompt, warm cache, and long context separately. Compare failure/retry policy separately; a cheap token price can lose if an unsafe retry repeats a large request.

| Scenario | Input | Output | What to record |
|---|---:|---:|---|
| patch review | 40k | 8k | cache eligibility and tool calls |
| repository refactor | 200k | 20k | long-context rule and peak output |
| design document | 80k | 12k | structured output and truncation |
| agent loop | variable | variable | number of rounds and failed tools |

## Validation

python3 -m unittest discover -s tests is offline. The calculator does not call a provider, discover models, or estimate video/image billing. Keep the catalog snapshot with your report. If the model page has a minimum charge, peak-hour multiplier, reasoning surcharge, or context multiplier, model it explicitly rather than hiding it in a rounded rate.

## FAQ

**Is this an invoice?** No. It is a reproducible estimate. **Why keep cache separate?** Cached input often has a distinct rate. **Why omit unknown models?** A missing primary source is better than a fabricated number. **Can I compare video here?** No; video uses seconds and reference-input rules. **What should a budget alert use?** The upper scenario plus a retry reserve, with request IDs retained for audit.
