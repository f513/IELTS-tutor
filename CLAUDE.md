# IELTS Tutor — memory for this repo

**Read `STATUS.md` first, always.** It's the live checkpoint: what's done,
what's running in the background, what to do next, and how to resume if a
background process died (containers can restart silently — this has
happened before). `PLAN.md` has the full static architecture/plan if you
need more context than STATUS.md's summary.

## One-paragraph summary

We're analyzing all 421 videos of the YouTube channel **IELTS Advantage**
(@Ieltsadvantage) to build a Claude Code multi-agent IELTS tutor: 4
specialists (`.claude/agents/ielts-{reading,listening,speaking,writing}.md`)
grounded in that channel's actual teaching methodology, plus one orchestrator
(`ielts-tutor.md`) on top. Pipeline: scrape metadata → per-video markdown →
classify (section × subtype) → per-section methodology analysis → write the
agent files. See `PLAN.md` for full detail.

## Do not redo this (already done, check before repeating)

- Channel video list, metadata (title+description+date) for all 421 videos:
  `data/raw/uploads.json`, `data/raw/info/*.json` (gitignored — rebuild via
  `scripts/scrape.py`, resumable), `data/videos/*.md` (committed).
- Classification of all 421 videos into section × subtype:
  `data/classification.json`, `data/catalog.md`.
- Transcripts: **unavailable**, YouTube blocks it on this environment's
  shared IP (confirmed: literal reCAPTCHA / "Sign in to confirm you're not
  a bot", not a simple rate limit — tried direct HTTP, headless Chromium,
  and a third-party subtitle site, all blocked). `scripts/probe_transcripts.py`
  is a lightweight one-shot check for whether this has lifted — run it
  **at most every 2-3 hours**, never in a tight loop.

## Conventions this repo follows

- Commit and push often (small, incremental commits) — a stop-hook enforces
  this, but more importantly containers here can be reclaimed/restarted
  without warning, so uncommitted work is genuinely at risk.
- `data/raw/info/` and `data/raw/subs/` are gitignored (too many tiny files).
  The committed source of truth is `data/videos/<id>.md`.
- Heavy analysis work is delegated to subagents (Agent tool) in parallel
  batches, not done inline — keeps context small and matches what the user
  asked for (a manager agent coordinating worker agents).
- Every multi-step phase gets its own entry in `STATUS.md` before starting
  and is marked done when finished, so a fresh session (fresh context, or a
  different Claude instance entirely) can pick up exactly where this one
  left off without re-deriving decisions already made.
