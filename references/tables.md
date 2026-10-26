# Tables

Decide whether the post needs a table while outlining, not after drafting. A table that is planned gets its data collected during research or intake; a table that is added late gets filled with whatever is to hand.

## When a post needs a table

Use a table when the reader will compare values across two dimensions:

- three or more items compared on two or more attributes (models, tools, plans, releases)
- before/after or baseline/variant numbers
- benchmark or experiment results
- a timeline with a date, an event, and a consequence per row
- options with their trade-offs (option, cost, benefit, when to choose it)
- a roundup summary: one row per update, so the reader can scan before reading

Expect at least one table in these structures: trend roundup, deep-dive that compares products, build log (results), data-driven experiment (setup and results), and any "X vs Y" or "when to use X" explainer.

Do not use a table for a one-dimensional list (use bullets), for two items with one attribute (use a sentence), for narrative or reasoning, or for cells that each need more than about fifteen words.

## Plan the table before filling it

1. Write what the table shows as a title of at most twelve words, with no full stop. It goes directly above the table as a paragraph starting with `Table:`, for example `Table: Three models compared on price and context window`. The portfolio blog drops the label and renders the rest as the table's title bar. Do not write "The table shows..." as a sentence of body text.
2. Choose the rows (the things compared) and the columns (the attributes). Put the item name in the first column.
3. List every cell the table needs. This list is a research task in Mode A and an intake question in Mode B.
4. Collect the value for every cell before writing the table. If a column cannot be filled for most rows, drop the column. If a row cannot be filled for most columns, drop the row or say in prose why it is missing.

## Populate every cell

- No empty cells and no filler such as `-`, `N/A`, `TBD`, `?`, `...`, "various", or "varies".
- When a value does not exist or was not found, say which: "Not disclosed", "Not supported", "Not measured", or "None". These are information; a blank is not.
- Mode A: every value comes from a source found during research. Add a Source column with a link per row, or cite the sources in a `Sources:` caption under the table. Never fill a cell from memory or by analogy with a neighboring row.
- Mode B: every value comes from the author. A cell the author has not supplied is `[AUTHOR TO FILL: what is needed]`, never an estimate. Figures in tables go in the "Author-supplied, unverified" hand-off checklist like any other.
- Be specific: "128k tokens", not "large"; "$20 per user per month", not "paid"; "2026-09-14", not "recently".
- Put the unit in the column header when every row shares it (`Latency (ms)`), otherwise in each cell. Use the same unit and precision down a column.
- For before/after tables include both raw values and the change. Check the arithmetic of every computed cell.
- Make rows comparable: the same attribute measured the same way for every row. If one row was measured differently, say so under the table.
- Order rows deliberately (by the key metric, by date, or alphabetically) and say which if it is not obvious.

## Shape and size

- Three to six columns. Wider tables do not fit a phone screen; split them or move an attribute into prose.
- At least two body rows. A one-row table is a sentence.
- Keep cells short: a value or a phrase, not a paragraph.
- Use plain column headers of one to three words.
- Right-align numeric columns with `---:` so digits line up.
- Put the sources in a caption: one paragraph directly under the table that starts with `Sources:` (or `Source:`, or `Note:` for a caveat about how a row was measured). The portfolio blog renders that paragraph as a small caption attached to the table. Keep it to who supplied which column or row.
- After the caption, write one or two sentences of ordinary prose that say what the reader should take from the table. Do not mix the takeaway into the caption, and do not repeat every cell in prose.

## Markdown rules

    Table: Two models compared on context window and release date

    | Model | Context window (tokens) | Released | Source |
    | --- | ---: | --- | --- |
    | Example A | 200,000 | 2026-03-02 | [Release notes](https://example.com/a) |
    | Example B | 128,000 | 2026-04-18 | [Docs](https://example.com/b) |

- Leave a blank line before and after the table, or some renderers show it as plain text. That includes the blank line between the `Table:` title and the header row, and between the last row and a `Sources:` or `Note:` caption.
- The second line is the separator row: one `---` per column. Without it there is no table.
- Every row has the same number of cells as the header.
- Write a literal pipe inside a cell as `\|`.
- No line breaks, lists, or headings inside a cell. Links, bold, and inline code are fine.
- Do not put a table inside a code block unless the post is showing Markdown source.

## Check before hand-off

    python scripts/table_check.py content/posts/<slug>.md

It reports rows whose cell count does not match the header, missing separator rows, empty and filler cells, and tables with fewer than two body rows. Add `--require-table` for structures that should always contain one.
