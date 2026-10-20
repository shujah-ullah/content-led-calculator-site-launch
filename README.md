# Content-led Calculator Site Launch

A reusable Manus skill for turning validated keyword research into a content-led SEO website with embedded calculators, checklists, comparison worksheets, or other decision tools.

The skill covers the full execution path: research-backed page ownership, site architecture, crawler-visible static content, local-only calculator implementation, responsive navigation, technical SEO, content and link QA, mobile layout checks, Lighthouse validation, and production launch gates.

## What this skill is for

Use it when a niche or vertical has already been validated and the next step is to build a public site rather than only produce a keyword report. It is especially useful for calculator sites, finance decision tools, proposal review tools, home-improvement estimators, comparison worksheets, and other content-led products where the initial page content must be available to crawlers without JavaScript.

The default posture is static or statically generated pages with client-side calculations. The skill keeps user-entered values local unless a backend is explicitly approved and implemented with appropriate privacy controls.

## Package contents

```text
SKILL.md
references/
  calculator-spec.md       # Inputs, formulas, validation, accessibility, and boundaries
  keyword-page-map.md      # Keyword ownership and cannibalization rules
  launch-qa.md             # Final release checklist
scripts/
  audit_static_site.py     # Raw HTML, route, content, and link audit
  mobile_layout_check.cjs  # Chromium CDP mobile layout/runtime check
  run_lighthouse_batch.sh  # All-route mobile Lighthouse runner
```

## Typical workflow

1. Read the research report and identify the selected vertical, audience, geography, intent clusters, and evidence boundaries.
2. Assign one primary keyword cluster to each page and separate calculator ownership from supporting guide ownership.
3. Write the route architecture and calculator specifications before implementation.
4. Scaffold crawler-visible HTML, unique metadata, internal links, `manus-routes.json`, robots behavior, sitemap behavior, and a real 404.
5. Implement calculators locally with explicit formulas, validation, assumptions, accessible controls, reset/print behavior, and non-advisory result copy.
6. Build grouped navigation and footer hubs so no public route is orphaned.
7. Run static content/link QA, mobile emulation, and Lighthouse against every generated route.
8. Configure the real HTTPS public origin, rerun production checks, save the report, and commit only after all release gates pass.

## Usage examples

Run the static audit against a generated site:

```bash
python scripts/audit_static_site.py \
  --dist dist \
  --manifest dist/manus-routes.json \
  --json
```

Run Lighthouse mobile across all routes. The script defaults to a 390×844 viewport and accepts a custom viewport as optional arguments:

```bash
./scripts/run_lighthouse_batch.sh \
  https://example.com \
  dist/manus-routes.json \
  lighthouse-mobile
```

Run the Chromium mobile layout checker. Install its CDP dependency outside the production project, start Chromium with remote debugging, and pass the site origin and route manifest:

```bash
npm install --prefix /tmp/site-cdp --no-save chrome-remote-interface
chromium --headless --no-sandbox --remote-debugging-port=9223 about:blank
NODE_PATH=/tmp/site-cdp/node_modules node scripts/mobile_layout_check.cjs \
  http://127.0.0.1:3000 \
  dist/manus-routes.json \
  9223
```

## Release boundary

This skill does not authorize unsupported financial, tax, legal, lending, investment, energy, approval, savings, or incentive claims. It does not authorize lender rankings or collection of account numbers or other sensitive identifiers. Configure a real public origin before emitting absolute canonical, Open Graph, Twitter, or sitemap URLs; never use an internal preview URL as a production origin.

## Validation

The package is validated with the Manus skill validator. Its bundled static audit reproduces the reference site’s final result: 16 routes, zero broken links, zero broken fragments, zero stale-copy findings, zero orphan routes, and zero duplicate or high-similarity page pairs. The bundled mobile checker also passed all 16 reference routes with zero issues.
