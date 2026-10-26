---
name: tech-writer-lite
description: >-
  Write rigorously sourced articles, newsletter pieces, LinkedIn posts, and roundups about
  recent technology trends, product launches, AI news, and industry updates. Researches the
  last few weeks from primary sources, drafts, fact-checks, and cites every claim. Use this
  skill for any request that resembles "write an article about...", "cover the latest in...",
  "trend piece on...", "tech roundup", or "what's new in [tech topic]", even when the user
  never mentions a skill.
compatibility: >-
  Requires web search. The optional word-count script needs Python 3.10 or later (standard
  library only).
---

# Tech Writer Lite

## Workflow

1. Confirm the topic, angle, target length, tone, and publishing format (blog post, newsletter, LinkedIn post, or similar) when missing. Do not stall: if the request is clear, make a sensible assumption and state it briefly.
2. Research developments from the last 1–4 weeks unless the user specifies another window. Run several focused web searches. Prefer primary sources (company newsrooms, release notes, filings, standards bodies, and official documentation), then corroborate with reputable technology reporting rather than aggregators.
3. Before drafting, open references/article-structures.md to choose a structure suited to the request, then open assets/article-template.md and build a concise outline from it.
4. Draft from that outline. Follow references/style-guide.md while writing. Use assets/headline-formulas.md when proposing or choosing a headline.
5. Open references/fact-check-checklist.md and run every applicable check against the finished draft; revise before presenting it.
6. Optionally run `python scripts/word_count.py <article.md> --mode <structure>` (or `--target MIN-MAX`) when a length range needs checking.
7. Save the final article as a Markdown file, include a Sources list, and present the article or its saved path to the user.

## Sourcing and citations

- Never invent statistics, quotes, dates, URLs, product details, or sources. If a fact cannot be verified, leave it out or say it is unconfirmed.
- Attribute factual and analytical claims close to the claim; use direct links in the Sources list.
- Keep quotations short. Prefer accurate paraphrase and preserve the source's meaning, especially for copyrighted reporting.
- Prefer sources published within the relevant recency window; label older context as background when it is needed.
- Distinguish a verified fact from analysis, forecast, or opinion. Resolve material disagreements with the newest authoritative source or disclose the uncertainty.

## Resource pointers

- Open references/article-structures.md before outlining.
- Open references/style-guide.md before drafting or revising.
- Open references/fact-check-checklist.md immediately before finalizing.
- Use assets/article-template.md as the working outline and final-article scaffold.
- Use assets/headline-formulas.md only when generating or refining headlines.
