---
name: fashion-design-collection-analyzer-sub-profile-intake
description: Capture brand, target customer, season, price tier, and collection pieces for the Fashion Design / Collection Analyzer harness.
---

## Role
Sub-skill of `fashion-design-collection-analyzer`. Acts as **Stage 1: Intake**.

## Purpose
Collect a complete, validated profile of the collection under review so downstream stages can select frameworks, gather evidence, score, and build a roadmap.

## Required Inputs (Intake Schema)
Collect these fields. A field is required unless marked optional.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `brand_name` | string | yes | Brand or designer name. |
| `segment` | enum | yes | One of: luxury, premium, contemporary, mass, bridge, fast_fashion, artisanal, graduate_portfolio. |
| `target_customer` | string | yes | Age range, gender positioning, lifestyle, and geography. |
| `season` | enum | yes | One of: SS_2025, SS_2026, FW_2025, FW_2026, cruise, resort, pre_fall, capsule, evergreen. |
| `price_tier` | enum | yes | One of: entry, mass, bridge, premium, luxury, couture. |
| `distribution` | enum | optional | One of: dtc_ecommerce, wholesale, flagship, department_store, pop_up, rental, see_now_buy_now. |
| `pieces` | array | yes | List of pieces. Each piece must have `name`, `category` (top, bottom, dress, outerwear, knitwear, accessory, footwear), `color`, `material`, `silhouette`, `price_usd` (optional), `quantity` (optional). |
| `brand_positioning` | string | optional | Brand promise, aesthetic, sustainability claims, core codes. |
| `commercial_objective` | enum | optional | One of: statement_runway, commercial_sellthrough, market_entry, sustainability_reposition, awards_portfolio. |
| `constraints` | string | optional | Budget, MOQ, sustainability targets, production timeline. |

## Procedure
1. Read any structured inputs already supplied by the user or a previous stage.
2. For every required field that is missing or ambiguous, ask the user a single targeted clarifying question. Ask up to three questions in one turn; if more are needed, explain why.
3. Validate the collected payload:
   - `brand_name` is non-empty.
   - `segment` and `price_tier` are from the allowed enums.
   - `pieces` has at least 3 items and every piece has `name`, `category`, `color`, `material`.
   - Every `price_usd` is a positive number or omitted.
4. If validation fails, return the specific validation errors and request corrections.
5. Produce the structured payload below and record assumptions + confidence.

## Outputs

### Output Schema (JSON-like)
```json
{
  "intake_complete": true,
  "validation_errors": [],
  "payload": {
    "brand_name": "string",
    "segment": "enum",
    "target_customer": "string",
    "season": "enum",
    "price_tier": "enum",
    "distribution": "enum | null",
    "pieces": [
      {
        "name": "string",
        "category": "enum",
        "color": "string",
        "material": "string",
        "silhouette": "string",
        "price_usd": "number | null",
        "quantity": "number | null"
      }
    ],
    "brand_positioning": "string | null",
    "commercial_objective": "enum | null",
    "constraints": "string | null"
  },
  "assumptions": ["string"],
  "confidence": "High | Medium | Low"
}
```

## Quality Gate
- [ ] All required fields present and validated
- [ ] `pieces` array contains ≥3 pieces with required sub-fields
- [ ] Assumptions and confidence recorded
- [ ] Output schema valid and complete

## Intake Question Bank (use when fields are missing)
1. "What brand or designer name should I use for this review, and what customer segment are you targeting (luxury / premium / contemporary / mass / bridge / fast fashion / artisanal / graduate portfolio)?"
2. "Which season and price tier does this collection belong to?"
3. "Please list 3–10 pieces with name, category, color, and material so I can evaluate cohesion and merchandising."
