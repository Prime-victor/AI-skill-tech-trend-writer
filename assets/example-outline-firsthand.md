# Worked example: outline for a build log

This is an outline, not a draft. It shows what a Mode B outline looks like after intake when the author has shared the repo but not yet their story or numbers. Facts taken from the repo are written out. Everything only the author can know is a placeholder.

Structure: Build log / project write-up (references/article-structures.md).

---

**Working headline:** How I built a Claude skill for writing tech articles

**Summary:** [AUTHOR TO FILL: one or two sentences: what the skill does and the one result worth knowing]

**Thesis:** [AUTHOR TO FILL: the argument in one sentence, e.g. what you now believe about getting an LLM to write sourced articles]

## 1. Problem

- [AUTHOR TO FILL: what you were trying to write, and how often]
- [AUTHOR TO FILL: what went wrong when you asked Claude for an article without a skill: a specific bad output, such as a dead link or an unsourced statistic]
- [AUTHOR TO FILL: why existing tools or prompts were not enough]

## 2. Constraints

- Python 3 standard library only, no API keys, Markdown output. (From the repo.)
- [AUTHOR TO FILL: why you chose no third-party dependencies]
- [AUTHOR TO FILL: time budget and what you left out on purpose]

## 3. Approach: the workflow

- What a Claude skill is: a folder with a SKILL.md plus reference files, assets, and scripts that Claude loads when a request matches. Cite the official skills documentation for background.
- The workflow as SKILL.md defines it: confirm the brief, research, choose a structure, outline from the template, draft to the style guide, fact-check, check links, save Markdown.
- Why detail lives in references/ and assets/ instead of SKILL.md: [AUTHOR TO FILL: your reasoning, and what happened when SKILL.md was longer, if you tried that]
- [AUTHOR TO FILL: how many iterations the workflow went through and what changed between them]

## 4. The fact-check step

- What it is: a checklist run against the finished draft before it is shown: every statistic sourced, product names and versions current, quotes attributed, no claim contradicted by a newer source, facts separated from analysis. (From references/fact-check-checklist.md.)
- Why it is a separate step after drafting rather than an instruction during drafting: [AUTHOR TO FILL: what you observed]
- [AUTHOR TO FILL: a real example of an error the checklist caught: the claim, what was wrong, how it was fixed]
- [AUTHOR TO FILL: an error it missed, if any]

## 5. Why the link checker exists

- What it does: extracts every URL from the Markdown file, requests each one, reports which are broken, and exits non-zero if any are. With `--search-results` it also fails any URL that does not appear in the saved research results. (From scripts/link_checker.py.)
- The reason for `--search-results`: a URL can look plausible and still never have come from research. [AUTHOR TO FILL: the incident that made you add this: what the invented or dead link was and how you found it]
- Why a script instead of asking the model to check its own links: [AUTHOR TO FILL: your reasoning]
- [AUTHOR TO FILL: how many links a typical article has, and how often the checker finds a problem]

## 6. Results

| Metric | Before | After | Change |
| --- | --- | --- | --- |
| [AUTHOR TO FILL: e.g. time from topic to publishable draft] | [AUTHOR TO FILL] | [AUTHOR TO FILL] | [AUTHOR TO FILL] |
| [AUTHOR TO FILL: e.g. broken or unsourced links per article] | [AUTHOR TO FILL] | [AUTHOR TO FILL] | [AUTHOR TO FILL] |
| [AUTHOR TO FILL: e.g. tokens or cost per article] | [AUTHOR TO FILL] | [AUTHOR TO FILL] | [AUTHOR TO FILL] |

- [AUTHOR TO FILL: how you measured each number and over how many articles]

## 7. What went wrong

- [AUTHOR TO FILL: the first thing that did not work, and how you noticed]
- [AUTHOR TO FILL: something that surprised you about how Claude used the skill]
- [AUTHOR TO FILL: a limitation that is still there]

## 8. Takeaways

- [AUTHOR TO FILL: the lesson for someone building their own skill]
- [AUTHOR TO FILL: what you would do differently]
- [AUTHOR TO FILL: what you plan to add next]

## 9. Links

- Repo: [AUTHOR TO FILL: repo URL]
- Official documentation for Claude skills (to be linked after research)
- [AUTHOR TO FILL: an article written with the skill, if published]

---

## Hand-off checklist for this outline

Author-supplied, unverified:

- None yet. No figures have been supplied.

Still to fill:

- Every `[AUTHOR TO FILL: ...]` item above. The most important are the thesis, the fact-check example in section 4, the link-checker incident in section 5, and the results table.
