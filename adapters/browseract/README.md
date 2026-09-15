# BrowserAct Amazon Reviews Provider Boundary

BrowserAct is a ready mechanism for `review_pain_analysis`. It is not the PAIN decision engine.

## Mechanism

`browseract-amazon-reviews-api`

Input: Amazon ASIN
Provider: BrowserAct Amazon Reviews API template
Template ID: `77817507798321724`
Dependency: `BROWSERACT_API_KEY`

The official template states that Amazon login is not required and returns structured review fields including rating, title, review text, date, verified status and variant.

## Runtime

The adapter uses BrowserAct Workflow API v2:

1. `POST /v2/workflow/run-task-by-template`
2. poll `GET /v2/workflow/get-task`
3. decode `output.string`
4. retain provider observations only

## Important limitation for current test

The official template documents only `ASIN` as an input parameter. It does not document a marketplace parameter. Therefore an Amazon.es-specific business conclusion must NOT be made until the returned data is verified as Amazon.es or a marketplace-specific BrowserAct workflow is configured.

## Business rule

Critical reviews collected from one Amazon/BrowserAct provider are one independent source. They may prove the collection mechanism and contribute evidence, but they do not by themselves satisfy the PAIN gate's independent-source requirement.
