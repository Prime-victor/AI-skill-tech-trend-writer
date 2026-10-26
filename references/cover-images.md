# Cover images

Covers are optional. Draw one when the author asks for it or the site's existing posts already have covers (see Site settings in SKILL.md). A cover is one original SVG that communicates that post's subject, usually shown on the post card and above the article. Across a site, the covers should read as an art-directed set, not as one template with the shapes swapped.

The sizes and paths below are defaults from a typical blog layout. When the author's site uses a different cover path, aspect ratio or card size, follow the site.

Never use stock photos, generated photos, simulated hand-drawn art, or made-up screenshots. A real screenshot is only used when the author supplies it.

## Concept

Base the cover on what the article actually says. Every label, stage, number and name on a cover must appear in the article. Pick one of two forms:

- A diagram that carries meaning: a workflow, a schedule, an architecture comparison. Spacing and emphasis should say something (what comes first, what is costly, what was dropped).
- A typographic cover: one word or short phrase from the article, set large, with one deliberate mark.

Example covers:

| Post | Form | Background | Cover |
|---|---|---|---|
| The AI race at work is no longer about tokenmaxxing | Typographic | Paper off-white | "tokenmaxxing" in large serif, struck through in terracotta, above "cost per useful result" |
| How grill, spec, review, retro works | Diagram | Slate blue | A line of work crossing four labelled gates, a file under each, the spec file linked to build and to review |
| How time-boxing worker agents works | Diagram | Terracotta | A 0–60 minute axis with three worker lanes: commit, killed at 30, report in the last quarter |
| When to use a monolith instead of microservices | Diagram | Forest green | Orders, payments and shipping as one unit with one database, and as three services joined by network calls |

## Variety across the set

- Give each cover its own background colour. Any two posts can end up next to each other in the grid, so check the neighbours before choosing.
- Palette to draw from: paper off-white, muted blue and slate, forest green and olive, terracotta and ochre, charcoal. Teal only where the concept needs it.
- At most about one cover in three has a dark background, counted across all posts.
- Do not repeat a composition. Avoid glows, gradients, floating shapes, decorative networks, rounded cards inside the artwork, and symmetry for its own sake.

## File and canvas

- File: `public/blog/<slug>.svg` by default (or the site's cover path), hand-written, no embedded bitmaps, no external references, under 100 KB.
- Frontmatter: `image: /blog/<slug>.svg` and `image_alt: "..."`, a one-sentence description of what the cover shows. Set `image` only once the file exists.
- Root element: `viewBox="0 0 1600 960" width="1600" height="960"`, with `role="img"`, an `aria-label` and a `<title>` that match `image_alt`.
- Many sites fit an SVG cover whole rather than cropping it. On a card that is wider than 5:3 (for example 208px tall and up to about 720px wide) that leaves empty space left and right of the viewBox. Fill it: make the background rect much larger than the viewBox (`x="-3000" y="-1000" width="7600" height="2960"`) and let rules and axis lines run past the edges too.
- Keep everything that matters inside the viewBox.

## Text

- Use system font stacks, because an SVG loaded as an image cannot use the site's web fonts. Serif: `Georgia, 'Times New Roman', Times, serif`. Monospace: `ui-monospace, 'Cascadia Mono', Consolas, 'SF Mono', Menlo, 'Liberation Mono', monospace`.
- On a typical card the cover is drawn at about 0.2 scale. Labels that must be read there are at least 56 units tall and few in number.
- Smaller annotations go in a `.fine` group that is hidden on cards and shown on the article page:

```css
.fine { display: none; }
@media (min-height: 300px) { .fine { display: inline; } }
```

- Set `textLength` on a large display word so its width is the same on every operating system.

## Check before hand-off

If you can run the site, look at the blog index at desktop, tablet and phone widths (for example 1440px, 767px and 390px), and at the article page. If you cannot, say so in the hand-off. Labels must be readable at each size, nothing may be cut off, and no two neighbouring cards may share a background colour.
