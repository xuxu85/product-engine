# H10 Data Provider Boundary

This directory defines the integration boundary for Helium 10.

## Purpose

H10 is a data provider, not the decision engine and not a pipeline controller.
The pipeline consumes normalized market data and must remain independent of H10-specific response shapes.

## Contract

`adapter.py` must convert an upstream H10-like payload into canonical candidate records suitable for the MARKET/FINDER stage.

Required candidate fields:

- `candidate_id`
- `marketplace`
- `asin`
- `title`
- `price`
- `monthly_sales`
- `monthly_revenue`
- `review_count`
- `rating`
- `source`

Optional fields may be preserved under `metrics` or `metadata`, but the adapter must not infer customer pain, demand validation, willingness-to-pay, or product-market fit.

## Architecture rule

H10 may be replaced by another provider without changing the core pipeline. Provider-specific normalization belongs here.

## Current status

PRE-H10 implementation. No live H10 credentials or API calls are required for this adapter contract.
