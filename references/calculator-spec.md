# Calculator specification

Complete this specification before implementing each interactive tool.

## Purpose and boundary

- Searcher question:
- Page owner and route:
- What the tool calculates or organizes:
- What it does not determine:
- Data boundary: local browser, server, or external API:

## Inputs

For every input, record label, `name`, type, unit, default/example status, min/max, step, required state, source expectation, and whether the value is sensitive. Never request account numbers, Social Security numbers, signed documents, or other personal identifiers for a local decision worksheet.

## Outputs

Define the result cards, comparison rows, warnings, assumptions, source dates, and printable summary. Every output must identify whether it is a scenario, documented term, user assumption, or unresolved question.

## Calculation model

Document formulas, units, rounding, zero-interest or zero-value branches, payment timing, amortization assumptions, escalators, horizon treatment, and any fields deliberately excluded. Keep the formula in a testable pure function where possible.

## Interaction behavior

- Render an informative initial HTML form before JavaScript executes.
- Validate field-specific errors and set `aria-invalid` only on affected controls.
- Use labels associated with controls, a live status/result region, keyboard-friendly controls, and visible focus treatment.
- Provide reset behavior when state can be changed and print behavior when the output is a useful record.
- Keep example inputs clearly marked and never imply that defaults came from the user’s documents.
- Test empty, invalid, boundary, zero-interest, and normal scenarios.

## Content and compliance

State that the result is educational arithmetic or an inspection worksheet, not approval, an offer, tax treatment, a savings guarantee, or personalized financial advice. Explain that controlling agreements, current statements, formal payoff quotes, or qualified professionals govern where applicable.
