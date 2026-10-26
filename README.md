# Tech Writer Lite

A free agent skill that turns recent tech news into a sourced, fact-checked article. It researches the last 1–4 weeks from primary sources, picks a structure, drafts, runs a fact-check pass, and cites every claim.

See [`examples/`](examples/) for a finished article.

## Install

The installed folder name must match the skill name, `tech-writer-lite`. This repository is the skill folder, so clone it under that name.

Claude Code, for all your projects:

    git clone https://github.com/Prime-victor/AI-skill-tech-trend-writer.git ~/.claude/skills/tech-writer-lite

Claude Code, for one project (run from that project's root):

    git clone https://github.com/Prime-victor/AI-skill-tech-trend-writer.git .claude/skills/tech-writer-lite

Update later with `git pull` inside that folder.

Claude apps: download this repository as a ZIP, rename the extracted folder to `tech-writer-lite`, zip it again, and upload it as a skill in settings.

Other agents that support SKILL.md skills: copy the folder into that agent's skills directory as `tech-writer-lite`.

The skill needs an agent with web search.

## Use

Ask in natural language. The skill triggers on its own.

- Write an article about recent AI coding-agent launches.
- Cover the latest in enterprise cybersecurity.
- Give me a 400-word brief on yesterday's framework release.
- Create a weekly tech roundup for a startup newsletter.

## What's inside

- `SKILL.md`: the workflow and sourcing rules
- `references/`: article structures and length targets, style guide, fact-check checklist
- `assets/`: article template and headline formulas
- `scripts/word_count.py`: checks length against each structure's range (Python 3.10+, no packages)
- `tests/`: `unittest` suite for the script

Check an article's length:

    python scripts/word_count.py article.md --mode news
    python scripts/word_count.py article.md --target 800-1200

Run the tests:

    python -m unittest discover -s tests -v

## Want more?

**Tech Writer Pro** adds:

- **A firsthand mode** for build logs, lessons learned and portfolio posts written from your own work. It never invents a fact or an experience, and leaves visible `[AUTHOR TO FILL]` gaps for you instead.
- **A voice guide** so first-person posts sound like you, not like documentation.
- **Site settings** for your blog's folder, frontmatter, length and cover images.
- **Validation scripts** for frontmatter, tables and links, including a check that flags made-up URLs.

Find it on Agensi: [Tech Writer Pro](https://www.agensi.io/creators/victor-kiptum).

## License

MIT. See [LICENSE](LICENSE).
