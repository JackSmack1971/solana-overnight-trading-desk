# Solana Overnight Trading Desk — Codex development control plane

Project-level control-plane package for implementing **blueprint v2.6**. This is a development harness, **not** the trading application and not proof of runtime policy enforcement. All trading remains paper-only. Start with `docs/control-plane/installation.md`.

Native Codex surfaces: `AGENTS.md`, `.codex/config.toml`, `.codex/agents/*.toml`, `.agents/skills/*/SKILL.md`. Project-specific checks: `python -m tools.control_plane.validate`, `baseline`, `record`, and `gate`. These checks do not replace the Codex sandbox, approval system, OS network policy or CI.

The canonical blueprint is retained verbatim under `docs/blueprint/`. Do not relax its normative gates or infer authorization from this package.

Skill-routing and verification boundary audit: `docs/control-plane/skill-audit-v1.1.md` (static-only; no empirical Codex uplift established).

Local-only, opt-in development friction intelligence: `docs/control-plane/friction-intelligence.md`; run `python3 -m tools.friction --help`. It stores structured incidents outside the repo and cannot automatically approve/promote changes.

## v1.1 orchestration tools

See `docs/control-plane/orchestration-v1.1.md` for commands and strict limitations. Includes candidate-bound execution receipts, fail-closed gate checks, human reviewer statements, a phase DAG/state journal, context extracts, safe retry, concurrency planning, restart snapshots, and a passive hook adapter. It does **not** launch Codex, replace OS isolation or auto-qualify manual host gates. P3 empirical benchmark phase is intentionally excluded from this package update.

Optional CLI task launcher: `python3 -m tools.control_plane.drive` (preview) and `python3 -m tools.control_plane.drive --execute` (requires installed and qualified `codex`). Dispatch never auto-promotes phase or reviewer status.
