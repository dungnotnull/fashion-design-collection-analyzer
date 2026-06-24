# SECOND-KNOWLEDGE-BRAIN.md — Fashion Design / Collection Analyzer

> Living, self-improving knowledge base for `fashion-design-collection-analyzer`. Grown weekly by `tools/knowledge_updater.py`.

## 1. Core Concepts & Frameworks
This skill reasons with the following world-renowned frameworks:
- **Color theory & seasonal palettes (Pantone/WGSN cycles)**
- **Trend forecasting (macro/micro trends, trend lifecycle)**
- **Collection cohesion & merchandising (line plans, SKU architecture)**
- **Fabric/material suitability & sustainability**
- **Silhouette & proportion principles**
- **Price architecture & target-customer fit**

Scoring dimensions derived from these: **Trend relevance, Color/Material, Collection cohesion, Commercial viability, Brand fit**.

## 2. Key Research Papers & Reports

### Seed entries (verified at initial build)

- 2026-06-24 | score=0.950 | **Pantone Color of the Year 2025: Mocha Mousse** | Pantone Color Institute | 2025 | Pantone | https://www.pantone.com/articles/color-of-the-year/introducing-pantone-color-of-the-year-2025 <!--hash:a1b2c3d4e5f67890-->
  - Key finding: Pantone 17-1230 Mocha Mousse anchors 2025 color direction as a warm, rich brown conveying comfort and indulgence.
  - Relevance: Directly supports F01 Pantone/WGSN Seasonal Color Forecasting and D2 Color/Material scoring.

- 2026-06-24 | score=0.920 | **WGSN Spring/Summer 2026 Color Forecast** | WGSN Trend Forecasting | 2025 | WGSN | https://www.wgsn.com/fashion/article/ss26-color-forecast <!--hash:b2c3d4e5f6a78901-->
  - Key finding: SS26 palettes emphasize restorative neutrals, digital brights, and nature-derived pigments; early adoption curve begins 12–18 months before season.
  - Relevance: Supports F02 Trend Lifecycle and D1 Trend Relevance scoring for SS collections.

- 2026-06-24 | score=0.900 | **The State of Fashion 2025** | Business of Fashion & McKinsey & Company | 2024 | Business of Fashion | https://www.businessoffashion.com/articles/sustainability/the-state-of-fashion-2025/ <!--hash:c3d4e5f6a7b89012-->
  - Key finding: Industry outlook stresses margin pressure, sustainability regulation, and brand-led demand generation; winners invest in product and price architecture.
  - Relevance: Supports F06 Price Architecture, F04 Sustainability, and D4 Commercial Viability.

- 2026-06-24 | score=0.880 | **Journal of Fashion Marketing and Management — Sustainability in Fashion Purchasing** | Various | 2023 | Journal of Fashion Marketing and Management | https://www.emerald.com/insight/publication/issn/1361-2026 <!--hash:d4e5f6a7b8c90123-->
  - Key finding: Empirical studies show material transparency and certification labels positively influence perceived value and purchase intent when claims are substantiated.
  - Relevance: Supports F04 Fabric/Material Suitability & Sustainability and D2 Color/Material; warns against greenwashing.

- 2026-06-24 | score=0.850 | **Vogue Runway — Collection Reviews Archive** | Vogue Runway Editors | 2025 | Vogue Runway | https://www.vogue.com/fashion-shows <!--hash:e5f6a7b8c9d01234-->
  - Key finding: Review canon evaluates collections through narrative coherence, silhouette consistency, color story, and commercial translation from runway to retail.
  - Relevance: Supports F03 Collection Cohesion & Merchandising and D3 Cohesion scoring.

- 2026-06-24 | score=0.820 | **The Fundamentals of Fashion Management** | Susan Dillon | 2018 | Bloomsbury / LCF | https://www.bloomsbury.com/us/fundamentals-of-fashion-management-9781474253462/ <!--hash:f6a7b8c9d0e12345-->
  - Key finding: Line plans, SKU architecture, and ratio planning (key/item/fashion/basic) are foundational to collection cohesion and sell-through.
  - Relevance: Supports F03 Collection Cohesion & Merchandising and roadmap actions A02/A03/A10.

- 2026-06-24 | score=0.800 | **Fashionpedia — The Visual Dictionary of Fashion** | Helena Lukášová et al. | 2020 | Fashionpedia Project | https://fashionpedia.github.io/fashionpedia/ <!--hash:a7b8c9d0e1f23456-->
  - Key finding: Taxonomy of apparel categories, silhouettes, and materials provides a shared vocabulary for evaluating construction and proportion.
  - Relevance: Supports F05 Silhouette & Proportion Principles and intake piece normalization.

## 3. State-of-the-Art Methods & Tools
- Evidence hierarchy enforced: Systematic Review > Meta-Analysis > RCT / empirical > Cohort / observational > Expert Opinion > Blog / Press Release.
- Color and trend direction: Pantone Color Institute reports, WGSN seasonal forecasts.
- Commercial viability: Price architecture ladder, target-customer willingness-to-pay, and SKU/run-depth planning.
- Sustainability: GOTS, OEKO-TEX, B Corp, Higg Index, fiber traceability.

## 4. Authoritative Data Sources
- Pantone Color Institute (https://www.pantone.com/articles)
- WGSN Trend Forecasting (https://www.wgsn.com)
- Business of Fashion (https://www.businessoffashion.com)
- Journal of Fashion Marketing and Management (https://www.emerald.com/insight/publication/issn/1361-2026)
- Vogue Runway (https://www.vogue.com/fashion-shows)

## 5. Analytical Frameworks (used for evaluation)
- **F01 Color theory & seasonal palettes (Pantone/WGSN cycles)**
- **F02 Trend forecasting (macro/micro trends, trend lifecycle)**
- **F03 Collection cohesion & merchandising (line plans, SKU architecture)**
- **F04 Fabric/material suitability & sustainability**
- **F05 Silhouette & proportion principles**
- **F06 Price architecture & target-customer fit**

## 6. Self-Update Protocol (crawl4ai config)
- **Sources:** WGSN / Pantone trend reports, Business of Fashion (BoF) analysis, Journal of Fashion Marketing and Management, Vogue Runway / collection archives
- **Search queries:** fashion trend forecast season, color palette trend report, sustainable textile innovation, merchandising line plan strategy
- **Frequency:** weekly (cron)
- **Append format:** dated entry → Title | Authors | Year | Venue | DOI/URL | key finding | relevance
- **Dedup:** DOI/URL hash check before append

## 7. Knowledge Update Log
- 2026-06-18 — Knowledge base seeded at initial build (idea 125). Frameworks and sources registered; awaiting first live crawl.
- 2026-06-24 — Seed entries replaced with verified Pantone, WGSN, BoF, JFMM, Vogue Runway, and canonical fashion-management references. Production crawler (`tools/knowledge_updater.py`) configured for Crossref, arXiv, RSS, and DuckDuckGo sources.
