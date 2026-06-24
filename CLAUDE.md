# CLAUDE.md — Fashion Design / Collection Analyzer (idea 125)

## Skill Identity
- **Name / slug:** `fashion-design-collection-analyzer`
- **Tagline:** Fashion Design / Collection Analyzer
- **Source idea:** #125 (`ideas.md`)
- **Cluster:** Design, Creative & Media (`design-creative-media`)
- **Current phase:** Phase 0-5 complete - production-ready / open-source release stage

## Problem This Skill Solves
Designers and brands need objective feedback on whether a collection is on-trend, cohesive, well-constructed (color/material), and commercially viable, beyond subjective taste.

This skill becomes **a fashion design critic and merchandiser who evaluates collections for trend relevance, color/fabric, cohesion, and commercial viability**. It is research-first, grounds every score in named world-renowned frameworks, challenges its own assumptions before concluding, and produces a professional artifact: a multi-dimensional score plus a prioritized improvement roadmap.

## Harness Flow Summary
1. **Intake** → `sub-profile-intake` gathers structured inputs.
2. **Gate / framework** → the correct evaluation framework is selected.
3. **Research** → WebSearch/WebFetch enrich evidence from authoritative sources (graceful degradation to SECOND-KNOWLEDGE-BRAIN.md if unavailable).
4. **Scoring** → `sub-scoring-engine` produces a 0–100 multi-dimensional score.
5. **Roadmap** → prioritized improvement plan (effort × impact).
6. **Quality gate** → devil's-advocate review before final output.

_No hard safety/compliance gate; standard quality gates apply._

## Sub-skills
- `skills/sub-profile-intake.md` — Capture brand, target customer, season, price tier, and collection pieces.
- `skills/sub-framework-selector.md` — Select trend, color, and merchandising frameworks for the segment.
- `skills/sub-scoring-engine.md` — Score trend relevance, color/material, cohesion, and commercial viability.
- `skills/sub-improvement-roadmap.md` — Recommend edits to line plan, palette, and materials ranked by sell-through/impact.

## Tools Required
- `WebSearch`, `WebFetch` — live evidence gathering
- `Read`, `Write` — artifact production
- `Bash`/`python` — run `tools/knowledge_updater.py`

## Knowledge Sources (crawl targets)
- WGSN / Pantone trend reports
- Business of Fashion (BoF) analysis
- Journal of Fashion Marketing and Management
- Vogue Runway / collection archives

## Supporting Tools
- `tools/knowledge_updater.py` — crawl4ai pipeline that grows `SECOND-KNOWLEDGE-BRAIN.md` (weekly cron recommended).

## Active Development Tasks
- [x] Scaffold all required deliverables
- [x] Author main harness + 4 sub-skills
- [x] Define scoring dimensions: Trend relevance, Color/Material, Collection cohesion, Commercial viability, Brand fit
- [x] Expand SECOND-KNOWLEDGE-BRAIN with verified seed entries and production crawler
- [x] Add regression test harness (16 tests) and detailed 5-scenario validation guide
- [x] Publish cross-skill references and shared scoring scale
- [x] Mark all phases 0-5 complete in PROJECT-DEVELOPMENT-PHASE-TRACKING.md

## Related Root Docs
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — living knowledge base
