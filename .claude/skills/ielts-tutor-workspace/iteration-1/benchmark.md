# Skill Benchmark: ielts-tutor

**Model**: claude-sonnet-5
**Date**: 2026-10-06T00:00:00Z
**Evals**: 1, 2, 3, 4, 5 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|----------------|-------|
| Pass Rate | 100% ± 0% | 94% ± 8% | +0.06 |
| Time | 118.3s ± 64.6s | 85.6s ± 51.1s | +32.8s |
| Tokens | 71474 ± 5958 | 57112 ± 4528 | +14362 |

## Per-eval pass rate

| Eval | With Skill | Without Skill |
|---|---|---|
| 1. reading-exam-matching-headings | 6/6 (100%) | 6/7 (86%) |
| 2. listening-stuck-band-diagnosis | 5/5 (100%) | 5/5 (100%) |
| 3. speaking-full-mock-test | 7/7 (100%) | 6/7 (86%) |
| 4. writing-essay-grading | 6/6 (100%) | 6/6 (100%) |
| 5. honesty-rule-ppf-method | 5/5 (100%) | 5/5 (100%) |

## Notes

- Pass-rate delta is small (+0.06) because 3 of 5 evals (listening, writing, honesty) pass 100% in both configurations — those assertions check correctness/safety properties a strong base model already handles well, not channel-specific grounding.
- The two evals with a real pass-rate gap (reading, speaking) both fail the baseline on a concrete, meaningful behavior: the baseline reading run refuses to give any band estimate at all, and the baseline speaking run buries its text-based-limitation caveat at the end instead of stating it upfront.
- Across evals 2, 4, and 5, the real differentiator is qualitative grounding (named channel frameworks, cited transcript/video counts) rather than pass/fail — the current assertions under-test this; see eval_feedback in the per-run grading.json files for suggested stronger assertions.
- with_skill runs took noticeably longer and used more tokens on the 3 content-heavy evals (reading, speaking, writing), consistent with loading a ~300-430 line reference file before doing that work.
- Sample size is 1 run per configuration per eval, so stddev/min/max reflect across-eval variance, not run-to-run noise.
