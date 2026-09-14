# READY MECHANISM POLICY

## Purpose

The Product Engine must reuse an existing tool, repository, skill, workflow, API, or MCP before building a custom implementation.

## Required order

```text
CAPABILITY REQUIRED
      ↓
SEARCH READY MECHANISMS
      ↓
INSPECT REPOSITORY / SKILL / API
      ↓
VERIFY INPUT → OUTPUT CONTRACT
      ↓
ADAPT INTO PRODUCT ENGINE
      ↓
ONLY IF NO SUITABLE MECHANISM EXISTS
BUILD THE MINIMUM MISSING FUNCTION
```

## Finder rule

The Finder does not invent Amazon discovery filters or become a scraper. It requests a capability (for example `amazon_product_discovery` or `review_pain_analysis`) and delegates to the registered mechanism.

The mechanism returns observations. The Product Engine may classify those observations into pain, gap, opportunity, or asymmetry, but it must not silently change the provider's collection logic.

## Evidence rule

Provider output is evidence only when its provenance is retained:

- source/provider;
- marketplace;
- period/date;
- method;
- verification status.

Synthetic fixtures may test interfaces and routing only. They cannot produce a business PASS.

## Current reusable mechanisms

| Capability | Mechanism | Repository | State |
|---|---|---|---|
| Amazon product discovery | product-opportunity-finder-skill | `AronLEEdev/product-opportunity-finder-skill` | dependency-controlled |
| Review/pain analysis | product-review-analyze-skill | `AronLEEdev/product-review-analyze-skill` | available |
| Amazon product research | product-research-skills | `AronLEEdev/product-research-skills` | verification required |
| H10 data access | Helium10 MCP | `helium10/Helium10-MCP` | dependency-controlled |

## Anti-duplication

Do not build a second Amazon scraper, Product Intelligence Engine, review platform, research database, or H10 replacement merely because a current mechanism has an integration gap.

If integration is missing, build the smallest adapter/bridge required to consume the existing mechanism.
