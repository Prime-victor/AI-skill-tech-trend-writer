---
name: tech-trend-writer
description: >-
  Write rigorously sourced tech articles, blog posts, newsletter pieces, LinkedIn posts,
  and roundups about current or recent technology trends, product launches, AI news, and
  industry updates. Use this skill eagerly for any request that resembles "write an
  article about...", "cover the latest in...", "trend piece on...", "tech roundup",
  or "what's new in [tech topic]", even when the user never mentions a skill.
compatibility: Requires web search access to research and verify recent developments effectively.
---

# Tech Trend Writer

## Workflow

1. Confirm the topic, angle, target length, tone, and publishing format (blog post, newsletter, LinkedIn post, or similar) when missing. Do not stall: if the request is clear, make a sensible assumption and state it briefly.
2. Research developments from the last 1–4 weeks unless the user specifies another window. Run several focused web searches. Prefer primary sources—company newsrooms, release notes, filings, and official documentation—then corroborate with reputable technology reporting rather than aggregators.
3. Before drafting, open references/article-structures.md to select a shape suited to the request, then open assets/article-template.md and build a concise outline from it.
4. Draft from that outline. Open and follow references/style-guide.md while writing. Use assets/headline-formulas.md when proposing or selecting a headline.
5. Open references/fact-check-checklist.md and run every applicable check against the finished draft; revise before presenting it.
6. Optionally run scripts/link_checker.py on the Markdown file to detect broken cited links. Pass --search-results with a saved search-results export to also verify that cited URLs came from research rather than being fabricated. Use scripts/word_count.py when a requested or assumed length range needs verification.
7. Save the final article as a Markdown file, include a source list, and present the finished article or its saved path to the user.

## Sourcing and citations

- Never invent statistics, quotes, dates, URLs, product details, or sources.
- Attribute factual and analytical claims close to the claim; use direct links in the Sources list.
- Keep quotations short. Prefer accurate paraphrase and preserve the source's meaning, especially for copyrighted reporting.
- Prefer sources published within the relevant recency window; label older context as background when it is needed.
- Distinguish a verified fact from analysis, forecast, or opinion. Resolve material disagreements with the newest authoritative source or disclose the uncertainty.

## When not to use this skill

Do not use this workflow for a purely personal opinion piece without factual or trend claims, or for an evergreen explainer where no recent development needs research. Use a general writing workflow instead.

## Resource pointers

- Open references/article-structures.md before outlining to choose breaking-news brief, roundup, or deep-dive structure.
- Open references/style-guide.md before drafting or revising for voice and formatting rules.
- Open references/fact-check-checklist.md immediately before finalizing to audit facts, dates, quotes, and citations.
- Use assets/article-template.md as the working outline and final-article scaffold.
- Use assets/headline-formulas.md only when generating or refining headlines.
