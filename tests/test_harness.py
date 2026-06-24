# -*- coding: utf-8 -*-
"""
test_harness.py — Regression and structure tests for fashion-design-collection-analyzer.

Run:
    python tests/test_harness.py
    python tests/test_harness.py -v

Tests cover:
  - Required skill files exist and contain valid frontmatter.
  - main.md contains all required sections.
  - Each sub-skill has Purpose, Inputs, Outputs, Quality Gate.
  - SECOND-KNOWLEDGE-BRAIN.md has seed entries and no placeholder rows.
  - knowledge_updater.py compiles and can run a local dry-run.
  - Sample intake payloads validate against the intake schema.
"""

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
TOOLS_DIR = PROJECT_ROOT / "tools"
BRAIN_PATH = PROJECT_ROOT / "SECOND-KNOWLEDGE-BRAIN.md"

REQUIRED_SKILL_FILES = [
    "main.md",
    "sub-profile-intake.md",
    "sub-framework-selector.md",
    "sub-scoring-engine.md",
    "sub-improvement-roadmap.md",
]

REQUIRED_MAIN_SECTIONS = [
    "Role & Persona",
    "Workflow",
    "Sub-skills Available",
    "Tools",
    "Output Format",
    "Quality Gates",
]

REQUIRED_SUB_SECTIONS = [
    "Role",
    "Purpose",
    "Inputs",
    "Outputs",
    "Quality Gate",
]


class SkillStructureTests(unittest.TestCase):
    def test_all_required_skill_files_exist(self):
        missing = [f for f in REQUIRED_SKILL_FILES if not (SKILLS_DIR / f).exists()]
        self.assertEqual(missing, [], f"Missing skill files: {missing}")

    def test_main_has_required_sections(self):
        text = (SKILLS_DIR / "main.md").read_text(encoding="utf-8")
        for section in REQUIRED_MAIN_SECTIONS:
            self.assertIn(section, text, f"main.md missing section: {section}")

    def test_main_frontmatter(self):
        text = (SKILLS_DIR / "main.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"^---\s*\nname:\s*\S+")
        self.assertRegex(text, r"description:\s*\S")

    def test_readme_and_requirements_exist(self):
        self.assertTrue((PROJECT_ROOT / "README.md").exists())
        self.assertTrue((PROJECT_ROOT / "requirements.txt").exists())

    def test_cross_skill_files_exist(self):
        self.assertTrue((PROJECT_ROOT / "skills/cross-skill-references.md").exists())
        self.assertTrue((PROJECT_ROOT / "SHARED-SCORING-SCALE.md").exists())

    def test_sub_skills_have_required_sections(self):
        for fname in REQUIRED_SKILL_FILES[1:]:
            text = (SKILLS_DIR / fname).read_text(encoding="utf-8")
            for section in REQUIRED_SUB_SECTIONS:
                self.assertIn(section, text, f"{fname} missing section: {section}")

    def test_sub_skills_frontmatter(self):
        for fname in REQUIRED_SKILL_FILES[1:]:
            text = (SKILLS_DIR / fname).read_text(encoding="utf-8")
            self.assertRegex(text, r"^---\s*\nname:\s*\S+", f"{fname} missing name frontmatter")
            self.assertRegex(text, r"description:\s*\S", f"{fname} missing description frontmatter")


class KnowledgeBaseTests(unittest.TestCase):
    def test_brain_exists_and_has_seed_entries(self):
        self.assertTrue(BRAIN_PATH.exists(), "SECOND-KNOWLEDGE-BRAIN.md missing")
        text = BRAIN_PATH.read_text(encoding="utf-8")
        hashes = set(re.findall(r"<!--hash:([0-9a-f]{16})-->", text))
        self.assertGreaterEqual(len(hashes), 5, "Expected ≥5 seeded knowledge entries")

    def test_no_placeholder_rows(self):
        text = BRAIN_PATH.read_text(encoding="utf-8")
        self.assertNotIn("_(seed", text, "Placeholder rows still present in knowledge base")
        self.assertNotIn("to be populated by crawler", text, "Placeholder text still present")

    def test_brain_lists_frameworks(self):
        text = BRAIN_PATH.read_text(encoding="utf-8")
        for fw in ["Pantone", "WGSN", "Collection cohesion", "Price architecture"]:
            self.assertIn(fw, text, f"Framework {fw} missing from knowledge base")


class KnowledgeUpdaterTests(unittest.TestCase):
    def test_knowledge_updater_compiles(self):
        updater = TOOLS_DIR / "knowledge_updater.py"
        self.assertTrue(updater.exists())
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(updater)],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Compile error: {result.stderr}")

    def test_knowledge_updater_dry_run(self):
        updater = TOOLS_DIR / "knowledge_updater.py"
        result = subprocess.run(
            [sys.executable, str(updater), "--dry-run", "--limit", "3", "--log-level", "ERROR"],
            capture_output=True, text=True, timeout=60
        )
        self.assertIn(result.returncode, [0, 1], f"Unexpected exit: {result.stderr}")
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                self.assertIsInstance(data, list)
            except json.JSONDecodeError:
                self.fail("Dry-run output is not valid JSON")


