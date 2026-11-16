#!/usr/bin/env python3
"""Build the GitHub Pages site from OVERVIEW.md into an APHL-themed page.

Run by the `pages` workflow, never committed output. It reads OVERVIEW.md,
embeds the Mermaid diagram so the browser renders it client-side (the same way
GitHub renders the block in the README). The viewer's browser measures and draws
with the one font it has loaded, and the script below waits for Libre Franklin
before rendering, so the node text does not clip. The converted Markdown is
wrapped in an APHL brand shell (teal palette, Franklin Gothic via the Libre
Franklin web fallback, an "APHL" wordmark, no logo).

No HTML or image file is tracked in the repository. The themed page is produced
here at build time and uploaded as the Pages artifact. The only tracked files
are this script and the workflow YAML, both inside the code allowlist.

Usage:
    python3 build_site.py OVERVIEW.md _site/index.html
"""
import pathlib
import re
import sys

import markdown

TEAL = "#00A0AF"
TEAL_MED = "#006E79"
TEAL_DARK = "#005057"

# Render the diagram in the viewer's browser, once Libre Franklin has loaded, so
# the measuring font and the drawing font are the same and node text does not
# clip (the failure the pre-rendered PNG showed in CI).
MERMAID_SCRIPT = """<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";
mermaid.initialize({startOnLoad:false});
const run = () => mermaid.run({querySelector:".mermaid"});
if (document.fonts && document.fonts.load) {
  Promise.all([
    document.fonts.load('400 1em "Libre Franklin"'),
    document.fonts.load('700 1em "Libre Franklin"')
  ]).then(run).catch(run);
} else {
  run();
}
</script>"""


def split_mermaid(md_text: str):
    """Return (markdown_without_mermaid, mermaid_block_or_None)."""
    m = re.search(r"```mermaid\n(.*?)```", md_text, re.S)
    if not m:
        return md_text, None
    return md_text[: m.start()] + "\x00MERMAID\x00" + md_text[m.end():], m.group(1)


