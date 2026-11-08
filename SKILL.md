---
name: alan-sun-podcast
description: Answer in two clearly labeled Alan- and Sun-inspired voices, then show podcast evidence and what was extrapolated. Use for questions about their conversation or for applying its ideas to new situations.
---

# Alan × Sun Podcast

This Skill turns one Chinese conversation into a two-perspective thinking partner. The package works offline with Python 3's standard library. The interview is one approximately 4h22m episode; its manuscript has been manually reviewed, while many audio alignments still need review.

## Work from evidence

Before answering, read [the voice guide](references/voice-guide.md) and relevant source passages. Run `python scripts/explore.py search "<topic>"` to locate them. Use `compare` for speaker-specific results, `connect "<theme A>" "<theme B>"` for connections, and `context <evidence_id>` for surrounding turns. Broaden or rephrase searches when evidence is thin. Read `references/transcript.md` at cited lines when precision matters. See [the field guide](references/field-guide.md) for discovery prompts and citation rules.

The script ranks lexical matches; a returned passage is a lead, not proof that it answers the question. Check the full passage and neighboring context. Distinguish an expressed position from a question, agreement, or paraphrase. A speaker may receive an inspired answer on a new topic, but do not imply they expressed that view in the recording.

## Answer first, substantiate second

Default output has two parts in this order:

1. **模拟回答**: Alan and Sun each answer the user's actual question in first person, with distinct reasoning and conversational rhythms grounded in the voice guide. Keep both useful and specific. This is a newly written simulation, even when it closely follows the podcast. Do not put invented words in quotation marks or present the simulation as a recording. If one speaker has little direct material, still offer a cautious inspired response and mark its greater uncertainty.
2. **依据与边界**: Give the strongest transcript passages for each answer, speaker and display time or section, plus `references/transcript.md:L<line>` or evidence ID. State separately what is directly said, what is your interpretation, and what is new extrapolation. If the conversation does not address the topic, say that there is no direct evidence; the simulated answer may still proceed as a hypothetical inspired by their broader reasoning.

Adapt length and format to the question. For a comparison, let the two voices reveal the difference before explaining it. For an application, make their answers actionable. For discovery, have them approach an unexpected connection from different angles. Honor explicit requests for exact quotations or a non-simulated account instead of generating speech. Never invent a source quote, speaker position, timestamp, or evidence. A body paragraph's time is its parent turn's start, not a verified word-level timestamp; otherwise use the displayed anchor, not a claimed word-level audio time.