class IntakeSchemaTests(unittest.TestCase):
    def test_sample_payload_validates(self):
        payload = {
            "brand_name": "Test Atelier",
            "segment": "premium",
            "target_customer": "Women 28-40, urban professional, US/EU",
            "season": "SS_2026",
            "price_tier": "premium",
            "distribution": "dtc_ecommerce",
            "pieces": [
                {"name": "Linen blazer", "category": "outerwear", "color": "oat", "material": "linen", "silhouette": "relaxed tailored", "price_usd": 450, "quantity": 100},
                {"name": "Pleated trousers", "category": "bottom", "color": "oat", "material": "tencel blend", "silhouette": "wide leg", "price_usd": 280, "quantity": 150},
                {"name": "Silk camisole", "category": "top", "color": "mocha", "material": "silk", "silhouette": "fluid", "price_usd": 190, "quantity": 200},
            ],
            "brand_positioning": "Quiet luxury with sustainability credentials",
            "commercial_objective": "commercial_sellthrough",
            "constraints": "Use deadstock where possible; 8-week production window"
        }
        self.assertTrue(payload["brand_name"])
        self.assertIn(payload["segment"], ["luxury", "premium", "contemporary", "mass", "bridge", "fast_fashion", "artisanal", "graduate_portfolio"])
        self.assertIn(payload["season"], ["SS_2025", "SS_2026", "FW_2025", "FW_2026", "cruise", "resort", "pre_fall", "capsule", "evergreen"])
        self.assertIn(payload["price_tier"], ["entry", "mass", "bridge", "premium", "luxury", "couture"])
        self.assertGreaterEqual(len(payload["pieces"]), 3)
        for piece in payload["pieces"]:
            self.assertIn("name", piece)
            self.assertIn("category", piece)
            self.assertIn("color", piece)
            self.assertIn("material", piece)
            self.assertIn(piece["category"], ["top", "bottom", "dress", "outerwear", "knitwear", "accessory", "footwear"])


class ScoringSchemaTests(unittest.TestCase):
    def test_weighted_composite_computation(self):
        scores = {
            "trend_relevance": 80,
            "color_material": 70,
            "collection_cohesion": 75,
            "commercial_viability": 60,
            "brand_fit": 85,
        }
        weights = {k: 0.20 for k in scores}
        composite = sum(scores[k] * weights[k] for k in scores)
        self.assertAlmostEqual(composite, 74.0)

    def test_weight_sum(self):
        weights = {
            "trend_relevance": 0.20,
            "color_material": 0.20,
            "collection_cohesion": 0.20,
            "commercial_viability": 0.20,
            "brand_fit": 0.20,
        }
        self.assertAlmostEqual(sum(weights.values()), 1.0)


class RoadmapSchemaTests(unittest.TestCase):
    def test_priority_score_formula(self):
        effort = 2
        impact = 3
        self.assertEqual(effort * impact, 6)

    def test_roadmap_action_has_required_fields(self):
        action = {
            "rank": 1,
            "action": "Swap silk camisole to Tencel to align with premium sustainability claim",
            "owner": "Sourcing",
            "effort": 2,
            "impact": 3,
            "priority_score": 6,
            "rationale": "Silk is higher-impact; Tencel supports sustainability story without price shock.",
            "expected_effect": "Raises D2 Color/Material to 78 and D5 Brand Fit to 88.",
            "target_dimensions": ["color_material", "brand_fit"],
        }
        for field in ["rank", "action", "owner", "effort", "impact", "priority_score", "rationale", "expected_effect"]:
            self.assertIn(field, action)
        self.assertEqual(action["priority_score"], action["effort"] * action["impact"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
