# DeepSeek V4.1 Flash — Cost-Aware Coding Model Selection

Argolink-focused cost-aware coding model selection for DeepSeek V4.1 Flash. This repository is a self-contained integration reference: it explains the request shape, the asynchronous lifecycle where applicable, safe retries, and the failure states that matter in production.

[DeepSeek V4.1 Flash model page →](https://argolink.io/gh-ai-coding-model-cost-guide) · [Argolink API docs →](https://argolink.io/gh-unified-api-docs)

The model page is authoritative for live availability, pricing, limits, and fields. This repository gives the workflow a searchable home; it does not invent a second model catalog.

## What is inside

- `docs/model-contract.md`: model-specific facts checked against the current Argolink catalog.
- `docs/workflow.md`: the intent behind this repository and the decision points that prevent accidental resubmission.
- `examples/request.sh` and `examples/client.py`: safe, runnable request examples using `ARGOLINK_API_KEY`.
- `tests/test_repository.py`: offline checks for the public contract and examples.
- `ARGOLINK.md`: public-boundary rules for contributors.

## Quick start

Set the key only in your shell or secret manager, then run the example:

```bash
export ARGOLINK_API_KEY='your-key'
./examples/request.sh
```

The example uses model ID `deepseek-v4.1-flash` and endpoint family `/v1/chat/completions`. The response is JSON; keep the returned request ID and redacted error body when diagnosing a failure. A timeout does not prove that a request was rejected, so do not submit a second request automatically.

## Model facts

- Model ID: `deepseek-v4.1-flash`
- Argolink model page: `https://argolink.io/gh-ai-coding-model-cost-guide` (tracked shortlink; destination is the model page)
- Endpoint family: `/v1/chat/completions`
- Context: `1,048,576` tokens; max output: `393216` tokens.
- Reasoning efforts: `low, high, max`; default: `high`.
- Listed token rates: input `$0.15` / output `$0.6` per million tokens; cached input `$0.003` when listed.

## Scope

This repository has one clear search intent: **cost-aware coding model selection**. It keeps the integration boundary small enough for a developer or an AI assistant to answer a concrete question, while linking the live Argolink model page for changes.

## Safety

Never commit an API key, a returned media URL containing a private token, or production input. Examples are deliberately small and do not make a request during tests.
