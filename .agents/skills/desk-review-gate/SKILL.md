---
name: desk-review-gate
description: Independently review a concrete Solana Desk candidate diff, contract traceability, and executed verification receipts before gate promotion. Not for authoring the patch, accepting the author's summary, or declaring host/provider readiness from offline checks.
---

# Desk independent review

**Owns:** a fresh-context correctness assessment of a specific candidate, not its implementation. Read `AGENTS.md`, affected blueprint sections, scoped instructions and the **actual** diff against recorded baseline.

1. Identify exact commit/worktree, staged and unstaged changes, files, blueprint/OD/acceptance IDs and whether the diff changed after evidence was collected. A stale review or unavailable baseline is INCONCLUSIVE, not an approval. Inspect code, contracts, tests, generated outputs and nearby consumers; do not rely on a completion narrative. Confirm intake/contract/implementation evidence all identify the same candidate and correct §16 dependency phase; an unmatched handoff is INCONCLUSIVE.
2. Attempt to falsify changed behavior: inspect counterexamples for time/availability/generation, source-model arithmetic and source provenance, risk/equity/fee conservation, order lifetime, persistence, campaign isolation and deterministic replay where applicable. Check that test expectations are independent and failures are not hidden by changed assertions.
3. Check actual command outputs or receipts against applicable blueprint §17–18 gates and `control-plane/verification-map.json` **only when that manifest exists**. If `tools.control_plane.gate` is available, treat it as receipt assertion checking, **not** command authenticity or blueprint completion; missing tooling is NOT_RUN, not automatic approval. Determine whether evidence is relevant, current to the diff, independently reproducible and sufficient for each claimed gate. Mark missing provider/WSL/reference tests explicitly NOT_RUN or BLOCKED.
4. Record findings by severity, exact file/line or rule ID, reproduction or logic trace, consequence, and disposition. Distinguish confirmed defects, suspected risks and evidence gaps. Require the author to remediate and obtain fresh checks after patch change; do not silently patch from the reviewer role.
5. Return APPROVE_FOR_NEXT_GATE only when no critical findings remain, all **applicable** verification obligations actually have evidence, and test receipt/diff hashes still match; otherwise BLOCKED or INCONCLUSIVE with focused next action. A clean review is not proof of profitability, verified deployed binary, provider terms or live execution safety.

The reviewer does not modify the candidate; any remediation returns to `desk-implement-slice` and invalidates stale review evidence. Hand off an explicit phase-scoped disposition and evidence IDs to `desk-host-handoff` only after offline review succeeds. No commit, push, merge, publish or promotion to a higher application label by implication.

## Executable integration (v1.1)

If independently authorized to review, inspect actual diff and record an explicit assertion using `tools.control_plane.review`. This merely records your assertion; it does not authenticate reviewer independence. Verify against current candidate using `tools.control_plane.gate`.
