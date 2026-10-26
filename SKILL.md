---
name: tech-trend-writer
description: >-
  Write developer-blog and portfolio articles in two modes. News/trend mode: rigorously
  sourced articles, newsletter pieces, LinkedIn posts, and roundups about recent technology
  trends, product launches, AI news, and industry updates. Firsthand/evergreen mode:
  portfolio posts built from the author's own work, such as project write-ups, build logs,
  "how I built X" posts, lessons learned, personal-data experiments with before/after
  numbers, opinion pieces, and explainers. Use this skill eagerly for any request that
  resembles "write an article about...", "cover the latest in...", "tech roundup",
  "write up my project", "blog post about how I built...", "turn my notes into a post",
  or "what I learned from...", even when the user never mentions a skill.
compatibility: >-
  Web search is required for news/trend mode and recommended for firsthand mode. The
  optional scripts need Python 3 (standard library only).
---

# Tech Trend Writer

## Choose the mode first

- **Mode A: News/trend.** The subject is something other people recently shipped, announced, or reported. The value comes from research.
- **Mode B: Firsthand/evergreen.** The subject is the author's own project, data, experience, or opinion, or an explainer that does not depend on a recent event. The author supplies the argument and experience; you supply research, structure, fact-checking, and polish.

Selection rules:

1. Recent launches, announcements, "the latest in", roundups, or a named time window: Mode A.
2. "I built", "my project", "what I learned", the author's own numbers, notes, or repo, an opinion, or a timeless "how X works": Mode B.
3. Mixed requests, such as the author's take on a recent launch: use Mode B when the author's experience or argument is the spine, and apply the Mode A sourcing rules to every news claim.
4. A request to make an existing post sound like the author is a Mode B revision: follow references/voice.md, keep every technical claim, quote and code block, and keep the length within about 10%.
5. If the mode is still unclear, ask one question: "Is this about recent news, or about your own project or experience?" Then proceed.

State the chosen mode in one line before starting.

## Mode A workflow: news/trend

1. Confirm the topic, angle, target length, tone, and publishing format (blog post, newsletter, LinkedIn post, or similar) when missing. Do not stall: if the request is clear, make a sensible assumption and state it briefly.
2. Research developments from the last 1–4 weeks unless the user specifies another window. Run several focused web searches. Prefer primary sources—company newsrooms, release notes, filings, and official documentation—then corroborate with reputable technology reporting rather than aggregators.
3. Before drafting, open references/article-structures.md to select a shape suited to the request, then open assets/article-template.md and build a concise outline from it. Decide now whether the piece needs a table (references/tables.md) and list the cells it requires, so research collects a sourced value for each one.
4. Draft from that outline. Open and follow references/style-guide.md while writing. Use assets/headline-formulas.md when proposing or selecting a headline. Fill every table cell with a specific, sourced value; never leave a cell blank or fill it from memory.
5. Open references/fact-check-checklist.md and run every applicable check against the finished draft; revise before presenting it.
6. Optionally run scripts/link_checker.py on the Markdown file to detect broken cited links. Pass --search-results with a saved search-results export to also verify that cited URLs came from research rather than being fabricated. Run scripts/table_check.py when the article contains or should contain a table. Run scripts/word_count.py with `--mode portfolio` for a post saved to the portfolio repo, or `--mode news` (or `brief`, `roundup`, `deep-dive`) for other destinations; `--target MIN-MAX` overrides both.
7. Save the final article as a Markdown file (see Output below), include a source list, and present the finished article or its saved path to the user.

## Mode B workflow: firsthand/evergreen

**Hard rule: never invent experiences, metrics, quotes, or outcomes.** When the author has not supplied a number, anecdote, or result, write a clearly marked `[AUTHOR TO FILL: what is needed]` placeholder instead. Do not estimate, round up, or fill the gap with a plausible example.

1. Intake. In one message, ask only for what is still missing:
   - (a) the thesis in one sentence
   - (b) what they actually did
   - (c) real numbers or metrics: before/after, time, cost, tokens
   - (d) what went wrong or surprised them
   - (e) links to the repo or demo

   Read any notes, repo, or logs they share before asking. If they want a draft before answering, proceed and use placeholders.
