# PROJECT-detail.md — Fashion Design / Collection Analyzer

## Executive Summary
`fashion-design-collection-analyzer` is a Claude Skill that turns Claude into **a fashion design critic and merchandiser who evaluates collections for trend relevance, color/fabric, cohesion, and commercial viability**. It ingests domain inputs, screens for safety/compliance where required, selects a world-renowned evaluation framework, gathers fresh evidence, scores the subject across 5 dimensions, and outputs a prioritized improvement roadmap. It is part of the **Design, Creative & Media** cluster.

## Problem Statement
Designers and brands need objective feedback on whether a collection is on-trend, cohesive, well-constructed (color/material), and commercially viable, beyond subjective taste.

Domain context: practitioners need reproducible, evidence-graded evaluation rather than ad-hoc opinion. This skill enforces a research-first harness with explicit quality gates and a self-improving knowledge base.

## Target Users & Use Cases
- Primary: practitioners, learners, and decision-makers in this domain.
- Trigger examples:
1. **SS collection trend check** — Designer shares a spring line. Expect trend-cycle positioning and palette critique.
2. **Cohesion problem** — Pieces feel disjointed. Expect line-plan and SKU-architecture roadmap.
3. **Sustainability positioning** — Brand wants eco-credibility. Expect material-suitability and greenwashing caution.
4. **Price-tier mismatch** — Luxury fabrics at mass price. Expect price-architecture realignment.
5. **New designer portfolio** — Grad collection. Expect commercial-viability vs creative-statement balance.

## Harness Architecture
```
/fashion-design-collection-analyzer  (main.md)
   |
   v
[1] sub-profile-intake        -> structured intake
   |
   v
[2] framework selection  -> choose named framework
   |
   v
[3] research (WebSearch/WebFetch)        -> evidence (graceful deg: SECOND-KNOWLEDGE-BRAIN.md)
   |
   v
[4] scoring engine                       -> 0-100 multi-dimensional score
   |
   v
[5] improvement roadmap                  -> effort x impact prioritized actions
   |
   v
[6] quality-gate / devil's advocate      -> final professional artifact
```

## Full Sub-Skill Catalog
#### `sub-profile-intake`
- **Purpose:** Capture brand, target customer, season, price tier, and collection pieces.
- **Inputs:** structured outputs from prior stage + user-supplied data
- **Outputs:** validated, structured payload for the next stage
- **Tools:** Read, Write
- **Quality gate:** output schema validated before proceeding

#### `sub-framework-selector`
- **Purpose:** Select trend, color, and merchandising frameworks for the segment.
- **Inputs:** structured outputs from prior stage + user-supplied data
- **Outputs:** validated, structured payload for the next stage
- **Tools:** Read, Write, WebSearch/WebFetch
- **Quality gate:** output schema validated before proceeding

#### `sub-scoring-engine`
- **Purpose:** Score trend relevance, color/material, cohesion, and commercial viability.
- **Inputs:** structured outputs from prior stage + user-supplied data
- **Outputs:** validated, structured payload for the next stage
- **Tools:** Read, Write, WebSearch/WebFetch
- **Quality gate:** output schema validated before proceeding

#### `sub-improvement-roadmap`
- **Purpose:** Recommend edits to line plan, palette, and materials ranked by sell-through/impact.
- **Inputs:** structured outputs from prior stage + user-supplied data
- **Outputs:** validated, structured payload for the next stage
- **Tools:** Read, Write
- **Quality gate:** output schema validated before proceeding


## Evaluation Frameworks (world-renowned, citable)
- Color theory & seasonal palettes (Pantone/WGSN cycles)
- Trend forecasting (macro/micro trends, trend lifecycle)
- Collection cohesion & merchandising (line plans, SKU architecture)
- Fabric/material suitability & sustainability
- Silhouette & proportion principles
- Price architecture & target-customer fit

## Scoring Model
| Dimension | Range | Notes |
|-----------|-------|-------|
| Trend relevance | 0–100 | Weighted contribution to the composite index |
| Color/Material | 0–100 | Weighted contribution to the composite index |
| Collection cohesion | 0–100 | Weighted contribution to the composite index |
| Commercial viability | 0–100 | Weighted contribution to the composite index |
| Brand fit | 0–100 | Weighted contribution to the composite index |

Composite = weighted mean of dimensions (weights justified per case, surfaced to the user). Every dimension score must cite at least one framework criterion or evidence source.

## Skill File Format Specification
Frontmatter: `name`, `description`. Required sections in `main.md`: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates.

## E2E Execution Flow
1. Parse user request; if inputs missing, run intake questions.
2. Select framework based on subject characteristics.
3. Gather evidence (prefer Systematic Review > Meta-analysis > RCT/empirical > expert opinion).
4. Score each dimension with cited justification.
5. Build prioritized roadmap.
6. Run devil's-advocate quality gate; revise; present artifact.
- Error handling: missing data → state assumptions + confidence; tool failure → degrade to knowledge base and signal limitation.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: WGSN / Pantone trend reports, Business of Fashion (BoF) analysis, Journal of Fashion Marketing and Management, Vogue Runway / collection archives.
- Crawl queries: fashion trend forecast season, color palette trend report, sustainable textile innovation, merchandising line plan strategy.
- Append format: dated entries with Title, Authors, Year, Venue, DOI/URL, key finding, relevance.

## Supporting Tools Spec — `knowledge_updater.py`
- Inputs: source list + query list (above), `--since` date.
- Outputs: appended, de-duplicated entries in `SECOND-KNOWLEDGE-BRAIN.md`.
- Schedule: weekly cron.

## Quality Gates (must be true before final output)
- [ ] Framework selection justified
- [ ] Every score cites a framework criterion or evidence source
- [ ] Roadmap items have effort + impact + owner
- [ ] Assumptions and confidence stated; limitations disclosed
- [ ] Devil's-advocate pass completed

## Test Scenarios (≥5)
1. **SS collection trend check** — Designer shares a spring line. Expect trend-cycle positioning and palette critique.
2. **Cohesion problem** — Pieces feel disjointed. Expect line-plan and SKU-architecture roadmap.
3. **Sustainability positioning** — Brand wants eco-credibility. Expect material-suitability and greenwashing caution.
4. **Price-tier mismatch** — Luxury fabrics at mass price. Expect price-architecture realignment.
5. **New designer portfolio** — Grad collection. Expect commercial-viability vs creative-statement balance.

## Key Design Decisions
1. Research-first; no memory-only claims when search is possible.
2. Named frameworks only — never ad hoc criteria.
3. Framework-selector adapts to subject; no one-size scoring.
4. Multi-dimensional score + prioritized roadmap are mandatory outputs.
5. Self-improving knowledge base via weekly crawl.
