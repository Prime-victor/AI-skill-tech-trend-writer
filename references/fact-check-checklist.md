# Fact and Citation Checklist

Before finalizing, verify each applicable item:

- [ ] Every statistic, percentage, financial figure, benchmark, and user count has a source.
- [ ] Every named product, model, feature, and version is current as of the research date.
- [ ] Every quote is short, accurately attributed, and paraphrased rather than copied unless a brief direct quote is essential.
- [ ] No claim contradicts a more recent or more authoritative source found during research.
- [ ] Publish dates and discovery or announcement dates are stated when readers could confuse them.
- [ ] Links lead to the cited source, and claims do not overstate what that source says.
- [ ] The article clearly separates confirmed facts from analysis, projections, and opinion.
- [ ] The Sources list includes the most material primary and corroborating sources.
- [ ] Every table cell holds a specific value that traces to a source (or, in Mode B, to the author). No cell is blank, filler, or filled by analogy with another row.
- [ ] Units and precision are consistent down each table column, and computed cells (change, percentage, total) are arithmetically correct.
- [ ] Figures in a table match the same figures in the prose.
- [ ] Each table has a `Table:` title directly above it. Where it cites sources or needs a caveat, a `Sources:` or `Note:` caption sits directly below it, and the takeaway is a separate sentence after that.
- [ ] The cover exists at `public/blog/<slug>.svg`, `image` points to it and `image_alt` describes it. Every label on it appears in the article, its background differs from the other posts' covers, and it reads at card size (references/cover-images.md).

## Firsthand posts (Mode B)

Apply the checks above to every external claim, then verify each applicable item below.

Author-supplied figures:

- [ ] Every figure in the post about the author's own work came from the author. None was estimated, rounded, or inferred by Claude.
- [ ] Each author-supplied figure is listed under "Author-supplied, unverified" in the hand-off checklist, with what it measures.
- [ ] Each figure has a unit, a baseline, and a time period or sample size, or a placeholder asking for it.
- [ ] Percentages and multiples are arithmetically consistent with the raw before/after values shown.
- [ ] The same figure does not appear with different values in different places.

Reproducibility:

- [ ] The post states how each result was measured: tool, command, or data source.
- [ ] Versions of the models, libraries, and tools that affect the result are named.
- [ ] The repo or demo link is present, and the linked code matches what the post describes.
- [ ] Code and command excerpts are taken from the author's material, not reconstructed from memory.

No overclaiming:

- [ ] Results are stated as what happened in the author's setup, not as general truths.
- [ ] Causal claims ("X reduced Y") are supported by a controlled comparison, or reworded as observation.
- [ ] Limitations, untested cases, and a small sample size are disclosed near the result they qualify.
- [ ] Quotes and anecdotes involving other people came from the author; none were invented or embellished.

Placeholders:

- [ ] Every gap is marked `[AUTHOR TO FILL: ...]` and listed in the hand-off checklist.
- [ ] No placeholder remains when `status` is `published` (scripts/frontmatter_check.py enforces this).

Hand-off checklist format, placed at the end of the reply and not in the post:

    Author-supplied, unverified:
    - [ ] <figure> — <what it measures> — <where it appears>

    Still to fill:
    - [ ] <placeholder text> — <section>
