# Personal Homepage

Personal portfolio site, pure HTML+CSS+JS, no frameworks.

## Quick reference
- **Live:** https://garymiley.github.io/
- **Repo:** GaryMiley/GaryMiley.github.io (main branch, GitHub Pages)
- **Entry:** `index.html` (self-contained, all inline)

## Edit & deploy
```bash
git add index.html && git commit -m "update" && git push
```
Changes go live in ~1-2 minutes via GitHub Pages.

## Architecture
- Single `index.html` with inline `<style>` and `<script>`
- Projects stored in browser localStorage (key: `portfolio_projects`)
- Images uploaded via FileReader → base64 data URIs
- No backend, no build step, no dependencies

## Network
GitHub blocked in China; git push requires proxy at `127.0.0.1:7897`.
