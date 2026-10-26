# Voice: write it the way the author would say it

Every portfolio post should read like an engineer telling a colleague what they found, not like product documentation. Accurate and well structured is the floor. A person has to be in it.

Apply this file to every Mode B draft, to the firsthand parts of a Mode A piece, and to any request to revise a post so it "sounds like me", "sounds less like AI", or "reads less like docs".

## Find the author's real material first

The hard rule from SKILL.md still holds: never invent an experience, a result, a number, or an opinion. Being creative means looking harder for real material, not making it up.

Before writing a placeholder, look for what the author already has:

1. **The conversation.** Corrections they made, things they pushed back on, the reason they asked for the post. "Make it about models, not only OpenRouter, because someone might move between Codex and Claude" is a stance worth keeping.
2. **Their files.** Handoff documents, notes, `AGENTS.md` and `CLAUDE.md` files, research notes, READMEs, and draft docs in their projects. A handoff that says "the author rejected this framing, do not use it" is a real before-and-after.
3. **Their git history.** Commit messages and dates show what was built, when, and in what order.
4. **Their earlier posts.** Stances and stories already published under their name can be referred back to.

Check ownership before you use anything as the author's experience. Run `git log --format=%an` and `git remote get-url origin`: a clone or fork of someone else's project is not the author's work. You may cite it as someone else's example, by name.

Quote only what is safe to publish. Leave out personal details, money, private plans, and anything about other people that the author did not publish themselves. Tell the author in the hand-off which of their files you quoted.

Do not mine an employer's or client's repositories for publishable details. Use only what the author tells you about work projects.

When a fact only the author knows decides what you write (did they hit this problem, have they shipped this pattern, keep or cut this example), ask before drafting, in one round of short multiple-choice questions. Do not guess, and do not fill a request's own unfilled `[brackets]` yourself.

Only when none of these has what a section needs, write `[AUTHOR TO FILL: what is needed]`. A post with placeholders stays `status: draft`.

## Open with a moment

Start with a short, real moment: something the author did, saw, or got wrong, with a date or a concrete detail. Then state the post's main point in one or two sentences.

Do not open with "A question that keeps coming up", "In today's fast-moving world", "Have you ever wondered", or a definition.

## Take a stance where the reader wants one

Add two or three first-person lines where a reader would ask "so what would you do?", usually after a comparison table, at a fork between options, or at the end of a section that lists trade-offs.

- Base each stance on something the author said, did, or already recommends in the post. Turning the post's own recommendation into "I'd ..." is fine. Adding a new opinion is not.
- Keep the stance at the author's strength. "I'd skip it unless you're locked to one vendor" is a stance. "It is never worth it" is an upgrade.
- If a section needs an opinion the material does not support, write `[AUTHOR TO FILL: your view on X]`.
- Ration the stance words. "I'd" and "I would" belong on the two or three strongest stances only; let the author pick them when they have an opinion. Everything else is plain advice in the second person ("Take the budget from the model you're about to call"), still in their voice. A status line such as "This is the design I'd use, not something I've shipped" is not a stance and does not count.

## Say only what the author lived through

- Write a first-person moment ("I found this out when...") only for something the author confirms they hit, with only the details they gave.
- If they say where they used a tool but not what went wrong, state exactly what they said and put a placeholder after it for what happened. Do not let the next paragraph read as their experience.
- Things they have not hit get one or two plain sentences, with the doc quote kept only if it carries the point. No "I", no "we found".
- Label code and designs honestly, in one line next to them: "I run this in production on ...", "I've prototyped it in ...", or "This is the design I'd use, not something I've shipped." If you do not know which, ask; never default to the stronger claim.
- Point to outside examples as outside: "I came across ...", then what the author took from it. Never "a repo I built" or "my setup" for someone else's work.

## Show the real thing

In the section the post exists for, replace at least one generic list or template with the author's actual artifact: a file, a log, a commit, a before-and-after. Show it, then say in one or two sentences what it fixed or prevented. Claim only what the artifact shows. If you cannot tell whether it worked, say what it was for, not that it worked.

- If the artifact was written by a tool or another person and names the author in the third person ("Sam pointed out..."), add one short line before it saying who wrote it, and leave the artifact itself unchanged.

## End on what the author would change

Close with a one- or two-sentence recap of the main rule, then end on the one thing the author would do differently next time, in their words. Ask for it if they have not said; never supply a lesson they did not give.

## Break the symmetry

Posts drafted from a template come out with every section the same length and shape. Fix that on purpose:

- Let the section that carries the post run longest, with detail.
- Cut at least one section to a sentence or two.
- Not every section gets a list or a table. Keep a table only when the reader compares across columns.
- Vary how sections end: some with a stance, some with an example, some just stop.

## Read it aloud

Rewrite any sentence the author would not say to a colleague over coffee.

- Use contractions: it's, don't, you'll, I'd.
- Prefer plain words: "use" over "utilize", "about" over "approximately", "so" over "therefore".
- Mix short sentences with a few longer ones.
- Cut stock phrases: "The short answer:", "The real question is", "It's worth noting", "In conclusion", "Let's dive in", "Here's the thing", "At the end of the day", "X are no different", "put it plainly", "Simply put".
- Break templated cadence: a pair of clipped declaratives that set up a contrast ("You can't hand over the session. You can hand over files.") reads like house style. Join them, or say it the way you'd say it out loud. Keep some short sentences; just stop them arriving in matched pairs.
- Do not write a section as a run of parallel bold labels, each a doc quote followed by a rule. That is documentation. Use prose, or a shorter list with uneven items.
- Headings say what the section is about in the author's words. Drop a "Takeaways" heading when the last section can just end on what to do; keep it only if a list of actions is the clearest ending.

## When revising an existing post

- Do not change technical claims, product names, numbers, or code.
- Keep every direct quote exactly as written, under its current attribution.
- Leave any section the author marked "don't touch" alone, apart from small transition fixes.
- Keep the length within about 10% of the original, and inside the reading-time cap. Count without placeholders, and tell the author roughly how many words each placeholder has room for.
- After the revision, outside the post, list every placeholder left, every file of the author's you drew on, and the one or two changes you are least sure about, such as a stance you inferred or an example you framed.
