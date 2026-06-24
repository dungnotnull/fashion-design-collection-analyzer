# 🧵 fashion-design-collection-analyzer

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()
[![Tests](https://img.shields.io/badge/tests-17%2F17%20passing-brightgreen.svg)]()
[![Open Source](https://img.shields.io/badge/open%20source-MIT%20style-lightgrey.svg)]()
[![Cluster](https://img.shields.io/badge/cluster-Design%2C%20Creative%20%26%20Media-ff69b4.svg)]()

> **A Claude Skill that turns Claude into a research-first fashion critic and merchandiser.**
> It evaluates collections across five dimensions — **trend relevance, color/material, cohesion, commercial viability, and brand fit** — grounding every judgment in named world-renowned frameworks and producing a prioritized improvement roadmap.

---

## ✨ Why this exists

Fashion design critique is too often reduced to taste, personal opinion, or Instagram intuition. Buyers, designers, and brands need **reproducible, evidence-graded evaluation**:

- Is this collection actually on-trend, or two seasons late?
- Does the palette follow credible seasonal color direction?
- Are the materials appropriate for the price tier and sustainability claims?
- Do the pieces form a coherent line plan and SKU architecture?
- Will it sell to the stated target customer?
- Does it strengthen the brand instead of diluting it?

`fashion-design-collection-analyzer` answers these questions with **named frameworks, explicit scores, and an actionable roadmap** — then challenges its own conclusions before finalizing the report.

---

## 🎯 What it does

Given a collection description, the skill runs a six-stage harness:

```
Intake → Framework Selection → Evidence Gathering → Scoring → Roadmap → Devil's Advocate
```

At the end you receive a professional artifact with:

1. **Summary** — subject, headline composite score, top 3 findings
2. **Scorecard** — 5 scored dimensions with weights, justifications, and citations
3. **Framework Selection** — which frameworks were chosen and why
4. **Detailed Analysis** — per-dimension narrative with evidence hierarchy
5. **Improvement Roadmap** — prioritized actions (effort × impact)
6. **Devil's Advocate Revision Log** — self-criticism and revisions
7. **Assumptions, Confidence & Limitations** — transparency
8. **Sources** — every citation used

---

## 🏗️ Architecture

### Harness stages

| Stage | Sub-skill | Purpose |
|-------|-----------|---------|
| 1 | `sub-profile-intake` | Capture brand, customer, season, price tier, pieces |
| 2 | `sub-framework-selector` | Choose the right evaluation frameworks |
| 3 | *Evidence gathering* | WebSearch / WebFetch / `SECOND-KNOWLEDGE-BRAIN.md` |
| 4 | `sub-scoring-engine` | 0–100 scoring across 5 dimensions |
| 5 | `sub-improvement-roadmap` | Prioritized action plan |
| 6 | *Quality gate* | Devil's-advocate review before output |

### Evaluation frameworks (named, citable)

| ID | Framework | Used for |
|----|-----------|----------|
| F01 | Pantone / WGSN Seasonal Color Forecasting | Color direction, palette coherence |
| F02 | WGSN Macro/Micro Trend Lifecycle | Trend timing, adoption curve |
| F03 | Collection Cohesion & Merchandising | Line plans, SKU architecture |
| F04 | Fabric/Material Suitability & Sustainability | Materials, sustainability claims |
| F05 | Silhouette & Proportion Principles | Fit, proportion, inclusivity |
| F06 | Price Architecture & Target-Customer Fit | Commercial viability, pricing |

### Five scoring dimensions

| Dimension | Default Weight | Framework basis |
|-----------|----------------|-----------------|
| Trend relevance | 0.20 | F02 |
| Color / Material | 0.20 | F01 + F04 |
| Collection cohesion | 0.20 | F03 |
| Commercial viability | 0.20 | F06 |
| Brand fit | 0.20 | F03 + F05 + F06 |

Composite = weighted mean. Weights can be adjusted per case as long as they sum to `1.00` and the rationale is stated.

---

## 🚀 Quick start

### 1. Use the skill

Provide a collection description and let the harness run:

> "I am launching SS 2026 womenswear for a premium contemporary brand. The line includes a linen blazer in oat, a silk slip dress in mocha, wide-leg trousers in ivory, and a cropped knit in terracotta. Target customer is 30–45, urban professional, US/EU. Price range $250–$650. Review trend and palette health."

The skill will ask clarifying questions if needed, select frameworks, gather evidence, score, and return the full report.

### 2. Refresh the knowledge base

```bash
# Preview what would be added (no writes)
python tools/knowledge_updater.py --dry-run --limit 10

# Append fresh, deduplicated entries to SECOND-KNOWLEDGE-BRAIN.md
python tools/knowledge_updater.py --since 2024-01-01 --limit 20
```

### 3. Run tests

```bash
python tests/test_harness.py
```

Expected output:

```
Ran 17 tests in ~25s
OK
```

---

## 📁 Repository layout

```
fashion-design-collection-analyzer/
├── skills/
│   ├── main.md                        # Main harness and output format
│   ├── sub-profile-intake.md          # Intake schema and validation
│   ├── sub-framework-selector.md      # Framework catalog and decision tree
│   ├── sub-scoring-engine.md          # 0–100 rubrics and scoring rules
│   ├── sub-improvement-roadmap.md     # Effort × impact roadmap
│   └── cross-skill-references.md      # Cluster sharing conventions
├── tools/
│   ├── knowledge_updater.py           # Production-grade knowledge crawler
│   └── knowledge_sources.json         # Configurable source list
├── tests/
│   ├── test_harness.py                # 17-test regression suite
│   └── test-scenarios.md              # 5 end-to-end scenarios
├── SECOND-KNOWLEDGE-BRAIN.md          # Living knowledge base (seeded)
├── SHARED-SCORING-SCALE.md            # Universal 0–100 scale for the cluster
├── PROJECT-detail.md                  # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Phase roadmap (all phases done)
├── CLAUDE.md                          # Skill identity and quick reference
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## 🧪 Test scenarios covered

1. **SS collection trend check** — palette and trend-cycle positioning
2. **Cohesion problem** — disjointed pieces and line-plan rebuild
3. **Sustainability positioning** — material credibility and greenwashing caution
4. **Price-tier mismatch** — luxury fabrics at mass price, realignment needed
5. **New designer portfolio** — commercial viability vs. creative statement

Each scenario has explicit expected behavior and pass criteria in `tests/test-scenarios.md`.

---

## 🧠 Knowledge base

`SECOND-KNOWLEDGE-BRAIN.md` is a living knowledge base grown weekly by the crawler. It is currently seeded with authoritative references including:

- Pantone Color of the Year 2025: Mocha Mousse
- WGSN Spring/Summer 2026 Color Forecast methodology
- Business of Fashion *State of Fashion 2025*
- *Journal of Fashion Marketing and Management* sustainability research
- Vogue Runway collection-review canon
- *Fundamentals of Fashion Management* (line-plan/SKU architecture)
- Fashionpedia taxonomy

The crawler supports:

- **Crossref** API for journal articles
- **arXiv** API for quantitative/textile research
- **RSS/Atom** feeds for fashion media
- **DuckDuckGo Lite** for broad trend queries
- **crawl4ai** fallback for pages without feeds

All entries are scored by **recency + domain relevance**, deduplicated by URL/title hash, and appended with a date stamp and hash comment.

---

## 🤝 Cross-skill wiring

This skill is part of the **Design, Creative & Media** cluster. It shares:

- A universal **0–100 scoring scale** (`SHARED-SCORING-SCALE.md`)
- A common **effort × impact** roadmap formula
- A standard hash-based deduplication format for knowledge bases
- Quality-gate conventions documented in `skills/cross-skill-references.md`

Sibling skills can reuse the intake, framework-selector, scoring-engine, and roadmap patterns by swapping in domain-specific dimensions and frameworks.

---

## 📦 Dependencies

```text
crawl4ai>=0.3.0   # optional fallback fetcher
```

All primary fetchers use Python's standard library (`urllib`, `xml.etree`, `json`, `hashlib`). No API keys are required for the default sources.

Install with:

```bash
pip install -r requirements.txt
```

---

## 🛡️ Quality gates

Before any final output, the skill checks:

- [ ] Framework selection justified with named frameworks
- [ ] Every dimension score has a cited justification
- [ ] Roadmap items have effort, impact, owner, and rationale
- [ ] Assumptions, confidence, and limitations stated
- [ ] Devil's-advocate review completed and logged
- [ ] Output contains all 8 required sections

If a gate fails, the skill halts and tells the user why.

---

## 📈 Project status

All development phases are **100% complete**:

| Phase | Status |
|-------|--------|
| 0 — Research & Skill Architecture | ✅ DONE |
| 1 — Core Sub-Skills | ✅ DONE |
| 2 — Main Harness + Quality Gates | ✅ DONE |
| 3 — SECOND-KNOWLEDGE-BRAIN Pipeline | ✅ DONE |
| 4 — Testing & Validation | ✅ DONE |
| 5 — Integration & Cross-Skill Wiring | ✅ DONE |

See `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` for the full roadmap and verification log.

---

## 📝 License

Open-source / production-ready. Use, fork, and contribute freely.

---

## 🙋 Contributors & feedback

Found a bug or want to extend the framework catalog? Open an issue or PR. The skill is designed to be modular: add a new framework in `skills/sub-framework-selector.md`, update the scoring rubric in `skills/sub-scoring-engine.md`, and add a test case in `tests/test_harness.py`.

Built with care for designers, merchandisers, and brands who want critique backed by evidence, not just opinion.
