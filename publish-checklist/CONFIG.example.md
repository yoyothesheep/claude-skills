# CONFIG — publish-checklist
# Copy this file to CONFIG.md and fill in your values. CONFIG.md is gitignored.

# Automated validation script command (use {slug} as placeholder)
PUBLISH_SCRIPT=python3 scripts/publish_check.py {slug}

# Path to the site-specific checklist file (page type detection + Phase 2 checks)
SITE_CHECKLIST_PATH=.claude/skills/publish-checklist/site-checklist.md
