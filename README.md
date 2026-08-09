# Tech Trend Writer

A Claude Skill for producing well-sourced articles about recent technology trends, product launches, AI news, and industry updates.

## What it includes

- A guided research-to-draft workflow in SKILL.md
- House style, fact-checking, and article-structure references
- A reusable Markdown article template and headline formulas
- Standard-library Python utilities for link validation and word counts

## Install

Copy the tech-trend-writer folder into the Claude Skills directory used by your Claude environment, then restart or reload that environment if needed.

## Use

Ask Claude for a current tech article in natural language, for example:

- Write an article about recent AI coding-agent launches.
- Cover the latest in enterprise cybersecurity.
- Create a weekly tech roundup for a startup newsletter.

The skill is designed to trigger for these requests and research the preceding 1–4 weeks unless a different period is specified.

## Utilities

Check all HTTP(S) links in a draft:

    python scripts/link_checker.py path/to/article.md

Also compare article URLs with a saved text or Markdown export of research results:

    python scripts/link_checker.py path/to/article.md --search-results path/to/search-results.md

Check length against a target range:

    python scripts/word_count.py path/to/article.md --target 800-1200

Both utilities use only the Python standard library.
