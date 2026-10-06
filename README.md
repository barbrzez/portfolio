# Personal Blog / Portfolio / CV

A minimal static site built with [Hugo](https://gohugo.io). Markdown
files in `content/` are compiled to static HTML and CSS. Deployed to
GitHub Pages with a client-side password gate.

## Quick start

```bash
# install Hugo (https://gohugo.io/installation/), then:
hugo server              # preview at http://localhost:1313
hugo                     # build static site to public/
```

## Writing content

Posts go in `content/posts/`, the About/CV page is `content/about.md`.
Use TOML front matter:

```markdown
+++
title = 'My Post'
date = 2026-02-01
tags = ['python', 'web']
description = 'Short summary shown on the blog index.'
+++

Body text in **markdown**...
```

- `tags` powers the tag pages under `/tags/`.
- Site title/author are configured in `hugo.toml`.
- Templates live in `layouts/`, styles in `assets/css/style.css`.
- Static files (JS, images) go in `static/` and are copied as-is.

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

Put the resulting hex hash into `HASH` in `static/js/gate.js` (the default
password is `changeme`).
