---
name: desk-task-intake
description: Scope a new Solana Desk implementation or bug-fix task into a verified baseline, blueprint rule IDs, ownership, and acceptance plan before edits. Not for performing edits, independent review, or host qualification.
---

# Desk task intake

**Owns:** read-only task qualification and an actionable handoff to `desk-contracts`, `desk-implement-slice`, or a verification workflow. Do not edit product or contracts in intake.

1. Read applicable root/scoped `AGENTS.md` and locate the authoritative v2.6 blueprint by confirmed repository path; use `docs/blueprint/solana-overnight-trading-desk-blueprint-v2.6-consolidated.md` and `control-plane/phases/README.md` when present. Missing paths are missing prerequisites, not evidence of another authority. Do not invent phase completion. Inspect current Git HEAD, status, staged/unstaged diffs, relevant code/tests and available phase evidence. If this is an extracted archive without `.git`, report **NO_GIT_BASELINE**; never invent a clean tree.
2. Identify exact active blueprint section(s), OD IDs, acceptance IDs and phase prerequisites. Check whether the task is already done, partially implemented or blocked. Compare with `contracts/ACTIVE_RULES.json` and traceability records **if they exist**; absent deliverables are a dependency, not a made-up mapping.
3. Select **one smallest coherent slice** within the blueprint §16 dependency order (contracts → ledger/replay → provider → execution/risk → strategy/reports → host). A later phase can proceed only if its prerequisite contracts and relevant offline evidence exist; independent non-dependent work may proceed. Record files/owners, read/write boundaries, prerequisite contracts and regression-sensitive invariants. Flag any economic, provider, security, compatibility, experimental or failure-policy choice that blueprint v2.6 does not delegate. Do not silently choose new thresholds or widen paper-only scope.
4. Define verification **before implementation**: focused positive and negative cases, relevant hand-calculated fixtures (§18), the independent reviewer/fault or reference checks needed, and applicable project gate (`control-plane/verification-map.json`). Distinguish checks possible offline from host/provider gates.
5. Hand off a compact record with `baseline_ref`, `blueprint_hash`, active rule/OD/test IDs, phase and prerequisite status, `slice_id`, exclusive write ownership, intended diff, independent oracles, planned commands, missing evidence, blockers and `next_skill`. Values are evidence references, not invented hashes. Route missing/contradictory contracts to `desk-contracts`, approved implementation to `desk-implement-slice`, post-change faults/parity to their specialists, and final independent decision to `desk-review-gate`. Stop if baseline ownership conflicts, authority is missing or the slice would depend on an unapproved normative decision. Do not claim tests have run because a plan lists them.

Use `python -m tools.control_plane.baseline` only if that command is available in the checkout; verify its result and never treat its Git failure as a clean baseline.

## Executable integration (v1.1)

After baseline inspect `python3 -m tools.control_plane.tasks next`; generate a task-specific source-excerpt brief with `tools.control_plane.context`. Task eligibility is not proof that phase contracts are complete. Persist a read-only handoff with `tools.control_plane.handoff` if interrupted.
