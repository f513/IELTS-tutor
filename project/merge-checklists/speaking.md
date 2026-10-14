# Speaking merge checklist

A = `.claude/agents/ielts-speaking.md`, B = `.claude/skills/ielts-tutor/references/speaking.md`, M = `_merge/speaking.md`.
Overall: B is a condensed rewrite of A. Almost every B item is also in A, and A is usually more detailed. M keeps A's fuller wording and drops B's shorter restatements.

| item | in A | in B | where in merged file (section heading) | note |
|---|---|---|---|---|
| YAML frontmatter (name, description, tools, model) | Y | N | (omitted) | Excluded by spec; belongs to the future thin wrapper |
| Text-based medium, no audio in/out, pronunciation can't be assessed, say so upfront | Y | Y | Speaking — reference (purpose note); Identity and philosophy | Also in Exam mode step 1 |
| Grounded in 179 Speaking videos + 3 transcripts (6.5/7.5/8) | Y | Y | Speaking — reference (provenance) | Video IDs added from data/analysis as citations |
| Host Chris, not a generic bot reciting band descriptors | Y | Y | Identity and philosophy | |
| Philosophy 1: communication over perfection; over-rehearsed English lowers score | Y | Y | Identity and philosophy | A wording kept ("only matter insofar as they serve...") |
| Philosophy 2: develop answers; 83 exam / 61 training-advice / 35 tips / 3 transcripts | Y | Y | Identity and philosophy | Numbers kept |
| Philosophy 3: memorization is detectable by the examiner and lowers the score | Y | Y | Identity and philosophy | |
| Tone: warm, direct, encouraging; praise first; explain why | Y | Y | Identity and philosophy | |
| Format facts: 11–14 min; P1 ~4–5; P2 1-min prep, up to 2 min; P3 ~4–5; same for Academic and GT | Y | Y | Identity and philosophy | |
| Pronunciation-specific techniques: explain, don't score | Y | Y | Identity and philosophy | |
| Answer development formula: answer → reason → example/2nd perspective | Y | Y | Core techniques > Answer development | Confirmation level stated |
| Formula is not an invented acronym | Y | Y | Core techniques > Answer development | |
| Anti-listing | Y | Y | Core techniques > Answer development | |
| "Not too short, not too long"; over-talking is a failure mode (rattles candidate, costs coherence) | Y | Y (partial) | Core techniques > Answer development | A's "rattle/coherence" detail kept |
| Direct-answer-first; don't bury under preamble | Y | Y | Core techniques > Answer development | |
| Systematic-error rule: slip vs pattern; "the most hard part"; "everyone has little slips"; caps ~Band 6 | Y | Y | Core techniques > The "systematic error" rule | A's examples (articles, comparatives) kept |
| Name slip vs pattern explicitly, not "some grammar errors noted" | Y | Y (partial) | Core techniques > The "systematic error" rule | |
| 100% rule: risks in practice, certainty in the test; failed fancy word costs more | Y | Y | Core techniques > The vocabulary "100% rule" | |
| "Right way to build vocabulary" = when you take risks, not a ban | Y | N | Core techniques > The vocabulary "100% rule" | |
| Lifting weights: 50kg vs 150kg | Y | Y (no numbers) | Core techniques > The vocabulary "100% rule"; Coaching analogies | |
| Quote "I never like to tell people to use a wider range..." | N | N | Core techniques > The vocabulary "100% rule" | Added from data/analysis (Band 7.5) as a citation for the existing claim; flagged |
| P1: easiest angle, not a knowledge test, trivial inaccuracy not penalized | Y | Y | Core techniques > Part-specific techniques | Transcript note kept (Band 7.5 per analysis) |
| P1: 2–3 sentences + one example; no single-word answers, no monologue | Y | Y | Core techniques > Part-specific techniques | |
| P2: extra ammunition, 2–4 bullets beyond the card (Band 6.5) | Y | Y | Core techniques > Part-specific techniques; Operating modes > Exam mode | |
| P2: use real life (Band 7.5 praise) | Y | Y | Core techniques > Part-specific techniques | |
| P2: steering toward expertise; don't force it (coffee example) | Y | Y (no example) | Core techniques > Part-specific techniques | Coffee example from A kept |
| P3: define abstract terms ("mindset") | Y | Y | Core techniques > Part-specific techniques | |
| P3: multi-perspective expansion template | Y | Y | Core techniques > Part-specific techniques | |
| P3: English test, not a knowledge test (or IQ test); confirmed at 6.5 and 7.5 | Y | Y | Core techniques > Part-specific techniques | "IQ test" from A |
| Analogy: broken car | Y | Y | Core techniques > Coaching analogies worth reusing | A's detail (strengths near ceiling) kept |
| Analogy: computer under stress (quieter, flatter, repetition, slips) | Y | Y | Core techniques > Coaching analogies worth reusing | |
| Analogy: lifting weights | Y | Y | Core techniques > Coaching analogies worth reusing | |
| Analogy: friend in a coffee shop | Y | Y | Core techniques > Coaching analogies worth reusing | |
| Ask the examiner to repeat/clarify | Y | Y | Core techniques > Other channel-confirmed techniques; Tips mode | |
| Scored test starts after the intro | Y | Y | Core techniques > Other channel-confirmed techniques; Tips mode | |
| Paired/comparison exercises | Y | Y | Core techniques > Other channel-confirmed techniques | |
| Band-jump framing (6→8, 6.5→7.5, 1.5 bands in a week) | Y | Y (no 6.5→7.5) | Core techniques > Other channel-confirmed techniques | All three examples kept |
| UNCONFIRMED: PPF Method | Y | Y | Explicitly UNCONFIRMED frameworks | |
| UNCONFIRMED: 9 Most Common Sentence Patterns | Y | Y | Explicitly UNCONFIRMED frameworks | |
| UNCONFIRMED: Part 2 unique step-by-step strategy | Y | Y | Explicitly UNCONFIRMED frameworks | |
| UNCONFIRMED: "5 frameworks"/"3 tricks" inconsistency | Y | Y | Explicitly UNCONFIRMED frameworks; Known gaps | Was only in Known gaps; also listed by name in the UNCONFIRMED section |
| UNCONFIRMED: "4 things the examiner tracks" | Y | Y | Explicitly UNCONFIRMED frameworks; Known gaps | Same as above |
| Official 4 criteria, no invented rubric | Y | Y | Scoring criteria framing | |
| Feedback order P → LR → GRA → FC, after part-by-part | Y | Y | Scoring criteria framing; Exam mode | |
| FC: idea pauses vs language pauses; coherence = development; "improve in a day" | Y | Y | Scoring criteria framing | |
| LR: accuracy + range | Y | Y | Scoring criteria framing | |
| GRA: range + accuracy; systematic-error rule | Y | Y | Scoring criteria framing | |
| P: clarity (100%, else ≤6) + higher-level features; accent not an axis | Y | Y | Scoring criteria framing | |
| Accent interference = blocks specific words, not "sounding foreign" | Y | N | Scoring criteria framing | |
| Scores not siloed; don't "hit the rubric" (idiom example) | Y | Y | Scoring criteria framing | |
| Idioms/accent/body language not levers | Y | Y | Scoring criteria framing | |
| Cal 6.5: Indian student in Dubai; P1 topics | Y | Y | Calibration examples > Band 6.5 | |
| Cal 6.5: P2 perfect-weather day, Dubai thunderstorm, ~2 min, repeated detail = stalling | Y | Y (partial) | Calibration examples > Band 6.5 | |
| Cal 6.5: P3 topics | Y | Y | Calibration examples > Band 6.5 | |
| Cal 6.5: "like talking to a friend"; P3 attempt praised | Y | Y | Calibration examples > Band 6.5 | |
| Cal 6.5: nerves not competence; calm = 9/9/9 + vocab 8; −1 band under stress | Y | Y | Calibration examples > Band 6.5 | |
| Cal 6.5: vocab "played it safe" | Y | Y | Calibration examples > Band 6.5 | |
| Cal 6.5: takeaway (mid-band score with near-top skill; check confidence first) | Y | Y | Calibration examples > Band 6.5 | |
| Cal 6.5: volume tip came from this test | N | N | Calibration examples > Band 6.5; Tips mode | Source attribution added from data/analysis; the tip itself is in A and B |
| Cal 7.5: marketing professional; P1 coffee-chain job, podcasts/gaming, Hyderabadi biryani, museums | Y | Y (partial) | Calibration examples > Band 7.5 | A's specifics kept |
| Cal 7.5: P2 campaign story; "footfall," "activations," "brand campaign of the year" | Y | Y (2 of 3 terms) | Calibration examples > Band 7.5 | No cue card read aloud (per analysis) |
| Cal 7.5: P3 topics (dissatisfaction, satisfying life, salary vs team) | Y | Y | Calibration examples > Band 7.5 | |
| Cal 7.5: P1 coached off "correct" fact; P2 "excellent"; P3 surface-level, "mindset" | Y | Y | Calibration examples > Band 7.5 | |
| Cal 7.5: Fluency 8 (Elon Musk comparison) | Y | Y (no Musk) | Calibration examples > Band 7.5 | |
| Cal 7.5: Pronunciation 8 (100% comprehensible, intonation/stress) | Y | Y (partial) | Calibration examples > Band 7.5 | |
| Cal 7.5: Vocab 7 (lifting weights) | Y | Y | Calibration examples > Band 7.5 | |
| Cal 7.5: Grammar weak point "most hard," "more easier", non-systematic | Y | Y | Calibration examples > Band 7.5 | |
| Cal 7.5: Overall 7.5, "master's degree... any visa" | Y | N | Calibration examples > Band 7.5 | |
| Cal 8: 2019 flagship template; clothing cue card verbatim | Y | Y (no 2019) | Calibration examples > Band 8 | |
| Cal 8: P1 studies/free time/travel; P3 designer clothes, work clothes, dress codes, Google | Y | Y (no dress codes/Google) | Calibration examples > Band 8 | |
| Cal 8: P1 too short; "go on until they stop you" vs "not too short, not too long" | Y | Y (no "go on...") | Calibration examples > Band 8 | |
| Cal 8: P2 full two minutes; P3 needs reasons/examples | Y | Y | Calibration examples > Band 8 | |
| Cal 8: Pron 8 minor accent interference; Vocab 8 but maybe 7 on test day (100% rule origin); Grammar 8 | Y | Y | Calibration examples > Band 8 | |
| Cal 8: coherence "improve in a day"; overall 8; higher potential from development alone | Y | Y (partial) | Calibration examples > Band 8 | |
| Cross-band pattern (under-development; mechanism by band) | Y | Y | Calibration examples > Cross-band pattern | Shown as a table |
| Coverage gap: no Band 5/6/7 transcript; strongest 6.5–9 | Y | Y | Calibration examples > Cross-band pattern; Known gaps | |
| Part 1 topic bank (39 topics) | Y | Y | Topic banks for realistic questions | Identical lists |
| Opener "Do you work, or do you study?" | Y | Y | Topic banks; Exam mode | |
| Topic difficulty doesn't scale with band; stricter evaluation instead | Y | Y | Topic banks for realistic questions | |
| Part 2 cue card format (topic line + 3–4 prompts; "Describe the type of X that...") | Y | Y (partial) | Topic banks for realistic questions | |
| Part 3 question patterns (cause/effect, societal, comparative, one hard question) | Y | Y | Topic banks for realistic questions | A's example phrasings kept |
| Announce the mode | Y | N | Operating modes | |
| Training mode steps | Y | Y | Operating modes > Training mode | |
| Exam mode: register and opener | Y | Y | Operating modes > Exam mode | |
| Exam mode: preface, P1 4–6 Qs one at a time, P2 prep notes + ~200 words, P3 4–6 Qs incl. one hard | Y | Y | Operating modes > Exam mode | |
| Exam mode: break character line; feedback structure; overall band; 1–2 next steps | Y | Y | Operating modes > Exam mode | |
| Advice: stuck at 6.5 (mock vs real, nerves, trying too hard) | Y | Y | Operating modes > Advice mode | |
| Advice: freezing in Part 3 | Y | Y | Operating modes > Advice mode | |
| Advice: can't extend answers | Y | Y | Operating modes > Advice mode | |
| Tip: vocabulary swaps + 100% caveat | Y | Y | Operating modes > Tips mode | |
| Tip: word repetition | Y | Y | Operating modes > Tips mode | |
| Tip: answer + one sentence | Y | Y | Operating modes > Tips mode | |
| Tip: ask for clarification | Y | Y | Operating modes > Tips mode | |
| Tip: don't over-invest in the intro | Y | Y | Operating modes > Tips mode | |
| Tip: volume, examiner twice as far away | Y | Y | Operating modes > Tips mode | |
| Tip: opener variety by question type | Y | Y | Operating modes > Tips mode | |
| Honesty: never invent PPF/9 patterns/P2 strategy; scripted reply | Y | Y | Honesty rule | |
| Honesty: no "revealed" framing; confirmed vs unconfirmed labels | Y | Y | Honesty rule | |
| Honesty: L1 grammar claim (Russian articles) is an anecdote | Y | Y (no example) | Honesty rule; Known gaps | |
| Honesty: Top 20 idioms, only 1 confirmed | Y | Y | Honesty rule; Known gaps | |
| Honesty: low-band calibration uses generic knowledge | Y | Y | Honesty rule | |
| Gap: idiom stance unresolved | Y | Y | Known gaps | |
| Gap: external PDFs/workbooks | Y | Y | Known gaps | |
| Gap: examiner identity (Chris dual role) | Y | Y | Known gaps | |
| Gap: only 2 of 179 P2 cue cards confirmed | Y | Y | Known gaps; Topic banks | See conflict 1 |

## Conflicts resolved

1. **Status of the weather cue card.** A's Known gaps says "clothing; weather, inferred." B's Known gaps says "(clothing; weather)" with no qualifier, and A's topic-bank section calls both "confirmed real cards." data/analysis/speaking.md (Band 6.5 entry) says the card was "inferred from content, not read aloud on camera." **Resolution**: M says clothing is confirmed verbatim and weather is inferred, in the Calibration (Band 6.5), Topic banks and Known gaps sections.
2. **Band 7.5 Part 2 (precision, not a direct A/B clash).** Both A and B present the marketing story as the Part 2 answer. data/analysis says no cue card was read aloud on camera and that the story "plausibly serves this role." **Resolution**: M adds "no cue card text is read aloud on camera."
3. **Section cross-references.** A refers to numbered sections ("Section 2", "Section 5"). **Resolution**: M uses section headings by name, since its structure differs.

## Dropped (true duplicates only)

- All of B's condensed restatements of A's content (B adds no unique facts). A's fuller wording was kept in every case.
- A's "See Section 6 for how to handle..." pointer, replaced with a pointer to the Honesty rule heading.
- A's YAML frontmatter, excluded by spec rather than as a duplicate. It belongs to the future wrapper.
