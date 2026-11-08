---
name: desk-host-handoff
description: Prepare and assess operator-controlled Windows/WSL2 qualification of an offline-tested Solana Desk candidate, including permission and provider-readiness evidence. Not for installing tools, modifying host settings, launching campaigns, or promoting synthetic tests to live readiness.
---

# Desk WSL2 host qualification handoff

**Owns:** operator-executable qualification plan and readback; blueprint §§3–4, 15, 17, 20 and `docs/control-plane/installation.md` if present; otherwise use blueprint §15 and report missing runbook guidance without inventing commands. Enter only after the exact candidate has offline acceptance receipts and independent `desk-review-gate` approval; otherwise produce a blocker list. This skill qualifies the host/provider conditions, not the study or prospective strategy.

1. Verify supplied offline gate evidence, immutable blueprint hash, source/dependency locks and open issues. Discover the **installed** Codex version/command help, WSL distro, Python/toolchain and actual effective permissions where authorized. A `.codex/config.toml` value alone is not enforcement evidence; `control-plane/client-qualification.json` initially records UNQUALIFIED.
2. Prepare bounded, operator-controlled read-only host probes: Ubuntu 24.04/WSL2, Linux filesystem, time sync/clock-step behavior, CPU/storage budget, process locks, restart recovery and deterministic filesystem outputs. Never auto-install, change Windows power/scheduler/time services or configure background launches.
3. Distinguish Codex sandbox/approval tests from application permission: negative probes for denied network, outside-workspace write, approval refusal, child-agent inheritance and resumed context must run only in disposable targets with permission. A prompt or skill prohibition is not a host firewall. If access is denied, record denial and stop; no alternate bypass.
4. Provider preflight is separately gated: official usage/retention permission (`PERMITTED` with evidence, not inferred from HTTP 200), allowlisted read-only origins/methods, real endpoint response shape, finalized coherent RPC bundles, deployed ProgramData fingerprints and independent reference parity. Mark `BLOCKED_PROVIDER_TERMS`, `BLOCKED_PROGRAM_COMPATIBILITY` or `INSUFFICIENT_PROVIDER_CAPACITY` exactly when evidenced; an untested condition is NOT_RUN/UNKNOWN, not a fabricated provider failure. Clock synchronization, request permission, source parity and deployment identity are independent requirements. No account key, transaction path, paid service or unauthorized probe.
5. Record operator command, date/environment, actual observation, evidence hash, candidate code/config fingerprint and applicable status; compare against offline acceptance and blueprint §17 completion labels before proposing `PAPER_DESK_VERIFIED`. If the host run changes code, contracts or dependencies, invalidate applicable offline receipts and return to implementation/review. Report what is still NOT_RUN. Do not initiate study, expand the frozen calendar, create capital, modify host configuration or grant readiness because a smoke command exited zero.

Handoff ends with verified facts, requested manual steps and blockers; the operator alone chooses whether to initialize a campaign on its frozen calendar. No smoke test, synthetic fixture, provider response or permission finding satisfies the fourteen-session study gate (§7) or twenty-eight-night prospective observation. `ENGINEERING_VERIFIED_OFFLINE` and `PAPER_DESK_VERIFIED` are different labels; neither implies edge or authorization for live orders.

## Executable integration (v1.1)

Host-qualification remains operator-controlled, and a command receipt does not establish OS isolation. Consult `docs/control-plane/orchestration-v1.1.md` before using evidence.
