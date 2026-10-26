# Changelog

## 2.6.0 — 2026-10-26

The skill was tuned to one author's blog: a fixed posts path, a cover on every post, and a 3–5 minute cap. Those are now defaults the user can change, so it fits any Markdown site.

### Added

- "Site settings" in SKILL.md: settings come from the conversation, then project instructions, then the repo's existing posts, then the defaults. The skill asks once when the posts directory is still unclear.
- `blog` mode in scripts/word_count.py (550–900 words), with a test. `portfolio` still works as an alias.
- LICENSE (MIT).
- examples/: a news/trend article and a firsthand draft with placeholders.
- README: install notes for other agents, a site-settings table, and a License section.

### Changed

- Cover images are optional: drawn only when the author asks or the site's posts already have covers. Cover sizes and paths in references/cover-images.md are defaults, not rules.
- Frontmatter follows the site's existing posts when there are any; references/output-format.md is the default schema.
- "Portfolio repo" wording is now "blog repo" throughout.
- The description leads with what the skill does and its no-invention rule.
- The README installs the skill by cloning this repository straight into the skills folder.

### Fixed

- .gitignore contained a literal `echo` command instead of ignore patterns.

## 2.5.2 — 2026-10-23

### Changed

- references/voice.md: "I'd" is kept for the two or three strongest stances, the rest is plain second-person advice; artifacts that name the author in the third person get a one-line note on who wrote them; posts end on a short recap and the one thing the author would do differently, supplied by the author.

## 2.5.1 — 2026-10-23

A second revision round showed the voice rules let a draft imply experience the author never had, and still allowed templated cadence.

### Changed

- references/voice.md: a new "Say only what the author lived through" section. First-person moments only for problems the author confirms, an honest one-line status next to code and designs (shipped, prototyped, or design only), and outside examples framed as "I came across" plus what the author took from them.
- references/voice.md: ask in one round of multiple-choice questions when an author-only fact decides the text, never fill a request's own brackets, and never mine employer or client repositories for publishable details.
- references/voice.md: more stock phrases to cut ("X are no different", "put it plainly"), no paired clipped declaratives, and no runs of parallel bold labels. Revisions leave "don't touch" sections alone and count length without placeholders.

## 2.5.0 — 2026-10-23

Firsthand posts were accurate and well structured but read like documentation with no person in them: a stock opening, no stances, a generic template where the author's own example belonged, and every section the same shape.

### Added

- references/voice.md: open with a real moment; take two or three first-person stances where the reader wants a recommendation, grounded in what the author said or already recommends; show one real artifact in the post's main section; vary section length and shape; a read-aloud pass with contractions and a list of stock phrases to cut; rules for revising an existing post (claims, quotes and code unchanged, length within 10%, a hand-off listing placeholders, sources used and least-sure changes).
- Before writing a placeholder, look for the author's real material in the conversation, their files, their git history and their earlier posts, and check ownership with git so a cloned project is never presented as their work.

### Changed

- SKILL.md: Mode B drafting step and resource pointers send first-person drafts and "make it sound like me" revisions to references/voice.md.
- references/style-guide.md: the firsthand section points to references/voice.md, and a "Takeaways" heading is now optional.

## 2.4.0 — 2026-10-09

The 2.3.0 covers all shared one dark background, one teal accent and a centred diagram, and read as a template. The cover rules are rewritten around distinct, article-specific covers.

### Changed

- references/cover-images.md: each cover is a meaningful diagram or a typographic cover with its own background colour; at most about one in three is dark; labels are allowed and must come from the article; the canvas is 1600×960 and is fitted whole, with the background bleeding past the viewBox to fill wide cards; system font stacks, a 56-unit minimum for card-size labels, and a `.fine` group for annotations shown only on the article page.
- The cover rule in references/style-guide.md and the cover item in references/fact-check-checklist.md follow the new rules. "No text in the image" is removed.

### Added

- `image_alt` frontmatter field in references/output-format.md: the cover's alt text.

## 2.3.0 — 2026-10-09

Portfolio posts had no cover, so every card on the blog showed the same gradient. Each post now gets a concept illustration.

### Added

