---
name: fashion-design-collection-analyzer-cross-skill-references
description: Cross-skill wiring and shared conventions for fashion-design-collection-analyzer within the Design, Creative & Media cluster.
---

## Purpose
This document defines how `fashion-design-collection-analyzer` shares reusable sub-skill logic, scoring scales, and artifact conventions with sibling skills in the **Design, Creative & Media** cluster. It prevents drift and ensures a user can move between skills without relearning vocabulary or scales.

## Cluster Membership
- `fashion-design-collection-analyzer` (this skill)
- `graphic-design-critic` (hypothetical sibling)
- `interior-design-evaluator` (hypothetical sibling)
- `brand-identity-auditor` (hypothetical sibling)
- `industrial-product-design-review` (hypothetical sibling)

## Shared Sub-Skill Patterns

### 1. Profile Intake (`sub-profile-intake`)
**Reused by:** all cluster skills.

Common schema fields every cluster intake must capture:
- `subject_name` / `brand_name`
- `segment` (luxury, premium, contemporary, mass, bridge, artisanal, graduate_portfolio)
- `target_audience`
- `commercial_objective`
- `pieces` / `artifacts` / `deliverables` (domain-specific list)

**Fashion-specific extensions:** season, price_tier, distribution, material/color per piece.

Sibling skills should import the intake validation rules and replace only the domain-specific enums and sub-fields.

### 2. Framework Selector (`sub-framework-selector`)
**Reused by:** all cluster skills.

Common convention:
- Framework IDs (`F01`, `F02`, …) are cluster-scoped and stable.
- Each skill owns a framework catalog mapping IDs to named, citable frameworks.
- Selection must produce a one-sentence justification tied to an intake field.

**Fashion catalog:** documented in `skills/sub-framework-selector.md`.

### 3. Scoring Engine (`sub-scoring-engine`)
**Reused by:** all cluster skills that produce multi-dimensional scores.

Common convention:
- 0–100 scale per dimension.
- Default equal weights (0.20 each for 5 dimensions).
- Composite = weighted mean; weights must sum to 1.00.
- Every score cites a framework criterion or evidence source.

**Fashion dimension set:** Trend relevance, Color/Material, Collection cohesion, Commercial viability, Brand fit.

Sibling skills may rename dimensions (e.g., Typography, Layout, Brand Consistency for graphic design) but must keep the same 0–100 scale, weighting rules, and citation requirement.

### 4. Improvement Roadmap (`sub-improvement-roadmap`)
**Reused by:** all cluster skills.

Common convention:
- Effort ∈ {1, 2, 3}.
- Impact ∈ {1, 2, 3, 4}.
- Priority score = Effort × Impact; rank descending.
- Every action has Owner, Rationale, and Expected Effect.

Sibling skills should reuse the prioritization formula and action-template pattern; only the action content is domain-specific.

## Shared Scoring Scale

| Score Range | Interpretation | Use Across Cluster |
|-------------|----------------|--------------------|
| 90–100 | Excellent / best-in-class | Consistent |
| 75–89 | Good / minor gaps | Consistent |
| 60–74 | Acceptable / needs work | Consistent |
| 40–59 | Weak / significant issues | Consistent |
| 20–39 | Poor / major rework | Consistent |
| 0–19 | Not viable | Consistent |

## Shared Quality Gates
Every cluster skill must enforce:
1. Framework selection justified.
2. Every score cites a framework or source.
3. Roadmap items have effort, impact, owner, and rationale.
4. Assumptions and confidence stated.
5. Devil's-advocate review completed.

## Knowledge Base Sharing
- `SECOND-KNOWLEDGE-BRAIN.md` is skill-specific but follows a shared append format:
  `- {date} | score={score} | **{title}** | {authors} | {year} | {venue} | {url} <!--hash:{hash}-->`
- The hash format `<!--hash:{16-hex}-->` is cluster-standard for deduplication.
- Each skill's `tools/knowledge_updater.py` may reuse the `KnowledgeEntry`, `_score_entry`, `load_existing_hashes`, and `append_entries` patterns from this skill.

## Integration Points with Other Clusters

### Business / Strategy Cluster
- Outputs from `fashion-design-collection-analyzer` feed into merchandising and go-to-market planning skills.
- Commercial viability score and roadmap are the primary handoff artifacts.

### Sustainability / ESG Cluster
- F04 (Fabric/Material Suitability & Sustainability) overlaps with material-lifecycle and greenwashing-review skills.
- Recommended handoff: list of unsupported sustainability claims and certification gaps.

### Technology / AI Cluster
- `tools/knowledge_updater.py` can be reused by any skill needing a Crossref + RSS + DuckDuckgo crawler.

## Alignment Checklist for New Sibling Skills
- [ ] Uses the same 0–100 scale and default weighting rules.
- [ ] Uses the same Effort/Impact roadmap prioritization formula.
- [ ] Includes all 5 shared quality gates.
- [ ] References this document or a cluster-level `CLUSTER-CONVENTIONS.md`.
- [ ] Reuses hash format for knowledge-base deduplication.
