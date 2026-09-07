#!/usr/bin/env python3
"""
Builds the Allrounder Marketing site.

Edit the fragments in site/pages/ — each one is plain HTML plus a small
meta header — then run:  python3 site/build.py
Everything in site/pages/ is wrapped in the shared shell (head, nav,
footer, scripts) and written out as the pages that get published.

Do not hand-edit the generated .html files at the repo root or in
services/ — a rebuild overwrites them.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = Path(__file__).resolve().parent / "pages"

SITE_NAME = "Allrounder Marketing"
EMAIL = "mikeallrounder33@gmail.com"

# label, href, nav key
NAV = [
    ("Services", "services.html", "services"),
    ("Campaigns", "campaigns.html", "campaigns"),
    ("About", "about.html", "about"),
    ("Contact", "contact.html", "contact"),
]

SERVICES = [
    ("Growth Audit", "services/growth-audit.html", "growth-audit"),
    ("Brand & Positioning", "services/brand-positioning.html", "brand-positioning"),
    ("Campaign Planning", "services/campaign-planning.html", "campaign-planning"),
    ("Channel & Media Planning", "services/channel-media-planning.html", "channel-media-planning"),
    ("Content & Social Planning", "services/content-social-planning.html", "content-social-planning"),
]


def parse_meta(text):
    """Pull the <!--meta ... --> header off a fragment."""
    m = re.match(r"\s*<!--meta\n(.*?)\n-->\n", text, re.S)
    if not m:
        raise SystemExit("fragment is missing its <!--meta --> header")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


CURRENT = ' aria-current="page"'


def nav_html(base, active):
    links = "\n".join(
        '    <a href="%s%s"%s>%s</a>' % (base, href, CURRENT if key == active else "", label)
        for label, href, key in NAV
    )
    menu = "\n".join(
        '  <a href="%s%s"%s>%s</a>' % (base, href, CURRENT if key == active else "", label)
        for label, href, key in NAV
    )
    return f"""<nav id="nav">
  <a class="brand" href="{base}index.html">
    <img src="{base}assets/allrounder-mark.jpg" alt="" width="34" height="34">
    <span class="wm">Allrounder<span>Marketing</span></span>
  </a>
  <div class="nav-links">
{links}
  </div>
  <a class="nav-cta" href="{base}contact.html">Book a call</a>
  <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mobileMenu" aria-label="Menu"><span></span></button>
</nav>

<div class="mobile-menu" id="mobileMenu">
{menu}
  <a href="{base}contact.html" style="color:var(--gold)">Book a call</a>
</div>"""


def footer_html(base):
    svc = "\n".join(
        f'        <li><a href="{base}{href}">{label}</a></li>' for label, href, _ in SERVICES
    )
    return f"""<footer>
  <div class="fcol">
    <span class="wm" style="font-weight:300;letter-spacing:.24em;text-transform:uppercase;font-size:.9rem">{SITE_NAME}</span>
    <span class="eyebrow">Strategy &middot; Growth &middot; Results</span>
  </div>

  <div class="foot-nav">
    <div>
      <p class="h">Services</p>
      <ul>
{svc}
      </ul>
    </div>
    <div>
      <p class="h">Studio</p>
      <ul>
        <li><a href="{base}about.html">About</a></li>
        <li><a href="{base}campaigns.html">Campaign blueprints</a></li>
        <li><a href="{base}contact.html">Contact</a></li>
      </ul>
    </div>
    <div>
      <p class="h">Legal</p>
      <ul>
        <li><a href="{base}privacy.html">Privacy policy</a></li>
        <li><a href="{base}terms.html">Terms of use</a></li>
      </ul>
    </div>
  </div>

  <div class="fcol" style="text-align:right">
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <span class="eyebrow">&copy; <span id="yr">2026</span> {SITE_NAME}</span>
  </div>
</footer>"""


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#0b0908">
{robots}<link rel="canonical" href="{canonical}">
<link rel="icon" href="{base}assets/allrounder-mark.jpg">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{origin}/assets/allrounder-logo.jpg">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@300;400;500;600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}css/site.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="shell">

<!-- Turns the logo JPEG's black field transparent: alpha = luminance, then steepened. -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <filter id="knockout" color-interpolation-filters="sRGB">
    <feColorMatrix type="matrix" values="1 0 0 0 0
                                         0 1 0 0 0
                                         0 0 1 0 0
                                         .42 .72 .28 0 0"/>
    <feComponentTransfer><feFuncA type="linear" slope="3.4" intercept="-.16"/></feComponentTransfer>
  </filter>
</svg>

{nav}

<main id="main">
{content}
</main>

{footer}

</div><!-- /shell -->
<script src="{base}js/site.js"></script>
</body>
</html>
"""

# Where the site is actually served from. Canonical URLs, Open Graph tags and
# the sitemap are all built from this — point it at the real domain the moment
# one is live, then rebuild, or search engines index the wrong host.
ORIGIN = "https://mikeallrounder33-ux.github.io/allrounder-website"

# DRAFT MODE.
# True  = the site stays reachable by link, but tells search engines not to
#         index it. Use this until the legal placeholders are filled in.
# False = open for indexing. Flip this, run the build, commit and push when
#         the site is genuinely ready to be found.
DRAFT = True


def build():
    fragments = sorted(PAGES.rglob("*.html"))
    if not fragments:
        raise SystemExit("no fragments found in site/pages/")

    written = []
    for frag in fragments:
        rel = frag.relative_to(PAGES)
        meta, content = parse_meta(frag.read_text())
        depth = len(rel.parts) - 1
        base = "../" * depth
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            SHELL.format(
                title=meta["title"],
                description=meta["description"],
                canonical=ORIGIN + "/" + ("" if rel.as_posix() == "index.html" else rel.as_posix()),
                origin=ORIGIN,
                site_name=SITE_NAME,
                base=base,
                robots=(
                    '<meta name="robots" content="noindex, nofollow">\n'
                    if DRAFT or meta.get("noindex") else ""
                ),
                nav=nav_html(base, meta.get("nav", "")),
                footer=footer_html(base),
                content=content.rstrip(),
            )
        )
        written.append(rel.as_posix())

    # sitemap covers the indexable pages only
    urls = "\n".join(
        "  <url><loc>%s/%s</loc></url>" % (ORIGIN, "" if p == "index.html" else p)
        for p in written
        if p != "404.html"
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n"
    )
    (ROOT / "robots.txt").write_text(
        # Draft: ask crawlers to stay away entirely until the site is finished.
        "User-agent: *\nDisallow: /\n"
        if DRAFT else
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /site/\n"   # unwrapped source fragments, not real pages
        f"\nSitemap: {ORIGIN}/sitemap.xml\n"
    )

    print(f"built {len(written)} pages + sitemap.xml + robots.txt")
    if DRAFT:
        print("  DRAFT MODE: every page carries noindex and robots.txt "
              "disallows all. Set DRAFT = False to open it up.")
    for p in written:
        print("  ", p)


if __name__ == "__main__":
    build()
