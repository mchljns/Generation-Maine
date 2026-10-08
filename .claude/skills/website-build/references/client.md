# Client feedback, pushback and records

## Logging feedback

Every note from the client goes into the feedback log verbatim, with the date and what they had just
seen. Under it, what was done and where, and what was left open. The client's exact words settle later
disagreements about what was asked; a paraphrase does not. Template: `assets/client-feedback.md`.

Read the note for scope as well as content. "We just want it to look cohesive, blue, white and gold,
the typeface, possibly the three bars, but don't overthink it" says: do those three things, show them,
stop. "Probably no content published there" says: the page points to the content, it does not host it.

## When the user corrects you

A correction is a rule for the rest of the project. Write it into the decision record the same turn
and follow it from then on. Examples of corrections and the rule each became:

- "I said just the bars if they can work." Do the thing asked, nothing beside it. When you added a
  second element the client did not ask for, remove it without defending it.
- "Don't use the Red Hat Display." Remove the font everywhere, including the variants, and say so.
- "Don't tell me they're live until they are." Verify by hash after the cache window, every time.
- "The photos don't need credits, they're just for example." Captions and credits off the page; keep
  them in the credits file.
- "The names should be the identifiers, not the towns." Rebuild the component around the rule, do not
  patch the label.
- "Can you use v2 in the URL vs lean." Rename the path, leave redirects at the old one.
- "I want the previous creator section from the first preview." Restore it from the record and the
  git history; do not approximate it.

When you raise a concern and the user repeats the request, the repetition is the decision. Do it, say
that you did, and move on. Do not re-argue a settled decision in a later message.

## Retiring a concept

When the client picks one concept, retire the other cleanly: redirect its address, keep its record entry
with the date and who decided, carry across anything the surviving concept adopted (a footer rule, a
device), and remove its toggle. The record should let a reader see what the other concept was without
the page existing.

## The decision record

One file, newest at the bottom, one entry per pass. An entry says what was done, why, what was tried
and set aside, what the client said in their words, and what is open. Name the file or page it lives
in. Template: `assets/decision-record.md`. Write it in the same turn as the work; a record written
later is a reconstruction.

Keep a "Decisions so far" list at the top and an "Open" list under it, so a new session can start from
the state without reading the history.

## The QA record

One section per audit pass with the viewports and conditions, the findings fixed, and the findings
accepted with the reason. Template: `assets/qa-record.md`. Accepted findings matter as much as fixed
ones; they stop the next pass from rediscovering them.

## Showing work

Send a screenshot sheet with every round, built from the state that changed, at the size the client
looks at. Before and after when the client asked for a change. The phone when it is a phone fix. Name
what is phone-only so a client on a desktop knows why they do not see it.

Lead the message with the outcome and anything you could not verify. Keep the sentences short. Numbers
in a table. No praise of your own work.

## Uncertainty and questions

Do everything that does not depend on the answer first. State the assumption you made and keep
building. Ask only when the readings would lead to materially different work, and ask in one line with
the options named.

When something cannot be done from the sandbox (a site unreachable, no encoder, a license not in hand),
say so, say what you did instead, and put the remainder in the open list.
