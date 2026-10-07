"""Offline token-cost estimator for a dated model-price snapshot."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _tokens(value: int, name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def multipliers(row: dict[str, Any], input_tokens: int, apply_long_context: bool) -> tuple[float, float]:
    if not apply_long_context:
        return 1.0, 1.0
    rule = row.get("long_context")
    if not rule or input_tokens <= int(rule["threshold"]):
        return 1.0, 1.0
    return float(rule["input_multiplier"]), float(rule["output_multiplier"])


def estimate(
    row: dict[str, Any],
    input_tokens: int,
    output_tokens: int,
    cache_tokens: int = 0,
    cache_write_tokens: int = 0,
    apply_long_context: bool = False,
) -> dict[str, float | bool]:
    """Return a transparent breakdown; rates in row are USD per million tokens."""
    input_tokens = _tokens(input_tokens, "input_tokens")
    output_tokens = _tokens(output_tokens, "output_tokens")
    cache_tokens = _tokens(cache_tokens, "cache_tokens")
    cache_write_tokens = _tokens(cache_write_tokens, "cache_write_tokens")
    if cache_tokens > input_tokens:
        raise ValueError("cache_tokens cannot exceed input_tokens")
    for key in ("input", "output"):
        if not isinstance(row.get(key), (int, float)) or not math.isfinite(float(row[key])) or row[key] < 0:
            raise ValueError(f"row.{key} must be a non-negative numeric USD-per-million rate")
    cached_rate = row.get("cached", row["input"])
    cache_write_rate = row.get("cache_write", row["input"])
    if not isinstance(cached_rate, (int, float)) or not isinstance(cache_write_rate, (int, float)):
        raise ValueError("cached and cache_write rates must be numeric when supplied")
    input_multiplier, output_multiplier = multipliers(row, input_tokens, apply_long_context)
    uncached_tokens = input_tokens - cache_tokens
    uncached_cost = uncached_tokens / 1_000_000 * float(row["input"]) * input_multiplier
    cached_cost = cache_tokens / 1_000_000 * float(cached_rate) * input_multiplier
    output_cost = output_tokens / 1_000_000 * float(row["output"]) * output_multiplier
    cache_write_cost = cache_write_tokens / 1_000_000 * float(cache_write_rate) * input_multiplier
    return {
        "uncached_input_usd": uncached_cost,
        "cached_input_usd": cached_cost,
        "cache_write_usd": cache_write_cost,
        "output_usd": output_cost,
        "total_usd": uncached_cost + cached_cost + cache_write_cost + output_cost,
        "long_context_applied": input_multiplier != 1.0 or output_multiplier != 1.0,
    }


def load_models(path: Path) -> dict[str, dict[str, Any]]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read price snapshot: {exc}") from exc
    if not isinstance(document, dict) or not isinstance(document.get("models"), dict):
        raise ValueError("price snapshot must contain a models object")
    return document["models"]


def rate_row(model: dict[str, Any], price_type: str) -> dict[str, Any]:
    value = model.get(price_type)
    if not isinstance(value, dict):
        raise ValueError(f"model has no {price_type} rates")
    row = dict(value)
    row["long_context"] = model.get("long_context")
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate coding-model token costs without network calls")
    parser.add_argument("prices", type=Path)
    parser.add_argument("--input", type=int, required=True)
    parser.add_argument("--output", type=int, required=True)
    parser.add_argument("--cached", type=int, default=0)
    parser.add_argument("--cache-write", type=int, default=0)
    parser.add_argument("--price-type", choices=("effective", "official"), default="effective")
    parser.add_argument("--apply-long-context", action="store_true")
    args = parser.parse_args()
    models = load_models(args.prices)
    result = {
        model_id: estimate(rate_row(model, args.price_type), args.input, args.output, args.cached, args.cache_write, args.apply_long_context)
        for model_id, model in models.items()
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
