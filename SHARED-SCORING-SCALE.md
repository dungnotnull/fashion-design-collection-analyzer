# SHARED-SCORING-SCALE.md — Design, Creative & Media Cluster

This document defines the universal 0–100 scoring scale and weighting rules used by all skills in the **Design, Creative & Media** cluster, starting with `fashion-design-collection-analyzer`.

## Universal 0–100 Scale

| Score Range | Label | Meaning |
|-------------|-------|---------|
| 90–100 | Excellent | Best-in-class execution; no material gaps. |
| 75–89 | Good | Strong execution with minor, fixable gaps. |
| 60–74 | Acceptable | Meets baseline but needs targeted improvement. |
| 40–59 | Weak | Significant issues that affect the outcome. |
| 20–39 | Poor | Major rework required; may not be viable. |
| 0–19 | Not viable | Fundamental failure in the dimension. |

## Weighting Rules

1. Default weight is equal across all dimensions (e.g., 0.20 each for 5 dimensions).
2. Weights may be adjusted when the intake or commercial objective justifies it.
3. If weights are adjusted, they must still sum to exactly 1.00.
4. The weighting rationale must be stated explicitly in the output.

## Composite Score

```
composite = Σ (dimension_score × dimension_weight)
```

Round the composite to one decimal place.

## Citation Requirement

Every dimension score must cite:
- A named framework criterion, OR
- An authoritative evidence source, OR
- A clearly labeled assumption when evidence is unavailable.

No score may be assigned without a justification string.

## Dimension Naming Convention

Skills may define domain-specific dimensions, but the scale and weighting rules remain identical.

| Skill | Dimension Set |
|-------|---------------|
| `fashion-design-collection-analyzer` | Trend relevance, Color/Material, Collection cohesion, Commercial viability, Brand fit |
| graphic-design-critic (sibling) | Strategy, Typography, Layout/Composition, Brand consistency, Execution |
| interior-design-evaluator (sibling) | Functionality, Aesthetic coherence, Material/finish, Spatial planning, Budget alignment |

## Confidence Levels

- **High:** Direct evidence from ≥2 authoritative sources or a systematic framework.
- **Medium:** One authoritative source or strong indirect evidence; minor assumptions.
- **Low:** Limited evidence, several assumptions, or contradictory signals.

Confidence must be stated per score or per composite.
