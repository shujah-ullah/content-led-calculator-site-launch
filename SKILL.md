---
name: content-led-calculator-site-launch
description: Build and launch a content-led SEO website with embedded calculators or decision tools. Use for turning validated keyword research into page architecture, crawler-visible static content, interactive local-only tools, navigation, technical SEO, mobile checks, Lighthouse audits, and final content/link QA.
---

# Content-led calculator site launch

Use this skill when a validated niche or research report must become a public, content-led website with calculators, checklists, comparison worksheets, or other decision tools. The default implementation is a static or statically generated site with client-side interactivity and no collection of sensitive user data.

## Workflow

1. **Confirm evidence and scope.** Read the research report and spreadsheet or data source. Identify the selected vertical, audience, geography, commercial boundary, primary keyword clusters, secondary terms, and pages already promised. Do not invent demand, rankings, lender claims, rates, incentives, or conversion outcomes.

2. **Create page ownership.** Build a one-row-per-page keyword map using [keyword-page-map.md](references/keyword-page-map.md). Give each important cluster one primary owner. Keep supporting guides on adjacent terms instead of repeating the exact calculator target. Decide which pages are tools, guides, trust/policy pages, and the home route.

3. **Write the execution plan.** Record the site architecture, route list, calculator specifications, editorial phases, technical SEO requirements, and launch gates in the project. Use the existing project blueprint and design system; do not start a new design pass for an already approved visual direction.

4. **Scaffold the crawler-visible site.** Prefer static generation when the page body can be known before a visit. Every indexable route must render meaningful initial HTML, a unique title and description, one H1, semantic sections, internal links, and any calculator’s initial form or explanatory copy without waiting for JavaScript. Generate a real 404 response with `noindex,follow`.

5. **Add production-safe SEO metadata.** Emit `lang`, viewport, title, description, robots, and route-specific keywords when the host’s SEO validator requires them. Emit canonical, Open Graph, Twitter, and absolute sitemap URLs only when an explicitly configured real HTTPS public origin exists. Never derive those URLs from an internal preview host. Make the production build fail when an indexed release has no public origin.

6. **Build content in route-owned blocks.** Use concise present-tense copy, visible evidence boundaries, FAQs where useful, and contextual links. Remove roadmap language such as “future calculator,” “in development,” “initial scaffold,” or “coming soon” from public HTML. Do not use thin keyword-swapped pages. Keep advice educational, document-first, and explicit about what the tool cannot determine.

7. **Implement each tool from a specification.** Before coding, define inputs, outputs, formulas, validation, assumptions, edge cases, reset/print behavior, accessibility semantics, and data boundaries using [calculator-spec.md](references/calculator-spec.md). Keep calculations local unless the user explicitly authorizes a backend. Label example values, do not collect account numbers or sensitive personal information, and make uncertainty visible.

8. **Connect navigation and footer.** Use grouped Tools, Guides, and About/Standards navigation with active-route state, keyboard-friendly disclosure behavior, a mobile layout, skip-link support, a proposal/audit CTA, and a complete footer hub. Verify every public route has an inbound link through navigation, footer, or contextual content.

9. **Run static content/link QA.** Build the site, run `scripts/audit_static_site.py`, and run the project’s own checker. The audit must cover titles, H1/H2 presence, body depth, stale copy, internal route and fragment links, assets, orphan routes, exact duplicate bodies, high-similarity page pairs, FAQ/tool coverage, and raw HTML content. Fix failures before committing.

10. **Run mobile and Lighthouse QA.** Use `scripts/run_lighthouse_batch.sh` with explicit 390×844 mobile emulation and run `scripts/mobile_layout_check.cjs` when Chromium and `chrome-remote-interface` are available. Check every route for horizontal overflow, clipped elements, broken images, runtime exceptions, console errors, missing landmarks, and missing tool mounts. Treat local preview scores as a baseline; rerun against production after compression, fonts, origin, and routing are configured.

11. **Review release gates.** Before push/live, require: build pass; project checker pass; no broken links or orphan routes; no stale/placeholder copy; unique route content; one H1 per page; mobile overflow-free output; no runtime errors; a real 404; production origin configured; canonical/social/sitemap output verified; and final source/report committed. Use [launch-qa.md](references/launch-qa.md) as the final checklist.

## Tooling patterns

- For a new Manus website, use the Webdev project workflow and host-managed diagnostics before implementation. Keep `manus-routes.json` synchronized with source routes.
- Run `scripts/run_lighthouse_batch.sh ORIGIN MANIFEST OUTPUT_DIR`; do not use the invalid `--preset=mobile` flag. Use explicit `--form-factor=mobile` and `--screenEmulation.*` flags.
- For mobile layout checks, start Chromium with a remote debugging port and run `scripts/mobile_layout_check.cjs`. Install `chrome-remote-interface` in a temporary directory; do not add it to the production app unless the project needs it.
- Save a concise Markdown or HTML audit report in `docs/`, including scope, conditions, route-level findings, blockers, and next actions. Keep local-preview limitations separate from production conclusions.
- Commit the validated implementation and report; mirror or push to the project’s canonical repository only after build and QA pass.

## Guardrails

Do not publish personal financial, tax, legal, lending, debt, investment, energy, approval, or savings advice as a calculator result. Do not rank lenders or claim current rates, incentives, eligibility, transfer rules, or savings without dated, verified sources. Do not make the site indexable by guessing a domain. Keep user-entered tool values in the browser unless a backend is explicitly approved and privacy boundaries are implemented.