2. Choose a Mode B structure from references/article-structures.md, then outline from assets/article-template-firsthand.md. assets/example-outline-firsthand.md shows a finished outline. Plan the tables at this point (references/tables.md): results, before/after numbers, and option comparisons belong in one, and any cell the author has not supplied becomes an intake question or an `[AUTHOR TO FILL: ...]` cell. Share the outline when placeholders outnumber supplied facts.
3. Research is supporting only. Verify the technical claims in the author's account and cite documentation or primary sources for background. The argument and the experience stay the author's: do not replace their thesis with a consensus view, and tell them directly when a source contradicts them.
4. Draft in the first person: concrete and specific, in the author's voice. Follow the firsthand section of references/style-guide.md and all of references/voice.md: open with a real moment, take two or three stances where the reader wants a recommendation, show one real artifact, vary section length, and read it aloud. Mine the conversation, the author's files and git history for real material before writing a placeholder. The ban on hype language applies in full.
5. Fact-check. Run references/fact-check-checklist.md, including its firsthand section, against the draft. Do not silently trust author-supplied figures: end your reply (outside the post body) with a short "Author-supplied, unverified" checklist naming each figure, plus a list of every remaining placeholder.
6. Save the post as a Markdown file (see Output below) with `status: draft`.
7. Run scripts/frontmatter_check.py, scripts/table_check.py, and scripts/link_checker.py on the saved file, and scripts/word_count.py with `--mode portfolio` (the structure's own `--mode` only when the post is not for the portfolio blog). Fix what they report, then present the post or its path to the author.

## Sourcing and citations

- Never invent statistics, quotes, dates, URLs, product details, or sources.
- Attribute factual and analytical claims close to the claim; use direct links in the Sources list.
- Keep quotations short. Prefer accurate paraphrase and preserve the source's meaning, especially for copyrighted reporting.
- Prefer sources published within the relevant recency window; label older context as background when it is needed.
- Distinguish a verified fact from analysis, forecast, or opinion. Resolve material disagreements with the newest authoritative source or disclose the uncertainty.

## Output

Portfolio posts are Markdown files with YAML frontmatter, kept in the portfolio repo and versioned in git. Do not write to a database or assume a dashboard editor.

- Default path: `content/posts/<slug>.md`. Use a different directory when the user names one or the repo already has its own convention.
- Frontmatter fields, in order: `title, slug, date, tags, summary, status, repo_url, canonical_url` (the last is optional). New posts are `status: draft`; only the author publishes.
- Skip frontmatter for newsletter, LinkedIn, or other non-portfolio destinations.
- Length: a portfolio post is a 3–5 minute read whatever its structure. Check it with `scripts/word_count.py --mode portfolio` and cut to fit before hand-off; references/article-structures.md says what to cut. Use the longer per-structure ranges only for other destinations or when the author asks for a long read.
- Reading experience: follow the portfolio section of references/style-guide.md (hook, headings, one scannable element per screen). Draw the post's cover illustration to references/cover-images.md, save it as `public/blog/<slug>.svg`, and set `image: /blog/<slug>.svg` with an `image_alt` description; use an author-supplied image instead when there is one.

Open references/output-format.md for field rules and path details.

## Scripts

Python 3 standard library only. Each exits non-zero when it finds a problem.

- `python scripts/frontmatter_check.py <post.md>`: required fields, slug, date, and status values. Leftover `[AUTHOR TO FILL` placeholders are a warning in a draft and an error when `status: published`.
- `python scripts/table_check.py <post.md> [--require-table]`: empty or filler cells, rows that do not match the header, and missing separator rows.
- `python scripts/link_checker.py <post.md> [--timeout 10] [--search-results <file>]`: reports redirects, 4xx, 5xx, and timeouts separately.
- `python scripts/word_count.py <post.md> --mode <name>`: counts prose only (no frontmatter or code blocks). Modes and their default ranges are listed in references/article-structures.md; `portfolio` is the 3–5 minute cap for posts on the blog.

## Resource pointers

- Open references/output-format.md before saving a post to the portfolio repo.
- Open references/cover-images.md before drawing a post's cover illustration.
- Open references/tables.md while outlining any post that compares items or reports numbers, and again before filling a table.
- Open references/article-structures.md before outlining to choose a structure for the chosen mode.
- Open references/style-guide.md before drafting or revising for voice and formatting rules.
- Open references/voice.md before drafting any first-person post, and whenever the author asks for a post to sound more like them, less like AI, or less like documentation.
- Open references/fact-check-checklist.md immediately before finalizing to audit facts, dates, quotes, and citations.
- Use assets/article-template.md as the working outline and final-article scaffold for Mode A, and assets/article-template-firsthand.md for Mode B.
- Open assets/example-outline-firsthand.md to see a worked Mode B outline with placeholders.
- Use assets/headline-formulas.md only when generating or refining headlines.
