---
name: desk-implement-slice
description: Implement one already-authorized, contract-backed Solana Desk code slice with focused regression evidence. Use for a bounded module fix or feature after contract intake; not for policy amendments, broad refactoring, or independent final approval.
---

# Desk implementation slice

**Owns:** one minimal code change; not blueprint interpretation authority or final independent approval.

1. Reconcile `AGENTS.md` hierarchy, current Git status/diff, applicable executable contract and tests with the actual intake baseline and `slice_id`; if the intake record is absent or stale, reconstruct it before editing. If missing contract affects monetary, temporal, persistence or experimental semantics, route to `desk-contracts` before coding. Preserve unrelated working-tree/staged edits; do not start overlapping writers.
2. State the exact active-rule/OD/test IDs, observable success and failure, exclusive file ownership, and narrow implementation. Never infer prerequisites from filename existence: verify actual contract acceptance and preceding §16 phase evidence. Use blueprint §§3–14 for behavior, especially §6 actual processing/availability time, §9 all-or-none source-model quotes, §10 integer accounting and §12 commit/recovery. **No** wallet, signer, transaction building, simulateTransaction, paid provider or live order path.
3. Implement only the selected slice using existing patterns. Do not change thresholds, hypothesis selection, frozen calendar, failure types or dependency locks merely to make tests pass. External-source uncertainty receives the specified typed block; synthetic implementation is not provider compatibility.
4. Execute focused tests including at least one negative/boundary case capable of catching the changed failure, then applicable required checks. For money/time/order/store/replay effects, hand off to `desk-fault-verification`; for decoder/curve code, `desk-reference-parity`. If tooling or fixture is unavailable, state the exact missing gate rather than substitute an assertion. Capture diff identity and commands/results once for both specialist reviewers; run parity and fault work independently when both apply, then reconcile their findings.
5. Recheck final diff against initial baseline for unrelated edits, weakened tests, changed generated files and unexpected artifacts. Send actual diff, baseline identity, rule/test IDs, test receipts and parity/fault dispositions to independent `desk-review-gate`; if unavailable, mark review NOT_RUN and do not self-promote. Any fix after review invalidates the affected receipts and review until rerun; a subagent assertion alone cannot promote the phase.

Stop at the first verified coherent slice. Report files, commands/exit results, pre-existing versus introduced failures, and remaining uncertain behavior. Do not push, deploy, publish or modify host configuration.

## Executable integration (v1.1)

Use `tools.control_plane.record` for fresh source-bound focused and required checks. Do not rely on plain exit-code text; `tools.control_plane.gate` requires matching current receipts and minimum test counts.
