# Hisoka GitHub Profile — V5 (Developer Card + Starred Repos Fix)

This is a complete GitHub profile package for `https://github.com/hisokaBK/hisokaBK`.

## Installation

1. Extract the ZIP.
2. Copy **README.md**, **assets/**, **scripts/**, and **.github/** into the repository root (preserve directories exactly).
3. Commit all files to the repository's **default branch**.
4. Visit **Actions > Update starred repositories badge > Run workflow** once to fetch the most recent number.
5. The workflow will then check for changes approximately every 6 hours, assuming Actions are enabled and the repository grants the workflow `contents: write` permissions. Scheduled jobs are not guaranteed to start exactly on time.

### What the Stars badge means

The GitHub profile `Stars` tab counts repositories **you have starred**. The old Shields.io `/github/stars/hisokaBK` endpoint tracks stars received by your repositories. Those are different measures.

The `STARRED REPOS` badge is initially **121**, matching the GitHub profile tab visible on November 18, 2026. It becomes automatically maintained after you upload and enable the included workflow.

If GitHub Actions are disabled or workflow push permissions are blocked, the initial value will remain static until you run a successful workflow. Manual workflow runs are available from Actions after the workflow is committed on the default branch.

### Developer card

`assets/developer-card.gif` is an animated graphic card created to reproduce the requested GitHub look (neon purple border, intro text and Hisoka portrait). It replaces the About Me free-floating text layout; a collapsible text equivalent is included below the artwork for accessibility and copying.

The card text is part of a GIF, because GitHub README rendering does not support arbitrary custom CSS for framed text/image overlays. Links to projects and contact still work as before.

### Visual content

- All four project covers link to their repositories.
- Tech Arsenal retains Postman and Swagger icons, backend tools, and DevOps & Workflow categories.
- Removed content stays removed: DESIGN/LOGIC/PRECISION banner, streak stats, and contribution graph.
- All local media references are relative to this repository root.

## Troubleshooting

If the badge never updates: open Actions > workflow runs to inspect errors, then check repository Settings > Actions > General > Workflow permissions. Repository policy may override requested permissions. GitHub may delay scheduled runs.
