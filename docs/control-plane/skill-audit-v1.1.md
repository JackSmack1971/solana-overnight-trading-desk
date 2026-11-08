# Seven-skill surgical audit — control plane v1.1

**Basis:** packaged control plane v1.0; canonical, byte-identical Solana Desk blueprint v2.6; project skill guides and the operational rubric provided with this task. No live Codex CLI invocation, routed activation study, paired no-skill comparison, WSL2 qualification, reference build or provider experiment was performed. This is a **static audit** only.

## Findings and changes

| Skill | Original shortcoming | Targeted correction | Handoff / exclusion |
|---|---|---|---|
| `desk-task-intake` | Generic activation, no durable baseline or gate mapping | Require Git/change ownership, blueprint IDs, a single slice, negative oracles, and an explicit NO_GIT_BASELINE path | Contracts or implementation; never edits |
| `desk-contracts` | No concrete active-rule schema or conflict response | Require explicit authored rule provenance, enum/time/null semantics, independent fixtures and CONTRACT_CONFLICT stop | Implementation after review; never changes blueprint |
| `desk-implement-slice` | Weak prerequisite and pass criteria | Require approved contract, slice limit, focused counterexamples, fault/parity handoff and final diff check | Independent review; never self-approves |
| `desk-reference-parity` | Could mistake source match for deployed equivalence | Separate synthetic/source/deployed proof, require pinned official Rust oracle and fingerprint evidence; typed block if absent | Provider gate only; never claims verified deployment |
| `desk-fault-verification` | No named failure families or durable observations | Cover commit/witness crash windows, exact deadlines, ledger accounting, recorded/audit replay and immutable cutoffs | Independent review; no code changes |
| `desk-review-gate` | Risk of approval from generic receipts or author claims | Validate current diff, relevance and authenticity limits of receipts, named invariants and reproducible findings | Next gate only; no auto-promotion |
| `desk-host-handoff` | No host/provider permission evidence distinction | Require actual local capability/denial probes, operator-only host steps, separate provider terms/parity/compatibility gates | No installation, campaigns or host reconfiguration |

## Cross-cutting resolution

- Preserved **all seven skill names and directory locations**. Descriptions now express *what, when and negative boundary*; no new router, dependency, subagent or arbitrary frontmatter was added.
- Continued referencing the canonical blueprint and scoped `AGENTS.md` instead of copying normative constants into skill definitions. The blueprint bytes and version remain unchanged.
- Kept economic and provider authorization policies in their authoritative files. Textual skills do not enforce permissions or establish Codex host capabilities.
- Added a static routing/stop-contract regression to existing control-plane tests. This confirms text structure, **not** model-trigger behavior.

## Evaluation scope and next required evidence

**G1** routing boundary: statically specified; activation precision/recall untested. **G2** decision value: blueprint-specific consequential decisions included. **G3** completion: explicit evidence requirements, no product evidence yet. **G4** autonomy: stops specified, actual sandbox/denial controls unqualified. **G5** empirical uplift: **UNVALIDATED**.

**Validated Performance: NOT YET TESTED. Classification: UNVALIDATED.** No `/100` score or claim of material uplift is warranted. For a future G5 evaluation, freeze baseline and updated skill packages, test positive/negative/neighbor routing prompts and paired implementation/failure tasks per the Operational Rubric; include a crowded catalog and skill resume after compaction. An installed Codex build and permissions must first be observed, not inferred from the bundled configuration.

**Known blocker:** This ZIP contains the development control plane, not the implemented trading application. Application-level acceptance fixtures, independent official Raydium parity, provider permission and WSL2 field-readiness remain future work, and cannot be declared passed by these static tests.
