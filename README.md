# Tech Trend Writer

A Claude Skill for writing developer-blog and portfolio articles. It works in two modes.

| Aspect | Mode A: News/trend | Mode B: Firsthand/evergreen |
| --- | --- | --- |
| Subject | What other people recently shipped or announced | Your own project, data, experience, or opinion; timeless explainers |
| Who supplies the substance | Research (last 1–4 weeks by default) | You: thesis, what you did, real numbers, what went wrong |
| What Claude does | Research, outline, draft, fact-check, link-check | Intake questions, supporting research, structure, fact-check, polish |
| Structures | Breaking-news brief, roundup, deep-dive | Build log, lessons learned, opinion, evergreen explainer, data-driven experiment |

In Mode B, Claude never invents experiences, metrics, quotes, or outcomes. Anything you have not supplied appears in the draft as `[AUTHOR TO FILL: ...]`, and every figure you did supply is listed back to you as "author-supplied, unverified" so you can confirm it before publishing.

If a request does not make the mode obvious, Claude asks one question and proceeds.

## What it includes

- `SKILL.md`: mode selection and both workflows
- `references/`: article structures and length targets, style guide, table guidance, cover image guidance, fact-check checklist, output format
- `assets/`: article templates for each mode, headline formulas, and a worked Mode B outline
- `scripts/`: frontmatter validation, table checking, link checking, and word counts (Python 3 standard library only)
- `tests/`: `unittest` suites for the scripts

## Install

The installed folder name must match the skill name, `tech-trend-writer`. This repository *is* the skill folder, so clone it under that name.

Claude Code, for all your projects:

    git clone https://github.com/Prime-victor/AI-skill-tech-trend-writer.git ~/.claude/skills/tech-trend-writer

Claude Code, for one project (run from that project's root):

    git clone https://github.com/Prime-victor/AI-skill-tech-trend-writer.git .claude/skills/tech-trend-writer

Update later with `git pull` inside that folder.

Claude apps: download this repository as a ZIP, rename the extracted folder to `tech-trend-writer`, zip it again, and upload it as a skill in settings.

Restart or reload Claude afterwards if the skill does not appear. The scripts need Python 3.10 or later and no other packages.

## Use

Ask in natural language. The skill triggers on its own.

### Mode A: news/trend

- Write an article about recent AI coding-agent launches.
- Cover the latest in enterprise cybersecurity.
- Create a weekly tech roundup for a startup newsletter.

Claude researches the preceding 1–4 weeks unless you give a different period, then drafts, fact-checks, and returns a sourced Markdown article.

### Mode B: firsthand/evergreen

- Write up how I built my invoice parser. The repo is at <url> and here are my notes.
- Turn these notes into a "what I learned" post about migrating from REST to gRPC.
- I cut my Claude token usage from 41k to 17k tokens per run. Help me write the post. Here are my before/after logs.
- I think most side projects don't need a database. Help me argue that in a blog post.
- Write an explainer on how prompt caching works, using my chatbot project as the example.

Claude first asks for whatever is missing from: your thesis in one sentence, what you actually did, real numbers, what went wrong or surprised you, and links to the repo or demo. You can answer briefly or say "draft it anyway" and fill the placeholders afterwards.

## Output

Portfolio posts are Markdown files with YAML frontmatter, saved in your portfolio repo and versioned in git. There is no database and no dashboard editor.

- Default path: `content/posts/<slug>.md`. Tell Claude if your site keeps posts elsewhere.
- Frontmatter: `title, slug, date, tags, summary, status, repo_url`, and optionally `canonical_url`.
- New posts are saved as `status: draft`. You change it to `published`.

Field rules are in `references/output-format.md`.

## Scripts

Run these from the skill folder (the repository root). Each exits non-zero when it finds a problem, so they can be used in a pre-commit hook or CI.

Validate frontmatter and find leftover placeholders:

    python scripts/frontmatter_check.py content/posts/my-post.md

It checks required fields, slug format (lowercase with hyphens), date format (`YYYY-MM-DD`), and status (`draft` or `published`). Leftover `[AUTHOR TO FILL` placeholders are a warning in a draft and an error in a published post.

Check that tables are well formed and fully populated:

    python scripts/table_check.py content/posts/my-post.md
    python scripts/table_check.py content/posts/my-post.md --require-table

It fails on empty cells, filler such as `-`, `N/A`, or `TBD`, rows whose cell count differs from the header, and a header with no separator row. It warns about one-row tables, tables wider than six columns, a missing blank line before a table, and cells that still hold an `[AUTHOR TO FILL` placeholder. `--require-table` also fails a post that has no table at all.

Check every HTTP(S) link in a post:

    python scripts/link_checker.py content/posts/my-post.md
    python scripts/link_checker.py content/posts/my-post.md --timeout 20

It tries `HEAD`, falls back to `GET`, follows redirects and reports the final URL and number of hops, and reports 4xx, 5xx, timeouts, and connection errors separately. This is the only script that uses the network.

Also fail any URL that does not appear in a saved export of research results:

    python scripts/link_checker.py path/to/article.md --search-results path/to/search-results.md

Check length against the default range for a mode or structure:

    python scripts/word_count.py content/posts/my-post.md --mode portfolio

Frontmatter and fenced code blocks are not counted. Modes: `news` 800–1200, `brief` 300–600, `roundup` 800–1200, `deep-dive` 1500–2500, `firsthand` 1000–1800, `build-log` 1000–1800, `lessons-learned` 900–1500, `opinion` 700–1200, `explainer` 1200–2000, `experiment` 1000–1800.

Use your own range instead (this overrides `--mode`):

    python scripts/word_count.py content/posts/my-post.md --target 800-1200

## Tests

    python -m unittest discover -s tests -v

The link-checker tests start a temporary server on localhost and do not reach the internet.

## Try asking

- Write a deep-dive on what this month's model releases mean for small dev teams.
- Compare this month's three big model releases in a table, then tell me what changed.
- Give me a 400-word brief on yesterday's framework release.
- Help me write a build log for my portfolio about this repo.
- Here are my token counts before and after I restructured my prompts. Write the experiment post.
- I have three lessons from shipping my first Chrome extension. Turn them into a post.
- Outline a post called "How I built a Claude skill for writing tech articles" and mark what I need to fill in.
