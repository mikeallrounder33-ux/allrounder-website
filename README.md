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

## Going live

The site is deployed and reachable, but `DRAFT = True` in `site/build.py`
puts `noindex` on every page and tells crawlers to stay out. It is visible
to anyone you send the link to; it will not turn up in search.

When the checklist below is done, set `DRAFT = False`, rebuild, commit and
push. That is the actual moment of publishing.

## Before going live

- [ ] Fill in every `[placeholder]` on **privacy.html** and **terms.html** —
      they render as highlighted boxes on the page so they're hard to miss.
      Have a lawyer read both; they are a solid starting draft, not legal advice.
- [ ] When a real domain is live, set `ORIGIN` in `site/build.py` to it and
      rebuild — canonical URLs, Open Graph tags and the sitemap all use it.
      It currently points at the GitHub Pages address.
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

## Where it's hosted

GitHub Pages, served from `main` at the repository root:
<https://mikeallrounder33-ux.github.io/allrounder-website/>

Every push to `main` redeploys automatically. Run `python3 site/build.py`
and commit the result before pushing, or the published pages won't reflect
your source edits.

### Adding a custom domain

1. Add a `CNAME` file at the repo root containing just the domain.
2. At the registrar, point the domain at GitHub Pages (an `ALIAS`/`ANAME`
   to `mikeallrounder33-ux.github.io`, or the four `A` records GitHub lists).
3. Set `ORIGIN` in `site/build.py` to the new domain, rebuild, commit, push.
4. Turn on "Enforce HTTPS" in the repository's Pages settings.
