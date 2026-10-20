# Launch QA checklist

Use this after the feature work is complete. Keep evidence with the project report.

## Build and route integrity

- [ ] Run the production-equivalent build and project checker.
- [ ] Confirm every source route has generated HTML and `manus-routes.json` matches it.
- [ ] Confirm unknown paths return a real 404 and the 404 page is `noindex,follow`.
- [ ] Confirm the production build refuses to emit indexable absolute metadata without a real HTTPS origin.

## Content and links

- [ ] Each page has meaningful raw HTML, one H1, H2 sections, and route-specific title/description.
- [ ] No placeholder, roadmap, future-tool, unsupported ranking, or guarantee language remains.
- [ ] Every internal route, fragment, stylesheet, script, and asset reference resolves.
- [ ] No route is orphaned; no exact duplicate or suspiciously similar page pair remains.
- [ ] Tool routes contain their initial form/mount; guides contain their intended explanatory/FAQ content.

## Metadata and structured data

- [ ] Titles and descriptions meet the host’s thresholds and are unique.
- [ ] Canonical, Open Graph, Twitter, and sitemap URLs use the real public origin.
- [ ] Robots policy matches the intended public/private boundary.
- [ ] JSON-LD is accurate, route-appropriate, and reflects visible content; do not add fake authors, dates, offers, ratings, or reviews.

## Mobile and runtime

- [ ] Test all routes at 390×844 or a comparable mobile viewport.
- [ ] Confirm no horizontal overflow, clipped content, broken images, runtime exceptions, or console errors.
- [ ] Confirm one main landmark, one H1, viewport meta, navigation, footer, and expected interactive mounts.
- [ ] Exercise representative tool validation, reset, print, and result states.

## Performance and release

- [ ] Run Lighthouse mobile on every public route; record performance, accessibility, best-practices, SEO, FCP, LCP, CLS, and TBT.
- [ ] Treat local preview scores as a baseline. Rerun against production with compression, font loading, caching, origin, and routing active.
- [ ] Review render-blocking CSS/fonts, compression, unused CSS, images, and third-party requests.
- [ ] Save the report, commit the result, and verify the canonical repository contains the same source and build checks.
