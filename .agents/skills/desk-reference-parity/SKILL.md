---
name: desk-reference-parity
description: Qualify Solana Desk Raydium CPMM decoder, deployment fingerprint, or curve/fee arithmetic using pinned official source and an independent Rust reference harness. Not for general Python code review or treating synthetic fixtures as deployed parity.
---

# Desk reference and parity gate

**Owns:** source-model compatibility evidence; blueprint §§3.2–3.6 and 9.2–9.5. Read applicable scoped `AGENTS.md` if present and affected contracts; missing reference artifacts remain explicit prerequisites, not assumed failures of installed tooling. Provider readiness requires actual evidence, not source-code resemblance.

1. Confirm official Raydium source repository/commit, file and layout hashes, license, program/ProgramData/Clock decoding sources, decoder version and pinned dependency/toolchain provenance in `contracts/program-lock.json` and `reference/fixture-manifest.json` **when present**. Missing values remain unknown; no guessed commit, hash or current deployment claim.
2. Separate three claims: (a) synthetically valid Python arithmetic, (b) tested parity with independent pinned **official Rust** operations, (c) deployed binary/source equivalence. Never infer (c) from (b) or IDL/program address alone; retain `deployment_source_match=UNPROVEN` without verified-build evidence.
3. Run the isolated build-time harness only with an existing authorized toolchain and explicitly recorded source/dependency set. Use independently authored raw integer input/expected-output fixtures for both directions, fee-boundary rounding, accrued shares, u64/u128 source-operation overflow, zero model output, Clock/observation-account constraints and Program/ProgramData fingerprint changes. Apply blueprint §§3.3–3.6, 9.4–9.5 exactly; never infer deployed parity from a passing quote fixture. Do not generate expected values by calling the Python implementation under test.
4. Compare exact results and typed failures, not floating tolerances. Confirm program and ProgramData are coherently captured, bytecode-region hash includes allocated padding and campaign fingerprint/deployment-slot rules are respected; source parity cannot waive health/generation or permission gates. Preserve commands, tool versions, fixture hashes and mismatching cases.
5. If source, isolated Rust toolchain or independent fixtures are absent, distinguish `REFERENCE_BUILD_UNAVAILABLE` from `BLOCKED_PROGRAM_COMPATIBILITY`, keep provider parity blocked and report synthetic checks separately. Permission evidence is a separate `desk-host-handoff` gate. Missing compatible deployment evidence never licenses a guessed decoder, pool layout or alternate quote oracle. Do not install global tools, make an unsafe installer run, enable a wallet or rewrite expected fixtures to pass.

Output pinned source/fixture/toolchain hashes, candidate diff identity, exact compared values/failures, commands, explicit PASS/BLOCKED/NOT_RUN and deployment uncertainty. Hand off receipts to `desk-review-gate`; after any decoder, fixture, source-lock or harness change, invalidate affected parity receipts until rerun. No promotion to `PAPER_DESK_VERIFIED` from parity alone.

## Executable integration (v1.1)

Record counted, executed reference checks against the current candidate with `tools.control_plane.record`; rerun after candidate changes. An empty discovery is not positive parity evidence.
