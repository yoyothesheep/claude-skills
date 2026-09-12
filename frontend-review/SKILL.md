---
name: frontend-review
description: Iteratively screenshot a running dev server with Puppeteer and fix UI issues until the interface matches design guidelines. Use when asked to review, polish, or QA frontend pages.
---

# Frontend Review

Uses Puppeteer to capture screenshots of a live dev server, compares them against project design guidelines, applies fixes, and repeats until the UI passes review.

## When to Use This Skill

- "Review the UI", "check how this looks", "polish the frontend"
- After implementing a feature, to visually QA before shipping
- "Make it match the design guidelines"
- Any time you need to verify visual correctness that type-checking and tests can't catch

## Setup

Read `CONFIG.md` in this skill directory (`.claude/skills/frontend-review/CONFIG.md`). If it doesn't exist, use these defaults:

```
DEV_URL=http://localhost:3000
PAGES=/
SCREENSHOT_PATH=.claude/review-screenshot.png
DESIGN_GUIDELINES_PATH=.claude/DESIGN-GUIDELINES.md
MAX_ITERATIONS=5
```

## Core Workflow

### Step 1: Verify dev server

```bash
curl -s -o /dev/null -w "%{http_code}" $DEV_URL
```

If you get anything other than 200, stop and tell the user to start the dev server first (e.g. `npm run dev`). Do not attempt to start it yourself.

### Step 2: Write the screenshot script

Write the following to `/tmp/frontend-review-screenshot.mjs`, overwriting any existing file:

```js
import puppeteer from 'puppeteer';
import { writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { mkdirSync } from 'fs';

const [,, url, outputPath, widthArg] = process.argv;
if (!url || !outputPath) {
  console.error('Usage: node frontend-review-screenshot.mjs <url> <outputPath> [width]');
  process.exit(1);
}

const width = parseInt(widthArg ?? '1440', 10);
const absOutput = resolve(process.cwd(), outputPath);
mkdirSync(dirname(absOutput), { recursive: true });

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width, height: 900, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
// Extra wait for animations to settle
await new Promise(r => setTimeout(r, 800));
await page.screenshot({ path: absOutput, fullPage: true });
await browser.close();
console.log(`Screenshot saved to ${absOutput}`);
```

This script uses the `puppeteer` package from the project's `node_modules`. Run it from the project root so that `import puppeteer` resolves correctly.

### Step 3: Capture and review each page

For each path in `PAGES` (comma-separated), capture **both viewports**:

```bash
# Desktop (1440px)
node /tmp/frontend-review-screenshot.mjs "$DEV_URL$PAGE" ".claude/review-desktop.png" 1440

# Mobile (375px — iPhone SE / standard mobile)
node /tmp/frontend-review-screenshot.mjs "$DEV_URL$PAGE" ".claude/review-mobile.png" 375
```

Read both screenshots. Read `DESIGN_GUIDELINES_PATH`. Produce a numbered list of specific UI issues, noting for each whether the issue appears on **desktop**, **mobile**, or **both**. Reference the exact element description and which guideline it violates.

### Step 4: Fix

Apply fixes to the relevant source files. Be surgical — one issue at a time if they're in different files, batched if they're in the same component.

### Step 5: Retake and re-evaluate

Retake both desktop and mobile screenshots for the same page. Re-read both images. Check whether the issues from Step 3 are resolved on both viewports. Note any regressions — a fix that breaks mobile is not a fix.

Repeat Steps 4–5 until either:
- No issues remain, or
- `MAX_ITERATIONS` is reached — at which point report remaining issues for the user to decide on

### Step 6: Report

Summarize:
- Pages reviewed
- Issues found and fixed (with before/after description)
- Any remaining issues and why they weren't auto-fixed
- Total iterations used

## Notes

- Always run the screenshot script from the **project root** so puppeteer resolves from `node_modules`
- If puppeteer isn't installed, stop and tell the user: `npm install --save-dev puppeteer`
- For pages that require auth or specific state (e.g. `/results`), note in your report that the screenshot may show an empty/redirected state and ask the user if they want to handle that separately
- `deviceScaleFactor: 2` produces retina screenshots — the image will be 2880px wide but represents a 1440px viewport
- If a page has entrance animations, the 800ms wait should cover most; increase if screenshots catch mid-animation states
