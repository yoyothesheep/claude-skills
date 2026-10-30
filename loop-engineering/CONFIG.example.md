# Loop Engineering Skill Configuration

# Directory paths (relative to repository root)
ACTIVE_DIR: active
SPECS_DIR: specs
PRODUCT_SPECS_DIR: specs/product
ENGINEERING_SPECS_DIR: specs/engineering
DECISIONS_DIR: history/decisions
COMPLETED_MILESTONES_DIR: history/milestones
TESTS_DIR: tests

# Living documentation files
LIVING_SPEC: specs/README.md
WORKING_RULES: CLAUDE.md

# Command configurations
TEST_COMMAND: uv run pytest
LINT_COMMAND: uv run ruff check .
FORMAT_COMMAND: uv run ruff format --check .

# UI verification viewports (px, widest first; optional). Every UI unit is checked at each width.
VIEWPORT_BREAKPOINTS: 1440, 1280, 991, 767, 479, 375
# Reference site for visual parity (blank if none)
PARITY_REFERENCE_URL: 

# Invariants & Policy Flags
REQUIRE_MAKER_VERIFIER_SEPARATION: true
AUTO_COMMIT: false
DETERMINISTIC_LOGIC_ISOLATED: true

# Test cases & Workshop reference
TEST_CASES: tests/TEST_CASES.md
WORKSHOP_URL: https://luma.com/22i8vgcm
