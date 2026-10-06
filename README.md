# Personal Blog / Portfolio / CV

A minimal static site. Markdown files in `content/` are compiled to
static HTML and CSS by [`sitegen.py`](sitegen.py) (Python, `markdown` +
`PyYAML`). Deployed to GitHub Pages with a client-side password gate.

## Quick start

```bash
pip install -r requirements.txt
python3 sitegen.py --clean
python3 -m http.server -d public 8000   # preview at http://localhost:8000
```

## Writing content

Posts go in `content/posts/`, the About/CV page in `content/pages/about.md`.
Use YAML front matter:

```markdown
---
title: My Post
date: 2026-02-01
tags: [python, web]
description: Short summary shown on the blog index.
---

Body text in **markdown**...
```

- `tags` powers the tag pages under `/tags/`.
- Each post gets its own page at `/posts/<slug>/`.
- Static assets (CSS, JS, images) live in `static/` and are copied as-is.
- Site title/author are configured in the `SITE` dict in `sitegen.py`.

## Deploy (GitHub Pages)

1. In the repo settings: **Settings > Pages > Build and deployment > Source**
   set to **GitHub Actions**.
2. Push to `main`; the workflow (`.github/workflows/pages.yml`) builds and
   publishes the site automatically.

## Password protection - important caveat

GitHub Pages serves plain static files and **cannot do real password
protection** - anyone can fetch the raw HTML. The included `gate.js` is a
client-side password overlay: it hides the content in a browser until the
correct password is entered and remembers it for 30 days via a cookie.

This is a visual deterrent only, not security. If you need real
protection, host the site elsewhere (e.g. any server with HTTP basic auth)
or keep sensitive content out of the repo.

To change the password:

```bash
echo -n "yourpassword" | sha256sum
```

Put the resulting hex hash into `HASH` in `static/gate.js` (the default
password is `changeme`).
