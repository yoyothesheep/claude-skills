# CONFIG — publish-checklist
# Copy this file to CONFIG.md and fill in your values. CONFIG.md is gitignored.

# Automated validation script command (use {slug} as placeholder)
PUBLISH_SCRIPT=python3 scripts/publish_check.py {slug} --sitemap {sitemap_path}

# Path to the site-specific checklist file (page type detection + Phase 2 checks)
SITE_CHECKLIST_PATH=.claude/skills/publish-checklist/site-checklist.md
SITEMAP_PATH=public/sitemap.xml

# Content tracker — updated automatically on successful publish
TRACKER_AEO_CONTENT=docs/tracker/AEO_Content.md
CITATION_BASELINES=docs/tracker/citation_baselines/
