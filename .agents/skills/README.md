# Solana Desk Skills — coordinated workflow

Install the seven implementation-workflow skill directories together in the target repository's documented Codex skill discovery location. Keep the authoritative v2.6 blueprint and applicable `AGENTS.md` in the repository; this package does not replace either. No new command, tool or subagent is implied by a skill name.

## Handoff and ownership

`desk-task-intake` (read-only) → `desk-contracts` (rule/schema authority when needed) → `desk-implement-slice` (one bounded code owner) → `desk-reference-parity` (official source/model parity when affected) and/or `desk-fault-verification` (invariant/fault evidence when affected) → `desk-review-gate` (independent review, never author of same patch) → `desk-host-handoff` (read-only host/provider qualification after offline approval). Fault and parity evaluation may be independent peers; neither substitutes for review.

Every handoff identifies actual baseline and candidate diff, blueprint hash, slice ID, applicable rule/OD/acceptance IDs, tested commands/results, evidence IDs, permission gaps, blockers and next owner. Do not invent hashes, IDs or receipts. If any input is absent, verify from the repository or record NOT_RUN/BLOCKED rather than treating an asserted handoff as proof. A candidate edit after verification invalidates affected evidence.

Blueprint §16 gives implementation dependency ordering; §17 gives application acceptance. The distinct labels ENGINEERING_VERIFIED_OFFLINE and PAPER_DESK_VERIFIED require their own observed evidence. Provider permission, source-model parity, WSL readiness, study feasibility and prospective performance are independent gates. No skill grants wallet, signing, live order, paid-service or autonomous host-modification authority.

This archive is a skill bundle, not an application control-plane implementation. Repository tools and paths named inside a skill are conditional on their presence.


`desk-friction-intelligence` is an **eighth, optional development-observation Skill**. It is not in the task implementation/review chain and cannot affect application faults, normative blueprint decisions, permission policy or promotion gates. See `docs/control-plane/friction-intelligence.md`.
