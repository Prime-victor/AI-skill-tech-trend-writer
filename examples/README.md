# Examples

One article from each mode, as the skill hands them over.

| File | Mode | What it shows |
| --- | --- | --- |
| [the-new-http-query-method.md](the-new-http-query-method.md) | A: news/trend | A researched article on RFC 10008 with a sources list and frontmatter |
| [what-i-fixed-in-my-article-writing-skill.md](what-i-fixed-in-my-article-writing-skill.md) | B: firsthand | A draft built only from facts the author supplied (here, this skill's changelog), with `[AUTHOR TO FILL: ...]` placeholders where only the author can answer |

The firsthand example is left as a draft on purpose: it shows what you get back before you fill in your own experience. Both pass the bundled checks:

    python scripts/frontmatter_check.py examples/<file>.md
    python scripts/table_check.py examples/<file>.md
    python scripts/word_count.py examples/<file>.md --mode blog
