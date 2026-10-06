#!/usr/bin/env python3
"""Static site generator for a personal blog/portfolio/CV.

Reads markdown files from content/, converts them to HTML, and writes a
fully static site to public/. No external server, no database.

Usage:
    python3 sitegen.py            # build to public/
    python3 sitegen.py --clean    # remove public/ first
"""

import argparse
import datetime
import html
import os
import re
import shutil
import sys

import markdown
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(HERE, "content")
STATIC_DIR = os.path.join(HERE, "static")
OUT_DIR = os.path.join(HERE, "public")

SITE = {
    "title": "Barbrzez",
    "tagline": "Personal blog, portfolio & CV",
    "author": "barbrzez",
}

MD_EXTENSIONS = ["extra", "sane_lists"]
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def escape(text):
    return html.escape(str(text), quote=True)


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_front_matter(raw):
    match = FRONT_MATTER_RE.match(raw)
    if not match:
        return {}, raw
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid front matter:\n{exc}")
    return meta, raw[match.end():]


def read_pages(subdir):
    directory = os.path.join(CONTENT_DIR, subdir)
    pages = []
    if not os.path.isdir(directory):
        return pages
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(directory, name)
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        meta, body = parse_front_matter(raw)
        slug = meta.get("slug") or os.path.splitext(name)[0]
        if subdir == "posts" and "date" in meta:
            date = meta["date"]
            if isinstance(date, str):
                date = datetime.date.fromisoformat(date)
        else:
            date = None
        pages.append(
            {
                "slug": slugify(slug),
                "title": meta.get("title", slug),
                "description": meta.get("description", ""),
                "tags": [t for t in (meta.get("tags") or []) if str(t).strip()],
                "date": date,
                "content_md": body,
            }
        )
    if subdir == "posts":
        pages.sort(key=lambda p: p["date"] or datetime.date.min, reverse=True)
    return pages


def render_markdown(text):
    return markdown.markdown(text, extensions=MD_EXTENSIONS)


def page(title, body, prefix, description=""):
    nav = [
        ("Blog", f"{prefix}index.html"),
        ("Tags", f"{prefix}tags/index.html"),
        ("About / CV", f"{prefix}about/index.html"),
    ]
    nav_html = "\n".join(
        f'<a href="{href}">{escape(label)}</a>' for label, href in nav
    )
    desc = escape(description) if description else escape(SITE["tagline"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} - {escape(SITE["title"])}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{prefix}style.css">
<script src="{prefix}gate.js"></script>
</head>
<body>
<header class="site-header">
<p class="site-title"><a href="{prefix}index.html">{escape(SITE["title"])}</a></p>
<p class="site-tagline">{escape(SITE["tagline"])}</p>
</header>
<nav class="site-nav">
{nav_html}
</nav>
<main class="site-main">
{body}
</main>
<footer class="site-footer">
<p>&copy; {datetime.date.today().year} {escape(SITE["author"])}</p>
</footer>
</body>
</html>
"""


def post_card(post, prefix):
    date = post["date"].strftime("%Y-%m-%d") if post["date"] else ""
    tags = " ".join(
        f'<a class="tag" href="{prefix}tags/{post_tag_slug(t)}/index.html">#{escape(t)}</a>'
        for t in post["tags"]
    )
    return f"""<article class="card">
<h2><a href="{prefix}posts/{post["slug"]}/index.html">{escape(post["title"])}</a></h2>
<p class="meta"><time>{date}</time></p>
<p class="excerpt">{escape(post["description"])}</p>
<p class="tags">{tags}</p>
</article>"""


def post_tag_slug(tag):
    return slugify(tag)


def build_post_pages(posts):
    for post in posts:
        out = os.path.join(OUT_DIR, "posts", post["slug"])
        os.makedirs(out, exist_ok=True)
        body_md = render_markdown(post["content_md"])
        date = post["date"].strftime("%Y-%m-%d") if post["date"] else ""
        tags = " ".join(
            f'<a class="tag" href="../../tags/{post_tag_slug(t)}/index.html">#{escape(t)}</a>'
            for t in post["tags"]
        )
        body = f"""<article class="post">
<h1>{escape(post["title"])}</h1>
<p class="meta"><time>{date}</time></p>
<p class="tags">{tags}</p>
{body_md}
</article>
<p class="backlink"><a href="../../index.html">&larr; All posts</a></p>"""
        write(
            os.path.join(out, "index.html"),
            page(post["title"], body, "../../", post["description"]),
        )


def build_tag_pages(posts):
    tags_dir = os.path.join(OUT_DIR, "tags")
    os.makedirs(tags_dir, exist_ok=True)
    by_tag = {}
    for post in posts:
        for tag in post["tags"]:
            by_tag.setdefault(tag, []).append(post)

    items = "\n".join(
        f'<li><a href="{post_tag_slug(tag)}/index.html">#{escape(tag)}</a> '
        f"({len(ps)})</li>"
        for tag, ps in sorted(by_tag.items())
    )
    body = f"<h1>Tags</h1>\n<ul class=\"tag-list\">{items}</ul>"
    write(
        os.path.join(tags_dir, "index.html"),
        page("Tags", body, "../"),
    )

    for tag, tagged in by_tag.items():
        cards = "\n".join(post_card(p, "../../") for p in tagged)
        body = f"""<h1>Posts tagged &quot;{escape(tag)}&quot;</h1>
<p class="backlink"><a href="../index.html">&larr; All tags</a></p>
{cards}"""
        out = os.path.join(tags_dir, post_tag_slug(tag))
        os.makedirs(out, exist_ok=True)
        write(
            os.path.join(out, "index.html"),
            page(f"Tag: {tag}", body, "../../"),
        )


def build_index(posts):
    cards = "\n".join(post_card(p, "./") for p in posts) or "<p>No posts yet.</p>"
    body = f"<h1>Blog</h1>\n{cards}"
    write(
        os.path.join(OUT_DIR, "index.html"),
        page("Blog", body, "./"),
    )


def build_about(about_page):
    if not about_page:
        return
    body = f"""<article class="post">
<h1>{escape(about_page["title"])}</h1>
{render_markdown(about_page["content_md"])}
</article>"""
    out = os.path.join(OUT_DIR, "about")
    os.makedirs(out, exist_ok=True)
    write(
        os.path.join(out, "index.html"),
        page(about_page["title"], body, "../", about_page["description"]),
    )


def write(path, content):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def copy_static():
    if not os.path.isdir(STATIC_DIR):
        return
    for root, _dirs, files in os.walk(STATIC_DIR):
        for name in files:
            src = os.path.join(root, name)
            rel = os.path.relpath(src, STATIC_DIR)
            dst = os.path.join(OUT_DIR, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    posts = read_pages("posts")
    about = read_pages("pages")
    about_page = about[0] if about else None

    build_index(posts)
    build_post_pages(posts)
    build_tag_pages(posts)
    build_about(about_page)
    copy_static()

    print(f"Built {len(posts)} posts into {OUT_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Build the static site.")
    parser.add_argument("--clean", action="store_true", help="remove output dir first")
    args = parser.parse_args()
    if args.clean and os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    build()


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
