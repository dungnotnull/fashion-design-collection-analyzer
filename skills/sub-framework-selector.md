---
name: fashion-design-collection-analyzer-sub-framework-selector
description: Select trend, color, and merchandising frameworks for the Fashion Design / Collection Analyzer harness.
---

## Role
Sub-skill of `fashion-design-collection-analyzer`. Acts as **Stage 2: Framework Selection**.

## Purpose
Given the validated intake payload, select the smallest set of named, citable frameworks that are relevant to the collection's segment, season, price tier, and commercial objective.

## Inputs
- Validated intake payload from `sub-profile-intake`.
- User request and any supplied artifacts.

## Framework Catalog
Each framework is a named, citable system used by fashion professionals.

| Framework ID | Framework Name | Best For | Key Criteria |
|--------------|----------------|----------|--------------|
| F01 | **Pantone / WGSN Seasonal Color Forecasting** | Color direction, seasonal palette coherence | Color-of-the-Year, seasonal color reports, palette harmony, color story narrative |
| F02 | **WGSN Macro/Micro Trend Lifecycle** | Trend relevance, timing | Macro drivers, micro trends, adoption curve (innovation → early adopters → mass → decline) |
| F03 | **Collection Cohesion & Merchandising (line plans, SKU architecture)** | Cohesion, assortment balance | Silhouette range, category mix, key/item/fashion/basic ratio, color ratio, size/run depth |
| F04 | **Fabric/Material Suitability & Sustainability** | Material quality, sustainability claims | Fiber origin, weight/drape, care, lifecycle impact, certifications (GOTS, OEKO-TEX, B Corp) |
| F05 | **Silhouette & Proportion Principles** | Fit, proportion, body diversity | Proportion balance, body-type inclusivity, wearability, consistency across pieces |
| F06 | **Price Architecture & Target-Customer Fit** | Commercial viability, price-tier alignment | Price architecture ladder, perceived value vs. cost, target customer willingness-to-pay |

## Framework Selection Decision Tree
Use the intake fields to decide which frameworks to activate.

1. Always activate **F03 Collection Cohesion & Merchandising** — every collection can be evaluated for line-plan balance.
2. Activate **F01 Pantone/WGSN Color Forecasting** if the intake includes ≥2 pieces with color descriptions or the objective involves seasonal palette critique.
3. Activate **F02 WGSN Trend Lifecycle** if season is SS/FW/resort/pre_fall/cruise or commercial objective is statement_runway / commercial_sellthrough.
4. Activate **F04 Fabric/Material Suitability & Sustainability** if materials are described, segment is artisanal/luxury/premium, or objective is sustainability_reposition.
5. Activate **F05 Silhouette & Proportion Principles** if pieces include silhouettes, or segment is mass/premium/contemporary where fit consistency matters.
6. Activate **F06 Price Architecture & Target-Customer Fit** if `price_usd` values are supplied, distribution is known, or objective is commercial_sellthrough / market_entry.

## Procedure
1. Read the validated intake payload.
2. Apply the decision tree above and select frameworks.
3. For each selected framework, write a one-sentence justification that ties the framework to a specific intake field (e.g., "F04 is selected because the collection claims sustainability positioning and lists linen and recycled polyester materials.").
4. List any framework considered but rejected, with a reason.
5. Produce the output schema below.

## Outputs

### Output Schema (JSON-like)
```json
{
  "framework_selection_complete": true,
  "selected_frameworks": [
    {
      "id": "F01",
      "name": "Pantone / WGSN Seasonal Color Forecasting",
      "justification": "string tied to intake field",
      "criteria": ["criterion 1", "criterion 2"]
    }
  ],
  "rejected_frameworks": [
    {
      "id": "F05",
      "name": "Silhouette & Proportion Principles",
      "reason": "No silhouette descriptions supplied and segment is graduate_portfolio where proportion experimentation is expected."
    }
  ],
  "assumptions": ["string"],
  "confidence": "High | Medium | Low"
}
```

## Quality Gate
- [ ] At least one framework selected
- [ ] Every selected framework has a justification tied to the intake payload
- [ ] Rejected frameworks documented when any framework was considered and not selected
- [ ] Output schema valid and complete
