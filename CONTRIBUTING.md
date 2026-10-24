# Contributing

Know a small scientific code that deserves a place here? Contributions are
welcome — especially self-nominations.

## Inclusion criteria (all three required)

1. **Measured verification** — accuracy claims are checked against an exact
   / analytic reference, an independent method, or a hand-computed case, and
   the measured error is stated.
2. **Tests** — an automated test suite (unit tests and/or CI).
3. **Honest limits** — a written statement of what is *not* claimed.

## How to add an entry

1. Open a pull request adding one row to the appropriate table in
   `README.md`:

   ```
   | [Repo name](https://github.com/owner/repo) | One sentence: what it verifies and against what reference |
   ```

2. Keep the description factual (no marketing adjectives).
3. Large, well-known projects belong in their existing rows' sections; small
   verified codes get their own row.

Suggestions and corrections as issues are welcome too.

## Check a catalogue edit locally

Run `python scripts/check_catalog.py` before submitting an entry. The offline
checker catches malformed repository links, duplicates across sections, missing
verification descriptions and broken table columns. Escape a literal pipe in
a description as `\|`. It does not check website availability or prove numerical
claims; inclusion criteria still require human review of the linked evidence.

Run its regression suite with `python -m unittest discover -s tests -v`.
Both commands use only the Python standard library.
