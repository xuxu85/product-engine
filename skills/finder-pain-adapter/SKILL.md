---
name: finder-pain-adapter
description: Convert verified Amazon review-analysis artifacts into the canonical Product Engine PainCard contract without inventing evidence.
---

# Finder Pain Adapter v1.0

## PURPOSE
Bridge an existing review-analysis mechanism into the Product Engine canonical PainCard format. This is an adapter, not a new pain-analysis engine.

## INPUT
A persisted review-analysis artifact produced by a verified review mechanism, such as reviews-map.json, reviews.js, or an equivalent structured review/theme output.

Required provenance:
- marketplace
- ASIN/product identifier
- source mechanism
- execution timestamp
- evidence references where available

## EXECUTION
1. Read the persisted artifact.
2. Inspect its actual schema and content.
3. Map only fields supported by the source into PainCard fields.
4. Preserve original review/evidence references.
5. Do not infer frequency, severity, confidence, or consumer intent when the source does not support them.
6. Mark unsupported fields as null/unknown rather than inventing values.

## OUTPUT
Canonical PainCard[]:

{
  pain_id,
  pain_statement,
  consumer_language[],
  evidence_refs[],
  evidence_count,
  severity,
  frequency,
  use_case,
  confidence,
  source_mechanism,
  marketplace,
  asin
}

## JUDGE
PASS only if:
- at least one PainCard exists;
- every PainCard has a traceable evidence reference;
- pain_statement is supported by source evidence;
- marketplace and ASIN are preserved;
- no unsupported metric is presented as fact;
- output conforms to the canonical schema.

FAIL if the source contains only raw reviews with no supported pain/theme analysis. Do not manufacture clusters in the adapter.

## PERSISTENCE
Persist the resulting PainCard[] in the canonical project state before downstream Trend execution.

## STATUS
This skill does NOT prove that the upstream review-analysis mechanism is executable or verified. Upstream verification remains a separate gate.

## FAILURE
If input is missing, malformed, unverified, or lacks sufficient evidence:
STATUS = BLOCKED
REPORT the exact missing condition.
Do not silently repair or invent data.

## NEXT NODE
Pain Judge -> Trend Validation only after PASS.
