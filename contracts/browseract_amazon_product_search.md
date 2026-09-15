# BrowserAct Amazon Product Search — Temporary Test Contract

## Purpose
Verify that the ready BrowserAct mechanism can execute one Amazon product-search task and return structured provider observations before any business conclusion.

## Input contract
- `KeyWords`: required string
- `Brand`: string; empty allowed
- `Maximum_date`: required numeric value represented as a string by the workflow API
- `language`: required string

## Test
- Marketplace target: Amazon Spain / `amazon.es`
- Keywords: `electrolyte water`
- Brand: empty
- Maximum products: `20`
- Language: `en`

## Expected provider observations
The returned data should contain product-level observations such as title, URL, rating, review count, price and any monthly-sales / availability / Best Seller fields exposed by the workflow.

## Business boundary
This test does not infer pain, opportunity, demand validity, or PASS/FAIL/PIVOT. Provider output must be validated before entering the business pipeline.

## Source
Official BrowserAct Amazon Product Search API skill / workflow template `77809217106347580`.
