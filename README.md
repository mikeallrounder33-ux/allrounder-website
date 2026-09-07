# Allrounder Marketing — website

Static site. No framework, no dependencies, no build tooling beyond one Python script.

## Structure

```
index.html, about.html, …   generated pages — do not hand-edit
services/*.html             generated service pages — do not hand-edit
site/pages/*.html           SOURCE. Edit these.
site/build.py               wraps each source fragment in the shared shell
css/site.css                all styles
js/site.js                  all behaviour
assets/                     optimised logo files
```

## Editing

1. Edit the fragment in `site/pages/` — plain HTML, with a small `<!--meta -->`
   header for the page title and description.
2. Run the build:

   ```
   python3 site/build.py
   ```

That regenerates every page with the same nav, footer and `<head>`, plus
`sitemap.xml` and `robots.txt`.

Changing the nav, the footer or anything in `<head>` means editing
`site/build.py` once, rather than every page.

## Before going live

- [ ] Fill in every `[placeholder]` on **privacy.html** and **terms.html** —
      they render as highlighted boxes on the page so they're hard to miss.
      Have a lawyer read both; they are a solid starting draft, not legal advice.
- [ ] Set `ORIGIN` at the bottom of `site/build.py` to the real domain, then
      rebuild — canonical URLs, Open Graph tags and the sitemap all use it.
- [ ] Replace the placeholder testimonial in the homepage "stack" panel.
- [ ] Add the real social URLs (currently `#`) in `footer_html()` in `site/build.py`.
- [ ] Confirm the tool names in "The stack we run" are ones you actually use.
- [ ] Point the host's 404 handler at `404.html`.

## Deploying

Any static host works — Netlify, Vercel, Cloudflare Pages, GitHub Pages, or
plain shared hosting. Publish the repository root; there is nothing to compile.

The contact form posts to FormSubmit, which forwards to
`mikeallrounder33@gmail.com`. The first submission from a new domain triggers a
one-time confirmation email from FormSubmit that must be accepted.
