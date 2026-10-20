# Keyword-to-page map

Use this reference during planning and before writing route metadata.

## Required columns

| Column | Rule |
|---|---|
| Keyword or query | Preserve the validated spelling and geography. Do not silently normalize away meaningful wording. |
| Cluster | Group close variants by searcher task, not by word overlap alone. |
| Intent | Label informational, commercial, support, comparison, or tool intent. |
| Priority | Mark one primary cluster per page; use secondary terms sparingly. |
| Target page | Assign one canonical owner route. |
| Evidence | Record the source, date, market, and any volume/KD/CPC values. |
| Notes | Capture exclusions, cannibalization risks, and content boundaries. |

## Ownership rules

- Give a head term one primary owner. Supporting pages should target adjacent questions, not duplicate the owner’s title and H1.
- Keep a calculator page focused on inputs, formulas, comparisons, and decision preparation.
- Keep a guide page focused on explanation, document review, FAQs, and questions to ask.
- Preserve commercial boundaries. A query about lenders does not authorize unsupported lender rankings.
- Use keyword evidence to prioritize pages, not to insert awkward exact-match phrases into every paragraph.
- Maintain the map in source data so the build checker can assert ownership and presence in raw HTML.

## Recommended route fields

Each public route should have: `path`, `kind`, `title`, `description`, `keywords`, `h1`, `lead`, `evidence`, `sections`, `related`, and, when applicable, `tool` or `embed`. Keep the URL stable when refining copy unless a redirect plan is explicitly approved.
