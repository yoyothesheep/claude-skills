# CONFIG.example.md — Product Scenarios Configuration Template
# Copy this file to `CONFIG.md` in this skill directory (`.claude/skills/product-scenarios/CONFIG.md` or `.agents/skills/product-scenarios/CONFIG.md`).
# `CONFIG.md` is gitignored.

PROJECT_NAME: "Example Project"

DOMAIN_ENTITIES:
  - name: "Entity"
    description: "Primary domain object"
  - name: "Attachment"
    description: "Supporting or auxiliary asset"

# Domain-specific AI behaviors to test
DOMAIN_AI_SCENARIOS:
  - id: "multi_asset_grouping"
    description: "Associating multiple input assets into a single cohesive entity"
  - id: "multi_entity_extraction"
    description: "Extracting multiple distinct entities from a single input asset"
  - id: "overlap_deduplication"
    description: "Recognizing overlapping/repeated content across sequential inputs (e.g. scrolling captures)"
  - id: "redundant_instruction_filtering"
    description: "Filtering repeated text from secondary/visual step annotations"

# Project-specific non-negotiable invariants
INVARIANTS:
  - "Never silently discard user input without explicit feedback or recovery."
  - "Every AI-generated modification must be human-inspectable."
