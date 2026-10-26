---
title: "What I fixed in my article-writing skill after using it on my own blog"
slug: what-i-fixed-in-my-article-writing-skill
date: 2026-10-26
tags: [ai-agents, skills, writing]
summary: "Six releases in a month, each one fixing something the drafts got wrong, and the rule that made the rest possible: never invent the author's experience."
status: draft
repo_url: "https://github.com/Prime-victor/AI-skill-tech-trend-writer"
---

# What I fixed in my article-writing skill after using it on my own blog

[AUTHOR TO FILL: the moment you decided the first version was not enough, for example the first firsthand post you asked it for and what came back]

The first version of tech-trend-writer did one thing: research recent tech news, draft an article, fact-check it, and cite sources. It worked for news. It had nothing to say about the posts I wanted most on my own blog, the ones about what I built.

## The rule everything else depends on

Version 2.0 added a second mode for firsthand posts: build logs, lessons learned, experiments, opinion. The hard part was not structure. It was stopping the model from filling gaps with a plausible story.

So the skill has one rule it never bends: it does not invent experiences, metrics, quotes, or outcomes. When I have not given it a number, the draft says so:

```text
[AUTHOR TO FILL: tokens per run before the change]
```

A checker script refuses to pass a post marked `published` while any of those placeholders remain. [AUTHOR TO FILL: your stance on this rule in one sentence, for example why a visible gap beats a plausible number]

## Every release fixed something I saw in a draft

From 2.2 on, each release names the problem it fixed: something wrong in a real draft.

Table: What each release fixed

| Version | What was wrong | What changed |
| --- | --- | --- |
| 2.0 | Only news articles | A firsthand mode with intake questions and placeholders |
| 2.1 | Comparisons buried in paragraphs | Table rules and a script that fails on empty or filler cells |
| 2.2 | Posts came out as 6–8 minute reads | A 3–5 minute cap and guidance on what to cut |
| 2.3 | Every post card showed the same gradient | A drawn SVG cover for each post |
| 2.4 | The covers all looked like one template | Rules for distinct, article-specific covers |
| 2.5 | Accurate posts with no person in them | A voice guide: real openings, stances, one real artifact |

Source: the skill's CHANGELOG.

The 2.5 problem was the hardest to see. The posts were correct and well structured, and they read like documentation. [AUTHOR TO FILL: one line on how you noticed, for example a reader comment or rereading a post a week later]

## Making it sound like me without lying for me

The voice guide pushed in one direction: open with a real moment, take a stance, show something real. The very next round of drafts went too far the other way. They implied experiences I never had.

Version 2.5.1 added the section the rest of the voice guide depends on: say only what the author lived through. First-person moments only for problems I confirm. An honest status next to any code: shipped, prototyped, or design only. Examples from other people are framed as something I came across, not something I did.

## The scripts check what instructions cannot

A model can skim past an instruction; a script exits non-zero whatever the model thinks. The skill ships four, all Python standard library, with 92 tests between them:

- `frontmatter_check.py` catches missing fields and leftover placeholders.
- `table_check.py` fails on blank cells and filler such as `TBD`.
- `link_checker.py` reports broken links and can flag any URL that did not come from the research.
- `word_count.py` checks length against the post's target.

[AUTHOR TO FILL: one thing a script caught that you would have published otherwise]

## What I would do differently

[AUTHOR TO FILL: the one thing you would change if you started the skill again]

If you build a writing skill of your own, start with the rule about invented facts and a script that enforces it. Style can be fixed in later releases; a published fake number cannot be taken back.
