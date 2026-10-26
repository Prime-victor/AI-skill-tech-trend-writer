# Article Structures

Mode A (news/trend) uses the first three structures. Mode B (firsthand/evergreen) uses the five that follow them.

## Default length targets

These are the ranges scripts/word_count.py applies with `--mode`. They count prose only: frontmatter and code blocks are excluded. A length the user asks for always wins; pass it with `--target MIN-MAX`.

| Structure | `--mode` | Words |
| --- | --- | --- |
| News article (Mode A default) | `news` | 800–1200 |
| Breaking-news brief | `brief` | 300–600 |
| Trend roundup or digest | `roundup` | 800–1200 |
| Deep-dive analysis | `deep-dive` | 1500–2500 |
| Firsthand post (Mode B default) | `firsthand` | 1000–1800 |
| Build log / project write-up | `build-log` | 1000–1800 |
| Lessons learned | `lessons-learned` | 900–1500 |
| Opinion / argument | `opinion` | 700–1200 |
| Evergreen explainer | `explainer` | 1200–2000 |
| Data-driven personal experiment | `experiment` | 1000–1800 |
| Any post saved to the portfolio blog | `portfolio` | 550–900 |

### Portfolio posts are capped at a 3–5 minute read

A post saved to the portfolio repo uses `--mode portfolio` whatever its structure. The structure still decides the sections; the cap decides how much goes in each. The blog shows reading time as total body words divided by 200, and it counts code blocks, tables, and the Sources list, which word_count.py does not. 550–900 prose words lands at 3–5 minutes on the page. The longer ranges above are for newsletters and other destinations, or for when the author asks for a long read.

To fit a structure into the cap:

- Keep the opening, the short answer, one table, one worked example, and the takeaways.
- Cut sections that restate the audience or the scope. One sentence in the opening covers both.
- Turn a list of three or more parallel items with reasons into a table (references/tables.md).
- Keep one code block or prompt, the one a reader would copy.
- Cite at most nine sources. Drop a source before dropping the claim's attribution.

## Tables

These structures normally carry at least one table: trend roundup (one summary row per update), deep-dive that compares products or options, build log (results), data-driven personal experiment (setup and results), and an explainer that weighs X against Y. Plan the table while outlining and follow references/tables.md.

# Mode A: news and trend structures

## Breaking-news brief

Use for one discrete announcement or development where speed and clarity matter more than extensive context.

1. Headline and dek
2. Lede: what happened, who announced it, and when
3. What changed: verified specifics
4. Why it matters: likely effect and limits
5. What happens next
6. Sources

Keep the background lean; add only context that helps readers interpret the news.

## Trend roundup or digest

Use for several related updates over a defined period, such as a weekly AI newsletter section or a product-launch roundup.

1. Headline and dek naming the theme and time window
2. Lede: the unifying shift
3. Update 1: development, evidence, implication
4. Update 2: development, evidence, implication
5. Update 3 (and optional Update 4): development, evidence, implication
6. The pattern: compare the updates without forcing a conclusion
7. Takeaway and sources

Give each item roughly equal weight unless one event clearly drives the story.

## Deep-dive analysis

Use when several credible developments support a broader shift and the reader needs context, trade-offs, and consequences.

1. Headline and dek
2. Lede: the central tension or thesis
3. Evidence of the shift
4. How the technology, market, or policy works
5. Who gains, who faces risk, and what is uncertain
6. Why it matters and what to watch next
7. Takeaway and sources

Build the thesis from evidence, not from a predetermined conclusion. Include credible counterevidence or constraints.

# Mode B: firsthand and evergreen structures

In every Mode B structure the thesis, the experience, and the numbers come from the author. Mark anything the author has not supplied with `[AUTHOR TO FILL: ...]`. Start from assets/article-template-firsthand.md and rename or reorder its sections to match the structure chosen here. See assets/example-outline-firsthand.md for a worked outline.

## Build log / project write-up

Use for "how I built X": one project, told from the problem through to a result the reader can inspect.

1. Headline and summary: what was built and the one result worth knowing
2. Problem: what was missing or painful, and for whom
3. Constraints: stack, time, budget, and what was deliberately out of scope
4. Approach: the design, and the alternatives that were rejected and why
5. Build: the key steps, with short code or config excerpts where they explain a decision
6. Results: numbers table, plus how each number was measured
7. What went wrong: bugs, dead ends, and surprises
8. Takeaways and what comes next
9. Links: repo, demo, and sources

Follow the decisions, not the commit history. Skip steps that taught nothing.

## Lessons learned

Use when the value is the reflection rather than the artifact: a retrospective on a project, a migration, a job, or a period of using a tool.

1. Headline and summary: the context and how many lessons
2. Context: what the author did, over how long, and at what scale
3. Lesson 1: the claim, the incident behind it, what the author does differently now
4. Lesson 2 (same shape)
5. Lesson 3 and optionally up to Lesson 5 (same shape)
6. What the author would still do the same
7. Takeaways and links

Each lesson needs a specific incident behind it. Cut any lesson that could have been written without doing the work.

## Opinion / argument

Use when the author holds a position and wants to defend it. The position is theirs; research tests and supports it.

1. Headline and summary: the position, stated plainly
2. Thesis: one sentence, plus why the author is placed to hold it
3. The case: two to four supporting points, each with firsthand evidence or a cited source
4. The strongest counterargument, stated fairly
5. Response: where the counterargument is right and where the thesis still holds
6. What would change the author's mind
7. Takeaway and sources

Label opinion as opinion. Do not soften the thesis into a both-sides summary, and do not strengthen it beyond what the evidence supports.

## Evergreen explainer

Use for "how X works" or "when to use X" posts that should stay accurate for a year or more and do not depend on a recent event.

1. Headline and summary: the question the post answers
2. Who this is for and what they should already know
3. The short answer
4. How it works: build up from one concrete example
5. A worked example the reader can run or follow
6. Common mistakes and edge cases
7. When not to use it, and the alternatives
8. Further reading and sources

Cite official documentation for behavior and name the versions the post was checked against. Where the author has used the thing in a real project, anchor the worked example there.

## Data-driven personal experiment

Use when the post rests on the author's own measurements: a before/after comparison, a benchmark, or a cost or token-usage optimization.

1. Headline and summary: the measured change, with both values
2. Question or hypothesis: what the author expected and why
3. Setup: workload, tools, versions, time period, and sample size
4. Baseline: the "before" numbers and how they were collected
5. Changes: each intervention, one at a time where possible
6. Results: before/after table with units, and the change attributable to each intervention
7. Caveats: what was not controlled, the sample size, and what may not generalize
8. How to reproduce: scripts, queries, or steps
9. Takeaways and links

Report absolute values next to every percentage. Present the result as what happened in this setup, not as a general law. Every figure in this structure is author-supplied and belongs in the hand-off checklist.
