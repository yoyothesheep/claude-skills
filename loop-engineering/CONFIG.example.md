# Loop Engineering Skill Configuration

# Directory paths (relative to repository root)
SPECS_DIR: specs
DECISIONS_DIR: decisions
HISTORY_UNITS_DIR: history/units
TESTS_DIR: tests

# Living documentation files
LIVING_DESIGN: DESIGN.md
LIVING_SPEC: SPEC.md
WORKING_RULES: CLAUDE.md

# Command configurations
TEST_COMMAND: uv run pytest
LINT_COMMAND: uv run ruff check .
FORMAT_COMMAND: uv run ruff format --check .

# Invariants & Policy Flags
REQUIRE_MAKER_VERIFIER_SEPARATION: true
AUTO_COMMIT: false
DETERMINISTIC_LOGIC_ISOLATED: true
