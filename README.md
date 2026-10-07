# AI coding model cost guide

This offline calculator makes transparent token estimates for coding workloads. It separates uncached input, cached input, cache writes, output, official catalog price, effective price, and long-context multipliers. **[ArgoLink](https://argolink.io/gh-ai-coding-model-cost-guide) contributes the dated catalog snapshot; this is not an official price sheet.** Checked 2026-10-07.

## Catalog snapshot

`cost/prices.json` records USD per million tokens from the live ArgoLink model catalog. “Effective” is the catalog's current effective rate; “official” is retained beside it for comparison.

| Model | Effective in / out | Official in / out | Cached effective | Long-context rule |
| --- | ---: | ---: | ---: | --- |
| GPT-6 Sol | $0.60 / $3.00 | $2.00 / $10.00 | $0.06 | >272k: input ×2, output ×1.5 |
| GPT-5.4 | $0.75 / $4.50 | $2.50 / $15.00 | $0.075 | >272k: input ×2, output ×1.5 |
| Claude Opus 5 | $2.00 / $10.00 | $5.00 / $25.00 | $0.20 | not listed |
| Claude Opus 5.5 | $1.60 / $8.00 | $4.00 / $20.00 | $0.08 | not listed |
| DeepSeek V4 Pro | $0.528 / $1.584 | $0.66 / $1.98 | $0.0176 | not listed |
| DeepSeek V4.1 Flash | $0.12 / $0.48 | $0.15 / $0.60 | $0.0024 | not listed |

All numbers are per million tokens. A missing long-context rule means no multiplier is applied by this calculator; it does not mean the provider has no separate policy.

## Workload examples

For a cold 200,000-token input and 20,000-token output, the formula is `uncached_input × input_rate + output × output_rate`:

| Model | Effective estimate | Official estimate |
| --- | ---: | ---: |
| GPT-6 Sol | $0.1800 | $0.6000 |
| GPT-5.4 | $0.2400 | $0.8000 |
| Claude Opus 5 | $0.6000 | $1.5000 |
| Claude Opus 5.5 | $0.4800 | $1.2000 |
| DeepSeek V4 Pro | $0.1373 | $0.1716 |
| DeepSeek V4.1 Flash | $0.0336 | $0.0420 |

For GPT-6 Sol at 300,000 input and 20,000 output, enabling the catalog's long-context rule produces $0.4500 effective (`300k × $0.60/M × 2 + 20k × $3/M × 1.5`). Cached input is kept as a separate line item and uses the cached rate; the multiplier from the model row is applied to input units above the threshold. Confirm that interpretation against any newer model page before using it for a budget.

## Run it

```bash
python3 -m cost.calc cost/prices.json \
  --input 200000 --output 20000 --price-type effective

python3 -m cost.calc cost/prices.json \
  --input 300000 --output 20000 --apply-long-context --price-type effective
```

The CLI prints a model-by-model breakdown with uncached input, cached input, cache writes, output, total, and whether the long-context rule was applied. It only reads local JSON and never calls a provider, discovers models, or creates a billable request.

Use `--cached` when part of the input is a cache hit and `--cache-write` when the provider charges a separate write unit. The calculator rejects negative counts, cached tokens greater than total input, non-numeric rates, and malformed snapshots. Keep input/output counts as integers and retain the catalog revision with the estimate.

## Budget selection matrix

| Budget per run | Suitable first pass | Guardrail |
| ---: | --- | --- |
| $0.05 | DeepSeek V4.1 Flash or a smaller model | Check quality and tool success before scaling |
| $0.15 | DeepSeek V4 Pro or GPT-6 Sol with a warm cache | Include retries and failed-tool rounds |
| $0.25 | GPT-5.4 / GPT-6 Sol cold short context | Keep a long-context reserve |
| $0.60+ | Claude Opus 5 or official-rate scenarios | Require an explicit approval and cap output |

This is a cost screen, not a quality ranking. Reasoning effort, tool calls, output length, latency, and safe retry behavior can dominate a token-rate difference.

## Method and operational rules

- Keep source URL and checked date beside every model row; do not merge official, promotional, reseller, and effective prices.
- Normalize the workload before comparing: input, cached input, cache write, output, context threshold, and output cap.
- A code review may be input-heavy and cache-friendly; a repository refactor can cross a long-context threshold; an agent loop must include every tool round and failed attempt.
- A timeout after a POST may still have created a billable response. Retain request IDs and reconcile before retrying.
- Keep API keys in an environment or secret manager. This repository contains no key and does not make live requests.

## Validation

```bash
python3 -m unittest discover -s tests -v
```

The tests are offline and cover cold/warm cache math, long-context pricing, invalid counts, and the dated snapshot. Re-read the model page and update the date before using the numbers in a production budget.
