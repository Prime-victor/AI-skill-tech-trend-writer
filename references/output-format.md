# Output Format

Portfolio posts are plain Markdown files with YAML frontmatter, stored in the portfolio repository and versioned in git. Do not write posts to a database such as Firestore, and do not assume a dashboard editor: the file is the source of truth.

## Where to save

- Default path: `content/posts/<slug>.md`, relative to the portfolio repo root.
- The path is configurable. If the user names a directory, or the repo already keeps posts somewhere else (for example `src/content/blog/` or `_posts/`), use that and follow the repo's existing file naming.
- The file name is the slug plus `.md`. scripts/frontmatter_check.py warns when they differ.
- When no portfolio repo is available in the session, save `<slug>.md` to the working directory and tell the user where it belongs.
- Do not commit or push unless the user asks.

## Frontmatter

Every portfolio post starts with this block, in this order:

    ---
    title: "How I built a Claude skill for writing tech articles"
    slug: how-i-built-a-claude-skill-for-writing-tech-articles
    date: 2026-01-15
    tags: [claude, skills, writing]
    summary: "One or two sentences for the post list and link previews."
    status: draft
    repo_url: "https://github.com/user/project"
    canonical_url: ""
    ---

| Field | Required | Rule |
| --- | --- | --- |
| `title` | yes | Non-empty. Matches the H1. |
| `slug` | yes | Lowercase letters and digits separated by single hyphens: `my-post-title`. |
| `date` | yes | `YYYY-MM-DD`. The publish date, or today's date for a draft. |
| `tags` | yes | A list with at least one tag: `[a, b]` or one `- item` per line. |
| `summary` | yes | Non-empty. One or two sentences, no hype. |
| `status` | yes | `draft` or `published`. |
| `repo_url` | yes | The key must be present. An `http(s)` URL, or empty when the post has no repo (most news posts). |
| `canonical_url` | no | An `http(s)` URL. Set it only when the post was first published elsewhere. |
| `image` | no | Cover image, shown on the post card and above the article. Add it after the fields above. Normally `/blog/<slug>.svg`, drawn to references/cover-images.md; otherwise an image the author supplied. |
| `image_alt` | with `image` | One sentence describing what the cover shows. It becomes the image's alt text. |

Rules:

- New posts start as `status: draft`. Only the author moves a post to `published`.
- A post with any `[AUTHOR TO FILL` placeholder cannot be `published`. scripts/frontmatter_check.py exits non-zero in that case.
- Derive the slug from the headline: lowercase, drop punctuation, replace spaces with hyphens, and trim it to a readable length.
- Quote any value that contains a colon.
- Keep to the simple YAML shown here: `key: value` pairs, inline or block lists, no nested maps or multi-line strings. The checker parses only this subset.
- If the portfolio's static-site generator needs extra fields, add them after these; the checker ignores unknown keys.

## When frontmatter does not apply

A Mode A piece written for a newsletter, a LinkedIn post, or any destination other than the portfolio repo does not need frontmatter. Remove the block from the template and save the file wherever the user asks.

## Validation before hand-off

    python scripts/frontmatter_check.py content/posts/<slug>.md
    python scripts/table_check.py content/posts/<slug>.md
    python scripts/word_count.py content/posts/<slug>.md --mode portfolio
    python scripts/link_checker.py content/posts/<slug>.md
