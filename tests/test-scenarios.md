# tests/test-scenarios.md — Fashion Design / Collection Analyzer

These scenarios validate the `fashion-design-collection-analyzer` harness end-to-end. Run the regression suite with:

```bash
python tests/test_harness.py
```

Then invoke the skill with each scenario input below and verify the pass criteria.

---

## Scenario 1: SS collection trend check

**Input prompt:**
> "I am launching a spring/summer 2026 womenswear collection for a premium contemporary brand. The line includes a linen blazer in oat, a silk slip dress in mocha, wide-leg trousers in ivory, and a cropped knit in terracotta. Target customer is 30–45, urban professional, US/EU. Price range $250–$650. What is the trend and palette health?"

**Expected harness behavior:**
- `sub-profile-intake` collects brand segment (premium contemporary), season (SS_2026), target customer, price tier, and 4+ pieces.
- `sub-framework-selector` activates F01 (Pantone/WGSN color), F02 (trend lifecycle), F03 (cohesion/merchandising), F05 (silhouette), and F06 (price architecture).
- Evidence gathering queries Pantone SS26 / WGSN palettes and verifies oat / mocha / terracotta direction.
- Scoring covers all 5 dimensions with cited justifications.
- Roadmap prioritizes palette edits and category balance by effort × impact.

**Pass criteria:**
- Framework selection is justified to the user.
- Every score cites a framework or source.
- Assumptions + limitations stated.
- Devil's-advocate pass evident in the revision log.
- Roadmap contains ≥4 actions with effort, impact, owner, and rationale.

---

## Scenario 2: Cohesion problem

**Input prompt:**
> "My 12-piece FW26 collection feels disjointed. I have a sequin evening gown, a puffer parka, a corporate trouser suit, a crochet cardigan, a leather mini skirt, and six printed tops in mismatched florals. Same brand, same season. Help."

**Expected harness behavior:**
- Intake flags `commercial_objective` and asks for brand positioning if missing.
- Framework selection heavily weights F03 (line plan / SKU architecture) and F05 (silhouette / proportion).
- Cohesion score is low (≤55) with explicit rationale.
- Roadmap leads with line-plan narrative and category-ratio realignment.

**Pass criteria:**
- D3 Collection Cohesion score ≤ 55 with cited reason.
- Top roadmap item is a structural cohesion action (line plan, narrative, or category ratio).
- At least one piece is recommended for removal or redesign.

---

## Scenario 3: Sustainability positioning

**Input prompt:**
> "We are repositioning our mass-market denim brand as sustainable. Collection uses organic cotton, recycled polyester, and claims 'carbon neutral.' Prices stay at $59–$89. Please review risks and credibility."

**Expected harness behavior:**
- Intake asks for certifications, fiber traceability, and third-party verification.
- F04 (materials / sustainability) and F06 (price architecture) are active.
- Scoring cautions against greenwashing if claims are unsupported.
- Roadmap includes certification and traceability actions before marketing.

**Pass criteria:**
- D2 Color/Material score reflects substantiation of sustainability claims.
- D4 Commercial Viability score comments on price-tier feasibility of sustainable materials.
- Roadmap contains a "greenwashing risk" action with owner = Sustainability Lead or Legal.
- Limitations section mentions verification gaps.

---

## Scenario 4: Price-tier mismatch

**Input prompt:**
> "We are a mass-market brand ($39–$129) and accidentally developed a 5-piece capsule using silk, cashmere, and fully-fashioned knits. Retail buyers love it but we cannot hit margin at our price tier. What should we do?"

**Expected harness behavior:**
- Intake captures the margin / price constraint.
- F04 (material-price suitability) and F06 (price architecture) are active.
- Commercial viability score is low (≤50) with material-price mismatch cited.
- Roadmap prioritizes material swaps and price architecture ladder.

**Pass criteria:**
- D4 Commercial Viability score ≤ 50 with cited F06 criterion.
- Top roadmap item is a material-price realignment or price-tier migration.
- At least one action has owner = Sourcing / Product Development.

---

## Scenario 5: New designer portfolio

**Input prompt:**
> "I am a fashion graduate and this is my final collection: 6 experimental looks with sculptural silhouettes, hand-painted fabrics, and one commercial jersey dress. I want gallery/press recognition but also need to show employers I can sell."

**Expected harness behavior:**
- Intake sets segment = graduate_portfolio and commercial_objective = awards_portfolio.
- Weighting adjusts to favor D5 Brand Fit and D3 Cohesion over D4 Commercial Viability.
- Framework selection includes F03 (cohesion / narrative) and F05 (silhouette / proportion).
- Roadmap balances creative statement with at least one commercial translation piece.

**Pass criteria:**
- Weighting rationale explicitly mentions graduate portfolio context.
- D5 Brand Fit score is the highest or second-highest dimension.
- Roadmap contains an action for a commercial "translation" piece without killing the statement.
- Devil's-advocate challenges whether the collection is too editorial to evaluate commercially.

---

## Regression Checklist (run after any edit)

- [ ] `python tests/test_harness.py` passes all tests.
- [ ] Framework selection always justified in final artifact.
- [ ] Scorecard includes all 5 dimensions with citations.
- [ ] Roadmap items carry effort + impact + rationale + owner.
- [ ] Graceful degradation when WebSearch/WebFetch unavailable (uses SECOND-KNOWLEDGE-BRAIN.md).
- [ ] Sources section lists every citation.
- [ ] Assumptions, confidence, and limitations stated.
- [ ] Devil's-advocate revision log included.
