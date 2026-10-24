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

# Invariants & Policy Flags
REQUIRE_MAKER_VERIFIER_SEPARATION: true
AUTO_COMMIT: false
DETERMINISTIC_LOGIC_ISOLATED: true
