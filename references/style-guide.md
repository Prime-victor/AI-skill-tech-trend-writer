# House Style Guide

## Voice

Write with a confident, calm, plain-English voice. Explain what changed, why it matters, and what remains uncertain. Sound informed, not breathless. Avoid hype-speak, clickbait, and vague claims of disruption.

## Sentences and paragraphs

- Favor sentences of roughly 12–25 words; vary rhythm when clarity benefits.
- Keep paragraphs to 2–4 sentences and give each one a single job.
- Lead with the concrete development before interpretation or background.

## Jargon

Define specialist terms on first use in everyday language. Keep accepted terms such as API when the intended audience expects them; otherwise expand the abbreviation once. Do not use jargon merely to signal expertise.

## Formatting

- Use one clear H1 headline, then descriptive H2 sections. Use H3 only for genuine subsections.
- Use bullets for scannable lists, comparisons, or steps—not as a substitute for narrative.
- Use a table when readers compare items across attributes or read before/after numbers. Plan it while outlining and fill every cell with a specific value; follow references/tables.md. Give it a `Table:` title above and a `Sources:` or `Note:` caption below, never a "The table shows..." sentence.
- Bold only a few terms or takeaways when scanning would materially improve; never bold full sentences or every section lead.
- Link sources naturally in prose where useful and include a compact Sources list at the end.

## Firsthand posts (Mode B)

- Follow references/voice.md for the opening moment, stances, the real artifact, uneven section lengths and the read-aloud pass.

- Write in the first person singular. "I" did the work; avoid "we" unless the author names a team.
- Prefer the specific over the general: the actual command, file, error message, model, version, and number. "Latency dropped from 2.1 s to 0.8 s" beats "it got much faster".
- Give every number its unit, its baseline, and how it was measured. A percentage without the two values behind it is not enough.
- Keep the author's own claims in their voice and at their strength. Do not upgrade "this worked for my project" into "this is the best approach".
- Include what failed. A post with no dead ends reads like marketing.
- Say what was not tested or measured rather than leaving the reader to assume it was.
- Leave `[AUTHOR TO FILL: ...]` placeholders visible and specific about what is needed, for example `[AUTHOR TO FILL: tokens per run before the change]`. Never smooth over a gap with an invented detail.
- Credit tools, libraries, and people by name, and link to them.

## Reading experience (blog posts)

A blog post is read on a phone, in one sitting, by someone deciding whether the author can think. Write it to the standard of a well-edited Medium article.

- Length: a 3–5 minute read. Check with `scripts/word_count.py --mode blog`.
- Hook: the first two sentences state a concrete situation, fact, or question. No scene-setting about how fast the industry moves.
- Subtitle: the `summary` field is shown under the headline. Make it one sentence that says what the reader gets.
- Section headings: one every 120–200 words, each a plain statement of what the section covers. A reader who only reads the headings should still follow the argument.
- Paragraphs: two to four sentences. A paragraph that runs past five lines on a phone gets split.
- One scannable element per screen or two: a table, a short list, a code block, or a pull quote. Do not stack two tables without prose between them.
- Pull quote: at most one blockquote, used for the line the reader should remember.
- Cover image (optional, see Site settings in SKILL.md): when the post gets a cover, make one original SVG that fits its subject, saved to the site's cover path (default `public/blog/<slug>.svg`, `image: /blog/<slug>.svg`) with an `image_alt` description; follow references/cover-images.md for concept, palette, canvas and text rules. Use an author-supplied image instead when there is one. Never invent an image URL, a screenshot, or a detail the article does not contain; if no cover was made, leave the fields out and say so in the hand-off.
- Ending: close on two or three things the reader can act on. A "Takeaways" heading is optional; drop it when the last section can end on them in the author's own words. Do not close with a summary of the post.

## Do not do this

- Do not manufacture urgency with words such as “just,” “breaking,” or “must-know” unless the timing supports them.
- Do not call something “revolutionary,” “game-changing,” “unprecedented,” or “the best” without specific, verified evidence.
- Do not imply causation when the sources establish only correlation.
- Do not bury caveats that would change a reader’s interpretation.
