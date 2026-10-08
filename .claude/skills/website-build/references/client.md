# Client feedback, pushback and records

The client owns the call. You own the options, the honesty and the record.

## Logging feedback

Every note from the client goes into the feedback log verbatim, with the date and what they had just
seen, names as given. Under it, a dated "what this changes" list, what was done and where, and what was
left open. The client's exact words settle later disagreements about what was asked; a paraphrase does
not. Template: `assets/client-feedback.md`.

Read the note for scope as well as content. "We just want it to look cohesive, blue, white and gold,
the typeface, possibly the three bars, but don't overthink it" says: do those three things, show them,
stop. "Probably no content published there" says: the page points to the content, it does not host it.
"Small project" is a budget signal: meet it with smaller scope and separable options, not a discount.

When a stakeholder note changes the brief (family cohesion, smaller scope), pause work it may
invalidate, build new variants without mutating the old, and map which open audit findings disappear by
cutting scope. Before stripping sections or motion to match a leaner brief, list what the client
considers signature or core and confirm the section list; a lean flag that hid the creators section had
to be reversed the same day.

## When the user corrects you

A correction is a rule for the rest of the project. Write it into the decision record the same turn and
follow it from then on. Carry earlier instructions forward into later rebuilds and regression-check
approved details after every rebuild; a rebuild once dropped an approved pulsing period.

Examples of corrections and the rule each became:

- "I said just the bars if they can work." Do the thing asked, nothing beside it. An unasked element
  gets removed without defending it.
- "Don't use the Red Hat Display." Remove it everywhere, including the variants, and say so. A change
  being license-safe and on-brand is not permission.
- "Don't tell me they're live until they are." Verify by hash after the cache window, every time.
- "The photos don't need credits, they're just for example." Captions and credits off the page; keep
  them in the credits file.
- "The names should be the identifiers, not the towns." Rebuild the component around the rule, do not
  patch the label.
- "Can you use v2 in the URL vs lean." Rename the path, leave redirects at the old one.
- "I want the previous creator section from the first preview." Restore it whole from the record and
  the git history (markup, styles, script), re-fit it, and say what the return costs.
- "Just need a comparison sheet, not apply to the site yet." A scope boundary: build the sheet, leave
  the live pages untouched, say so in the caption.
- "Save this but keep pushing." Commit the current state first, then explore, and report what held and
  what did not with the mechanical reason.
- "Make the informed decision." Decide with the smallest reversible change, explain it, and accept being
  overruled: revert cleanly and keep the data in case it returns.

When you raise a concern and the user repeats the request, the repetition is the decision. Do it, say
that you did, and move on. Do not re-argue a settled decision in a later message.

## Pushback and disagreement

- When the client rejects your recommendation or cannot tell two options apart, concede in one sentence,
  stop arguing, build their pick as well as it can be built, solve the objection you raised (with a size
  system, not a restatement), and record the trade as a decision, not a mistake.
- Answer "is there a better way" with a built comparison on the real surfaces at working sizes, graded,
  with a recommendation, the honest alternative and "nothing changes until you choose". When a request
  is ambiguous, build several readings of it.
- When the client repeats a complaint you cannot reproduce ("still looks green"), assume they are right.
  Widen the search to the token, the field and their device, measure their own screenshot, and explain
  the perceptual cause with concrete levers. The client's eye on their device outranks the hex.
- When several notes arrive in one message, acknowledge them by count, work them in the client's order,
  and answer each under its own label: done, fixed, unchanged and why.
- When a whole round is rejected, stop producing more sheets. Diagnose the pattern in your own method,
  offer structurally different ways out, ask for one reference, admit the limits of code-drawn artwork,
  and write a self-contained brief if the work goes to another tool or person.
- Give an honest no when asked directly, even when the client may like the option. Tell the client when
  to stop adding scope.
- When a fix you made breaks the thing an element exists for, say so, state the constraint as
  arithmetic, offer two or three options with their costs, and recommend one before building.

## Retiring a concept

When the client picks one concept, retire the other cleanly the same turn: redirect its address, keep
its record entry with the date and who decided, carry across anything the survivor adopted (a footer
rule, a device), and remove its toggle. Keep its pages reachable for comparison until told otherwise.
Move exploration to the survivor.

## The decision record

One file, newest at the bottom, one entry per pass. It opens with a dated "where things stand" summary,
a decisions table (element, decision, why, who chose and when, where the rejected alternative is kept),
an open list and a files list. Each entry says what was done and why, names the sheet that shows it and
the script that built it, records what was tried and set aside with the mechanical reason, quotes the
client's words, distinguishes "my read" from "client call", and closes with what is open. Record client
reversals of strategy as the client's decision citing the document reversed, guardrail exceptions as
client-directed naming the rule, and measured numbers as numbers. Each decision yields a one-line guide
rule written at the moment of the decision. Template: `assets/decision-record.md`.

Write the entry in the same command as the commit. A record written later is a reconstruction. Read the
tail before appending so nothing is logged twice; re-check numeric claims when code changes a threshold;
update the builder docstring in the same commit when a section comes or goes.

## The QA record

One section per audit pass with the viewports and conditions, the findings fixed, and the findings
accepted with the reason. Accepted findings matter as much as fixed ones; they stop the next pass from
rediscovering them. Template: `assets/qa-record.md`.

## Session handoffs

When a session continues from a summary, the summary carries the standing rules verbatim (copy rules,
banned words, guardrails), the user's non-negotiable quotes, the decisions made so far, the requests in
order, and the environment state (branch, deploy clone path, attribution lines, verification rule). A
fresh context that lacks these re-litigates settled decisions.

## Showing work

Send a screenshot sheet with every round, built from the state that changed, at the size the client
looks at. Before and after on the same mockup when the client asked for a change. Competing directions
on identical mockups. The phone when it is a phone fix. A one-sentence caption naming what each row is
and which option is applied or recommended. Annotate capture artifacts (fonts fell back, bar caught
mid-scroll). Motion as a GIF, a strip at named scroll positions, or the live page with "what to look
at". Name what is phone-only so a client on a desktop knows why they do not see it.

## How to talk about it

- One plain line before each working step (reproducing, measuring, committing) so the user can follow
  and redirect early.
- Lead with the result and the link (live URL, commit). Then: what was wrong, what it is now, the
  judgment call. Or: what I tested, what I applied, the other option if you want it.
- Numbers in a table, before and after.
- Present options with numbered rules and a first-pass grade split into better than, weaker than, and
  watch. Every grade ends with what holds it back and what would move it up a grade.
- Report what did not hold and why it was worth trying, with the mechanical reason. Name the weakest
  pixel on the page before the client finds it. Own mistakes without hedging. Say plainly when an
  instruction cannot be executed and how you interpreted it, and when a render or upload failed and
  where the file lives instead.
- Answer conceptual questions ("what is a brandmark versus a logo", "how do email and Substack fit")
  with a short structured explainer anchored in the project's own examples, ending in the decisions it
  implies.
- Report the environment in three buckets: used, blocked with the exact fix, wanted but absent. State
  the limits of the test environment (Chromium, no Safari) and ask for the device and browser when a
  bug cannot be reproduced.
- End with one numbered list of the decisions still open on the client's side and the placeholders
  still to confirm, repeated verbatim until made, and an offer of the specific next render rather than
  "what next".
- Do everything that does not depend on an answer first. State the assumption you made and keep
  building. Ask only when the readings would lead to materially different work, in one line with the
  options named.
