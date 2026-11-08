---
name: desk-friction-intelligence
description: Classify repeated Codex development shell, environment, dependency, or tool-workflow friction for Solana Desk, and propose evidence-linked local remediations. Not for application fault verification, trading data analysis, modifying blueprint decisions, or automatically applying policy changes.
---

# Solana Desk development friction intelligence

**Owns:** bounded, local-only analysis of avoidable agent-development friction. This Skill supplements, not replaces, `desk-fault-verification`, `desk-review-gate`, and the normative blueprint. It grants no shell, network, Git, trading or policy authority.

1. Identify an observed development friction incident: repeated incompatible command syntax, wrong shell, incorrect test invocation, missing environment prerequisite, tool discovery failure or redundant retries. Exclude intentional negative tests, ordinary implementation bugs, campaign/provider payloads, and blocked permissions. Preserve uncertainty.
2. Use `python3 -m tools.friction record` with approved **structured codes only**. Do not pass raw commands, stderr, paths, credentials, market data, campaign datasets, provider responses or sensitive material to the collector. If you cannot classify safely, skip collection and report the gap. CLI usage and categories: `docs/control-plane/friction-intelligence.md`.
3. At an appropriate task boundary, use `python3 -m tools.friction clusters --minimum 2` to detect exact recurring fingerprints. Count records, not proven sessions. Correlate independently with actual local tool results and environment facts when authorized. Do not treat a cluster as causal proof.
4. Reproduce a suspected root cause in a disposable environment, with observed command/exit evidence under existing control-plane verification rules. Distinguish shell/OS differences, WSL2 vs Windows, CLI version drift and expected policy denials.
5. Use `python3 -m tools.friction propose` to register a bounded hypothesis. Prefer environment-preflight checks, corrected scripts, test invocations or contextual Skill recipes over changes to root `AGENTS.md`. An incident cannot authorize host changes or blueprint economic/methodology decisions.
6. Any proposed repository edit goes through the existing task intake, single-writer implementation, review and authorization process. Optionally use `evaluate` to attach **reported** test exit status/digest; such a record is not independent attestation, permission or a promotion gate. No command in this Skill automatically edits policies.
7. Measure comparable before/after tasks and watch for regressions. Retire stale advice only through the ordinary review process. Don't infer improvement from lower raw failure counts without controlling task mix and toolchain version.

Return incident fingerprints, observed vs hypothesized causes, reproducible evidence, proposed target, tests actually executed, unverified checks and unresolved owner decisions. When collection is unavailable, continue the primary task without workaround, network escalation or fabricated evidence.

## Executable integration (v1.1)

For blocked tool invocation only, consider `tools.control_plane.friction_bridge`; use `tools.control_plane.friction_compare` for separate before/after candidate evidence. Neither is permission to change policy.
