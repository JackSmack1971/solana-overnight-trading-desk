---
name: desk-fault-verification
description: Verify Solana Desk financial, time, lifecycle, persistence, crash, and replay failure invariants after affected code or contract changes. Not for generic unit-test execution, implementing the fix, or running actual provider campaigns.
---

# Desk invariant and fault verification

**Owns:** adversarial evidence for a bounded change; blueprint §§6, 9–12, 14, 17–18. Read applicable scoped `AGENTS.md` if present, executable contracts and the actual changed diff; missing test fixtures are unverified prerequisites, not permission to synthesize expected outputs from code under test. Use isolated disposable roots; no real wallets or network side effects.

1. Freeze the exact candidate diff, test seed/fixtures, baseline outcome and specified rule IDs. Select fault classes affected by the diff, not every conceivable test. Independent fixture calculations must not derive their expectations from implementation output.
2. For money/order changes test double submission, duplicate idempotency key, fee-on-failed-order, failed sell with inventory unchanged, zero/unknown mark differentiation, portfolio isolation and per-asset integer ledger balance as applicable. Verify no silent rounding or fabricated close (§§9–10,12).
3. For clock/collection changes test actual-time deadline equality vs late processing, received/available boundary exclusion, transactions A/B/witness crash windows, generation/epoch contamination, advancing program-health watermarks, equal/older/conflicting slots, retirement-before-buy, byte-budget backpressure and DST calendar boundaries (§§4,6,11).
4. For storage/replay/report changes inject failure before/after durable commit, restart with pending order, corrupt/missing raw evidence, hash/projection mismatch, recorded-vs-audit replay, late offline calendar reconciliation, historical economic-as-of versus cutoff-recorded-at, immutable cutoff and byte-identical regeneration (§§12,14). A test that simply mocks out fsync/commit without observing durable state is insufficient.
5. Run selected focused cases and any repository-required check; retain command, exit status, fixture names, before/after durable state and observed failure code. Compare against pre-change baseline; classify each failed check as pre-existing, introduced, environment-blocked or unresolved. Avoid changing production code or weakening tests to make the suite pass.

Return per-rule PASS/FAIL/BLOCKED/NOT_RUN with baseline/candidate diff identity, independent oracle, actual command/result, durable postcondition and unresolved safety consequence. A subsequent fix invalidates affected receipts; rerun before review. A missing mandatory oracle blocks that gate; do not make a partial suite imply engineering completion. Hand off to `desk-review-gate`.

## Executable integration (v1.1)

Capture counted negative and fault checks as candidate-bound receipts; do not promote empty or skipped tests. Retry only blocked tool execution, never deterministic failing assertions.
