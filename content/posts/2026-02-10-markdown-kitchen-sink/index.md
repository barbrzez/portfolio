+++
title = 'Markdown Kitchen Sink'
date = 2026-02-10
tags = ['example', 'markdown']
description = 'A demonstration of every markdown feature supported by this site.'
+++

This post exercises all markdown features available on the site.

## Text formatting

Here is **bold text**, *italic text*, ***bold italic***, ~~strikethrough~~,
`inline code`, and [a link](https://gohugo.io). Also an autolink:
<https://example.com>, and a footnote reference[^1].

## Headings

### This is an H3

#### This is an H4

##### This is an H5

###### This is an H6

## Lists

Unordered:

- First item
- Second item
  - Nested item
    - Deeply nested item
- Third item

Ordered:

1. Step one
2. Step two
   1. Sub-step
   2. Another sub-step
3. Step three

Task list:

- [x] Write the post
- [ ] Publish it
- [ ] Share it

## Blockquotes

> A simple blockquote.
>
> > A nested blockquote with more text.
> >
> > And a second line.

> A quote with **formatting** and a `code span`.

## Code blocks

Inline: use `hugo server` to preview.

Fenced code with a language tag (Chroma highlighting):

```python
def fibonacci(n):
    """Return the n-th Fibonacci number."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

for i in range(10):
    print(fibonacci(i))
```

```javascript
function greet(name) {
  const message = `Hello, ${name}!`;
  console.log(message);
}
```

```html
<p class="intro">Hello <strong>world</strong></p>
```

```bash
hugo new posts/my-post.md
git push origin main
```

A code block without a language tag:

```
plain text
    indented line
no highlighting applied
```

## Tables

| Feature    | Supported | Notes                     |
| ---------- | :-------: | ------------------------- |
| Headings   |    yes    | up to H6                  |
| Tables     |    yes    | with alignment            |
| Footnotes  |    yes    | via reference syntax      |
| Task lists |    yes    | checkboxes rendered       |

Alignment demo: left `:---`, center `:---:`, right `---:`

| Left | Center | Right |
| :--- | :----: | ----: |
| one  |   two   |  three |

## Images

With caption, responsive sizes, and lazy loading:

{{< figure src="cover.jpg" alt="An abstract example image with rectangles" caption="Figure caption via the figure shortcode." >}}

## Horizontal rule

Above the line.

---

Below the line.

## Footnotes

The first footnote is attached at the top[^1]. Here is another one[^note].

[^1]: This is the first footnote.
[^note]: This is the second footnote, with **formatting** inside.

## Escaping and special characters

Literal asterisks: \*not italic\*. Literal backticks: \`not code\`.
HTML entities: &copy; &amp; &mdash; and an em dash &mdash; directly.