CSS = """
:root {
  --teal:#00A0AF; --teal-med:#006E79; --teal-dark:#005057; --teal-light:#A3CCCC;
  --rust:#B42E34; --rust-dark:#862226; --rust-light:#F3D1D2;
  --ink:#2C2C2C; --body:#404040; --muted:#6a7378;
  --bg:#ffffff; --surface:#F3F6F7; --line:#E2E9EC;
  --sans:"Libre Franklin","Franklin Gothic Medium","Franklin Gothic",Arial,sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ink:#F2F6F7; --body:#D6DEE1; --muted:#9fb0b4;
    --bg:#14191A; --surface:#1C2325; --line:#2B3538; --teal-light:#2d4f54;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --ink:#F2F6F7; --body:#D6DEE1; --muted:#9fb0b4;
  --bg:#14191A; --surface:#1C2325; --line:#2B3538; --teal-light:#2d4f54;
  color-scheme: dark;
}
* { box-sizing:border-box; }
html,body { margin:0; }
body { background:var(--bg); color:var(--body); font-family:var(--sans);
  font-size:17px; line-height:1.65; -webkit-font-smoothing:antialiased; }
.wrap { max-width:880px; margin:0 auto;
  padding-left:max(20px,env(safe-area-inset-left,0));
  padding-right:max(20px,env(safe-area-inset-right,0)); }
header.band { background:var(--teal-dark); color:#fff; }
header.band .wrap { padding-block:40px; }
.wordmark { font-weight:800; letter-spacing:.18em; font-size:15px; color:var(--teal-light);
  margin:0 0 20px; text-transform:uppercase; }
.wordmark .dot { color:#fff; }
header.band h1 { color:#fff; font-size:clamp(27px,5vw,42px); margin:0; font-weight:800;
  line-height:1.15; text-wrap:balance; }
main .wrap { padding-block:14px 56px; }
h2 { color:var(--ink); font-size:clamp(20px,3vw,26px); margin:40px 0 8px; font-weight:700;
  text-wrap:balance; }
h3 { color:var(--ink); font-size:18px; margin:26px 0 6px; font-weight:700; }
p { max-width:66ch; }
a { color:var(--teal-med); }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) a { color:var(--teal); } }
hr { border:0; border-top:1px solid var(--line); margin:34px 0; }
blockquote { margin:20px 0; padding:2px 0 2px 18px; border-left:3px solid var(--teal);
  color:var(--body); }
code { background:var(--line); padding:1px 6px; border-radius:5px; font-size:.88em; }
pre { background:var(--surface); border:1px solid var(--line); border-radius:10px;
  padding:16px; overflow-x:auto; }
pre code { background:none; padding:0; }
.diagram { background:var(--surface); border:1px solid var(--line); border-radius:12px;
  padding:22px; margin:22px 0; overflow-x:auto; text-align:center; }
.diagram img, .diagram svg { max-width:100%; height:auto; }
/* The diagram is a <div class="mermaid"> the browser renders to SVG. A <div>,
   not a <pre>, so the label spans inherit the page sans font (Libre Franklin)
   rather than the monospace a <pre> would force, which is what kept the node
   text matching its measured box width instead of clipping. The sans font is
   set explicitly too, so the SVG is drawn in the same font mermaid measured
   with. Hide the raw source until mermaid has processed it. */
.diagram .mermaid { font-family:var(--sans); text-align:center; line-height:1.4; }
.diagram .mermaid:not([data-processed="true"]) { visibility:hidden; }
/* mermaid draws each label in an SVG <foreignObject> sized to the width it
   measured; the rendered text can be a hair wider and the foreignObject clips
   it. Let the label containers overflow instead of clipping those last glyphs. */
.diagram .mermaid foreignObject { overflow:visible; }
.diagram .mermaid foreignObject > div { overflow:visible !important; width:max-content !important;
  max-width:none !important; }
.diagram .mermaid .nodeLabel, .diagram .mermaid .edgeLabel, .diagram .mermaid .cluster-label {
  overflow:visible; white-space:nowrap; }
table { border-collapse:collapse; width:100%; margin:20px 0; font-size:15.5px; display:block;
  overflow-x:auto; }
th,td { text-align:left; padding:10px 14px; border-bottom:1px solid var(--line);
  vertical-align:top; }
thead th { background:var(--teal-med); color:#fff; font-weight:700; border-bottom:none; }
tbody tr:nth-child(even) { background:var(--surface); }
strong { color:var(--ink); }
footer { border-top:1px solid var(--line); color:var(--muted); font-size:14px; }
footer .wrap { padding-block:24px; }
"""


def main() -> None:
    src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "OVERVIEW.md")
    out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "_site/index.html")

    md_text = src.read_text(encoding="utf-8")
    # Drop the leading H1 (it becomes the header band) and split out the diagram.
    md_text = re.sub(r"^#\s+(.*)\n", "", md_text, count=1)
    body_md, mermaid = split_mermaid(md_text)

    html_body = markdown.markdown(body_md, extensions=["tables", "fenced_code", "sane_lists"])

    if mermaid is not None:
        # A <div>, not a <pre>: a <pre> carries the UA monospace font, which the
        # foreignObject label spans inherit for drawing while mermaid measured the
        # boxes with its sans measuring node, so every label overflowed and clipped.
        fig = (f'<div class="diagram"><div class="mermaid">'
               f'{markdown.util.code_escape(mermaid)}</div></div>')
        html_body = html_body.replace("<p>\x00MERMAID\x00</p>", fig).replace("\x00MERMAID\x00", fig)
        scripts = MERMAID_SCRIPT
    else:
        scripts = ""

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Where was this patient exposed?</title>
<meta name="description" content="How the melioidosis genome answers origin of exposure, and the scale at which it stops working.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap">
<style>{CSS}</style>
</head>
<body>
<header class="band">
  <div class="wrap">
    <p class="wordmark">APHL<span class="dot"> · </span>Pathogen Genomics</p>
    <h1>Where was this patient exposed?</h1>
  </div>
</header>
<main>
  <div class="wrap">
{html_body}
  </div>
</main>
<footer>
  <div class="wrap">
    Built from <code>OVERVIEW.md</code> ·
    <a href="https://github.com/PHemarajata/bp-recombination-aware-snps">source repository</a>
  </div>
</footer>
{scripts}
</body>
</html>"""

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({len(page.encode())} bytes)")


if __name__ == "__main__":
    main()