- references/cover-images.md: what to draw, the 1600×900 canvas and safe area, the palette, the no-text rule, where the file goes (`public/blog/<slug>.svg`), and the four existing covers as examples.

### Changed

- The `image` field in references/output-format.md, the cover rule in references/style-guide.md and the output rules in SKILL.md now call for a drawn SVG cover by default. An author-supplied image still takes its place when there is one.

## 2.2.0 — 2026-10-09

Posts for the portfolio blog were coming out as 6–8 minute reads because each structure's default range was written for long-form pieces. They are now capped at 3–5 minutes.

### Added

- `portfolio` mode in scripts/word_count.py (550–900 prose words), with tests. It is the length check for every post saved to the portfolio repo, whatever its structure.
- "Portfolio posts are capped at a 3–5 minute read" in references/article-structures.md, including what to cut to fit a structure into the cap.
- "Reading experience (portfolio posts)" in references/style-guide.md: hook, subtitle, heading frequency, paragraph length, one scannable element per screen, one pull quote, and how to end.
- Optional `image` frontmatter field for a cover image in references/output-format.md. Only author-supplied images are allowed.

- Table titles in references/tables.md: a paragraph starting `Table:` directly above the table, which the portfolio blog renders as the table's title bar.
- Both article templates, the fact-check checklist and the style guide use the `Table:` title and the `Sources:` or `Note:` caption.
- Table captions in references/tables.md: sources go in a paragraph starting `Sources:` directly under the table, which the portfolio blog renders as a caption; the takeaway is a separate sentence after it.

### Changed

- Both workflows in SKILL.md run `word_count.py --mode portfolio` for portfolio posts. The per-structure ranges remain for newsletters, other destinations, and long reads the author asks for.
- The validation commands in references/output-format.md and README.md use `--mode portfolio` and include table_check.py.

## 2.1.0 — 2026-10-09

### Added

- references/tables.md: when a post needs a table, how to plan it before drafting, and rules for filling every cell with a specific, sourced or author-supplied value.
- scripts/table_check.py with tests: fails on empty or filler cells, rows that do not match the header, and missing separator rows; `--require-table` fails a post with no table.
- Table steps in both workflows in SKILL.md, table items in the fact-check checklist, and an optional comparison table in assets/article-template.md.

## 2.0.0 — 2026-10-09

The skill now serves a developer portfolio blog: it keeps the news workflow and adds a mode for firsthand and evergreen posts.

### Added

- Mode B (firsthand/evergreen) workflow in SKILL.md: intake questions, supporting-only research, first-person voice, and an "author-supplied, unverified" hand-off checklist.
- Hard rule against inventing experiences, metrics, quotes, or outcomes; gaps become `[AUTHOR TO FILL: ...]` placeholders.
- Mode selection rules at the top of SKILL.md, with one clarifying question when the mode is unclear.
- Five structures in references/article-structures.md: build log, lessons learned, opinion, evergreen explainer, and data-driven personal experiment, plus a table of default length targets.
- assets/article-template-firsthand.md, assets/example-outline-firsthand.md, firsthand headline formulas, and a firsthand section in the fact-check checklist and style guide.
- references/output-format.md: posts are Markdown files with standard frontmatter (`title, slug, date, tags, summary, status, repo_url`, optional `canonical_url`), saved by default to `content/posts/<slug>.md`.
- scripts/frontmatter_check.py and `unittest` suites in tests/.

### Changed

- The skill folder is now `tech-trend-writer`, matching the skill name.
- The frontmatter description triggers for project write-ups, build logs, and other firsthand posts as well as trend articles.
- scripts/link_checker.py reports redirect chains and the final URL, separates 4xx, 5xx, timeouts, and connection errors, and falls back to GET whenever HEAD does not return 200.
- scripts/word_count.py has a `--mode` flag with default ranges and no longer counts frontmatter, fenced code blocks, or HTML comments. Counts for existing drafts that contain these will be lower than before.
- assets/article-template.md starts with the standard frontmatter block.

### Removed

- The "do not use for opinion pieces or evergreen explainers" restriction.

### Fixed

- .gitignore contained a literal `echo` command instead of ignore patterns.
