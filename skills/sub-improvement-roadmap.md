---
name: fashion-design-collection-analyzer-sub-improvement-roadmap
description: Recommend edits to line plan, palette, and materials ranked by sell-through/impact for the Fashion Design / Collection Analyzer harness.
---

## Role
Sub-skill of `fashion-design-collection-analyzer`. Acts as **Stage 5: Improvement Roadmap**.

## Purpose
Translate the scorecard into a prioritized, actionable roadmap. Each action targets one or more weak dimensions and is ranked by effort × impact.

## Inputs
- Validated intake payload from `sub-profile-intake`.
- Selected frameworks from `sub-framework-selector`.
- Scores from `sub-scoring-engine`.

## Action Template Library
Use these action templates as starting points; adapt to the collection.

| ID | Action Template | Targets | Typical Owner |
|----|-----------------|---------|---------------|
| A01 | **Edit color story** — replace off-palette colors with seasonally forecasted Pantone/WGSN shades; enforce 60/30/10 neutral/core/accent ratio. | D2, D3 | Design Director |
| A02 | **Rebalance category mix** — align key/item/fashion/basic ratio to segment norms (e.g., luxury 20/30/30/20, mass 10/20/40/30). | D3, D4 | Merchandise Planner |
| A03 | **Clarify hero pieces** — identify 2–3 statement/anchor items and build supporting pieces around them. | D3, D5 | Creative Director |
| A04 | **Material-price realignment** — downgrade over-engineered fabrics to mass tier or upgrade perceived value to justify premium prices. | D2, D4 | Sourcing / Product Dev |
| A05 | **Strengthen sustainability proof points** — add certifications, fiber traceability, or care labeling to substantiate claims. | D2, D5 | Sustainability Lead |
| A06 | **Silhouette consistency pass** — align proportions and fit blocks so pieces work together on the same body. | D3, D5 | Pattern / Technical Design |
| A07 | **Price-architecture ladder** — introduce entry, core, and hero price points that match target-customer willingness-to-pay. | D4, D6 | Finance / Merchandising |
| A08 | **Trend-cycle timing check** — move early/late trends into the current season window or cut declining trends. | D1 | Trend Researcher |
| A09 | **Line-plan narrative** — write a one-sentence collection story and ensure every piece supports it. | D3, D5 | Brand Strategist |
| A10 | **SKU/run-depth optimization** — size the buy by expected sell-through and distribution channel capacity. | D4 | Demand Planner |

## Prioritization Formula
For each candidate action:
- **Effort** = 1 (low: copy/copy change, color swap), 2 (medium: material swap, re-merchandising), 3 (high: silhouette redevelopment, new sampling).
- **Impact** = 1 (low: marginal visual improvement), 2 (medium: improves one weak dimension), 3 (high: improves two weak dimensions or a critical score gap), 4 (transformative: reshapes commercial outcome or brand perception).
- **Priority score** = Effort × Impact. Rank descending. Break ties by fastest time-to-value and lowest risk.

## Procedure
1. Identify the lowest-scoring dimensions and their root causes from the scorecard.
2. Select 4–8 actions from the template library or invent context-specific actions.
3. Assign Effort and Impact values using the rubrics below.
4. Compute Priority score and sort descending.
5. Assign an Owner to every action.
6. Write a one-sentence rationale and state the expected effect on the target dimension(s).
7. Record assumptions and confidence.

## Effort / Impact Rubrics

### Effort
- 1 — Can be executed without sampling or supplier change (e.g., color swap, copy rewrite, price move).
- 2 — Requires one of: material swap, re-merchandising plan, certification paperwork, minor pattern tweak.
- 3 — Requires new sampling, silhouette redevelopment, supplier change, or significant line-plan restructuring.

### Impact
- 1 — Minor visual or narrative improvement; unlikely to move a dimension score by >5 points.
- 2 — Moves one weak dimension by 5–10 points.
- 3 — Moves two weak dimensions by 5–10 points, or one critical dimension by >10 points.
- 4 — Has potential to change commercial outcome or brand perception; moves composite score by >10 points.

## Outputs

### Output Schema (JSON-like)
```json
{
  "roadmap_complete": true,
  "actions": [
    {
      "rank": 1,
      "action_id": "A04",
      "action": "Material-price realignment: swap silk blouse to Tencel blend for mass tier",
      "owner": "Sourcing / Product Dev",
      "effort": 2,
      "impact": 3,
      "priority_score": 6,
      "rationale": "Silk at $89 mass-tier price destroys perceived-value margin and is inconsistent with F06 price architecture.",
      "expected_effect": "Raises D2 Color/Material to 75 and D4 Commercial Viability to 70.",
      "target_dimensions": ["color_material", "commercial_viability"]
    }
  ],
  "assumptions": ["string"],
  "confidence": "High | Medium | Low"
}
```

## Quality Gate
- [ ] 4–8 roadmap actions generated
- [ ] Every action has Effort, Impact, Owner, Rationale, and Expected Effect
- [ ] Priority score = Effort × Impact and actions ranked descending
- [ ] Actions target the lowest-scoring dimensions
- [ ] Assumptions and confidence recorded
- [ ] Output schema valid and complete
