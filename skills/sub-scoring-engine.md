---
name: fashion-design-collection-analyzer-sub-scoring-engine
description: Score trend relevance, color/material, cohesion, and commercial viability for the Fashion Design / Collection Analyzer harness.
---

## Role
Sub-skill of `fashion-design-collection-analyzer`. Acts as **Stage 4: Scoring**.

## Purpose
Score the collection 0–100 across five dimensions. Every score must cite a framework criterion or evidence source. Produce a structured payload for the roadmap stage.

## Inputs
- Validated intake payload from `sub-profile-intake`.
- Selected frameworks from `sub-framework-selector`.
- Evidence gathered from WebSearch/WebFetch or `SECOND-KNOWLEDGE-BRAIN.md`.

## Scoring Dimensions and Rubrics
For each dimension, use the rubric below to map qualitative evidence to a 0–100 score. Scores should be multiples of 5 unless strong evidence justifies another value.

### D1 — Trend Relevance (weight default 0.20)
Framework: F02 WGSN Macro/Micro Trend Lifecycle.

| Score | Description |
|-------|-------------|
| 90–100 | Collection directly addresses a confirmed macro trend in the relevant season; evidence from WGSN / Pantone / BoF supports alignment. |
| 75–89 | Strong alignment with a micro trend or early-stage macro signal; timing is appropriate. |
| 60–74 | Trend-relevant but derivative or slightly mistimed; no strong seasonal signal. |
| 40–59 | Weak trend link; relies on evergreen basics or contradicts current direction. |
| 20–39 | Out of phase with the season or targets a trend in decline. |
| 0–19 | No discernible trend relevance or actively off-trend. |

### D2 — Color / Material (weight default 0.20)
Framework: F01 Pantone/WGSN Color Forecasting + F04 Fabric/Material Suitability.

| Score | Description |
|-------|-------------|
| 90–100 | Palette is seasonally coherent, uses forecasted colors, and materials are appropriate to segment and price tier with credible sustainability credentials where claimed. |
| 75–89 | Good palette and material choices; minor mismatch in one area (e.g., one off-palette color). |
| 60–74 | Adequate but uninspired; some materials feel under- or over-engineered for the price. |
| 40–59 | Noticeable palette incoherence or material-price mismatch; sustainability claims unsupported. |
| 20–39 | Clashing colors or unsuitable materials; greenwashing risk or quality issues evident. |
| 0–19 | Fundamental failure in color/material execution. |

### D3 — Collection Cohesion (weight default 0.20)
Framework: F03 Collection Cohesion & Merchandising.

| Score | Description |
|-------|-------------|
| 90–100 | Clear narrative, balanced category mix, logical color ratio, coherent silhouettes; strong line-plan architecture. |
| 75–89 | Mostly cohesive; 1–2 pieces could be edited without harming the story. |
| 60–74 | Cohesion exists but is thin; category mix or color story needs work. |
| 40–59 | Pieces feel disjointed; no clear line plan or SKU architecture. |
| 20–39 | Random assemblage; conflicting aesthetics or silhouettes. |
| 0–19 | No coherent collection identity. |

### D4 — Commercial Viability (weight default 0.20)
Framework: F06 Price Architecture & Target-Customer Fit.

| Score | Description |
|-------|-------------|
| 90–100 | Price architecture aligns perfectly with target customer and distribution; perceived value exceeds cost; clear hero/capsule/basic balance. |
| 75–89 | Strong commercial logic; minor price or distribution friction. |
| 60–74 | Viable but undifferentiated; may struggle in a crowded market. |
| 40–59 | Price-tier mismatch, weak value proposition, or wrong channel for the customer. |
| 20–39 | Serious commercial risk (e.g., luxury fabric at mass price, unknown customer). |
| 0–19 | Not commercially viable in current form. |

### D5 — Brand Fit (weight default 0.20)
Framework: F03 + F05 + F06 combined.

| Score | Description |
|-------|-------------|
| 90–100 | Collection is unmistakably on-brand; extends existing codes while surprising appropriately; consistent with positioning and sustainability claims. |
| 75–89 | Strong brand fit; small tension that could become a feature with storytelling. |
| 60–74 | On-brand but generic; does not advance the brand narrative. |
| 40–59 | Mixed brand signals; some pieces feel off-brand or inconsistent with sustainability/price claims. |
| 20–39 | Significant brand disconnect; contradicts stated positioning. |
| 0–19 | Collection does not read as the brand at all. |

## Weighting Rules
- Default weights: 0.20 per dimension.
- Adjust weights only when the intake or objective justifies it, and explain the rationale.
- Common adjustments:
  - `sustainability_reposition` → raise D2 and D4 weights to 0.25, lower D1 to 0.15.
  - `statement_runway` → raise D3 and D5 weights to 0.25, lower D4 to 0.15.
  - `graduate_portfolio` → raise D5 and D3 weights, lower D4.

## Procedure
1. Review the selected frameworks and their criteria.
2. Map each piece of evidence to the relevant dimension and criterion.
3. Assign a 0–100 score for each dimension using the rubrics above.
4. Determine weights (default or adjusted with rationale).
5. Compute composite = Σ(score × weight).
6. For every score, write a 1–2 sentence justification and cite the source/framework.
7. Record confidence and assumptions.

## Outputs

### Output Schema (JSON-like)
```json
{
  "scoring_complete": true,
  "weights": {
    "trend_relevance": 0.20,
    "color_material": 0.20,
    "collection_cohesion": 0.20,
    "commercial_viability": 0.20,
    "brand_fit": 0.20
  },
  "weighting_rationale": "string",
  "scores": {
    "trend_relevance": { "score": 85, "justification": "...", "citation": "...", "framework": "F02" },
    "color_material": { "score": 70, "justification": "...", "citation": "...", "framework": "F01+F04" },
    "collection_cohesion": { "score": 75, "justification": "...", "citation": "...", "framework": "F03" },
    "commercial_viability": { "score": 60, "justification": "...", "citation": "...", "framework": "F06" },
    "brand_fit": { "score": 80, "justification": "...", "citation": "...", "framework": "F03+F05+F06" }
  },
  "composite_score": 74.0,
  "assumptions": ["string"],
  "confidence": "High | Medium | Low"
}
```

## Quality Gate
- [ ] All five dimensions scored
- [ ] Every score has a cited justification tied to a framework or evidence source
- [ ] Weights sum to 1.00 and rationale given if changed from default
- [ ] Composite score computed correctly
- [ ] Assumptions and confidence recorded
- [ ] Output schema valid and complete
