# Executable orchestration — v1.1

This is a **local development control plane**, not the trading runtime. Every tool is Python standard-library-only and operates in the current checkout. It does not call Codex automatically, trigger trades, access RPC, enable sandbox overrides, create commits, or mutate the host. A task operator / Codex session must explicitly invoke next steps. Claims of **fully autonomous Codex scheduling**, hook activation, host qualification, or reviewer independence would require integration with a qualified Codex runtime and are **not** implied by this package.

## Startup / recovery

Run from repository root in Python 3.12+:

```bash
python3 -m tools.control_plane.validate
python3 -m tools.control_plane.baseline
python3 -m tools.control_plane.tasks next
python3 -m tools.control_plane.context --task P0-baseline --output artifacts/control-plane/P0-context.json
python3 -m tools.control_plane.handoff --output artifacts/control-plane/handoff.json
```

`tasks.json` is the phase-level DAG. It is deliberately *not* proof that application phase deliverables exist. Before implementing phase content, decompose phase into blueprint-backed, narrowly scoped slices under the project's own workflow; do not claim P1 is done merely because a task has been started. Task state persists in `artifacts/control-plane/tasks-state.json`, excluded from the candidate hash and package manifest. `start`, `block`, `resume`, and `verify` are guarded transitions. `verify` requires a current matching gate verdict; manual P0/P7 instead require `manual-verify` with a matching gate verdict **and** `client-qualification.json` explicitly qualified by the operator with each probe flag true. This is a recorded operator assertion, not an automated proof. No auto-promotion from P0 is possible as shipped.

```bash
python3 -m tools.control_plane.tasks start --task P0-baseline
python3 -m tools.control_plane.tasks block --task P0-baseline --reason "host qualification pending"
python3 -m tools.control_plane.tasks status
python3 -m tools.control_plane.parallel --max 3
```

The parallel planner considers declared write-set overlap and graph eligibility. It never silently spawns subagents, creates worktrees, merges branches or grants them privileges. Actual parallel writers require isolated worktrees, separate exclusive ownership records and a single integration owner. Read-only parallel analysis may be less restricted. No tests have established runtime multi-agent concurrency on the user's Codex installation.

## Candidate-bound receipts and gates

`record` runs *one* explicit command, suppresses raw output, captures an optional conservative unittest/pytest count, and rejects passing assertions when the command changed candidate files. Evidence is stored under ignored `artifacts/control-plane/` only. The candidate digest hashes every non-excluded file, including untracked code, relevant instructions and the canonical blueprint. It is a snapshot integrity check, **not** a digital signature or audit-grade provenance system. A code or policy edit changes the digest, invalidating earlier receipts.

```bash
python3 -m tools.control_plane.record --check validate-package --output artifacts/control-plane/validate.json -- python3 -m tools.control_plane.validate
python3 -m tools.control_plane.record --check unittest-control-plane --output artifacts/control-plane/unit.json --minimum-tests 1 -- python3 -m unittest discover -s tests/control_plane -v
python3 -m tools.control_plane.gate --gate package --receipts artifacts/control-plane/validate.json artifacts/control-plane/unit.json --output artifacts/control-plane/package-verdict.json
```

For application implementation use `focused-tests`, `repo-required-checks`, and `independent-diff-review`, with positive test counts where required by `verification-map.json`. Explicit reviewer assertions may be recorded *only after actual independent review*:

```bash
python3 -m tools.control_plane.review --output artifacts/control-plane/review.json --reviewer-id reviewer-1 --decision APPROVE_FOR_NEXT_GATE --findings-count 0 --review-note "Reviewed candidate diff, contracts and negative tests"
python3 -m tools.control_plane.gate --gate implementation --receipts artifacts/control-plane/focused.json artifacts/control-plane/required.json artifacts/control-plane/review.json --output artifacts/control-plane/implementation-verdict.json
```

The `review` command records a reviewer statement; it does **not** prove independence or inspect the diff automatically. Gate evaluation checks receipt shape, candidate freshness, test-count minimums, source and reviewer assertion, but does not authenticate the runner, check semantic test coverage, attest command isolation or prove the review really occurred. Agent text cannot substitute for artifact evidence. `host-qualified` requires operator qualification separately; a command receipt alone cannot establish safe OS/network isolation. Gate verdicts are not accepted as receipt substitutes for another gate.

## Retry / repair loop

```bash
python3 -m tools.control_plane.retry --check focused-tests --output artifacts/control-plane/retry.json --attempts 2 --minimum-tests 1 -- python3 -m unittest discover -s tests/control_plane
```

Retry is deliberately restricted to local Python unittest / pytest runners, at most three attempts, and **only** blocked execution errors with no candidate mutation. Assertion failures are deterministic until diagnosed; do not blindly re-run and call them resolved. `retry` produces a diagnostic attempts bundle; record a fresh `record` receipt for gate input after it succeeds. Code repair requires a scoped implementation task and re-running all affected checks. No automated LLM patching loop is installed.

## Friction observations and before/after

```bash
python3 -m tools.control_plane.friction_bridge --receipt artifacts/control-plane/blocked.json
python3 -m tools.control_plane.friction_compare --before artifacts/control-plane/before.json --after artifacts/control-plane/after.json --output artifacts/control-plane/comparison.json
```

The bridge classifies only blocked local command execution (not ordinary test failures) and writes allowlisted metadata using the existing external SQLite friction store. The comparison requires separate candidate identities, the same check, and a blocked-to-passed transition; it calls the transition a **hypothesis**, not proof of causality. There is no autonomous modification of `AGENTS.md`, Skills, security config, blueprint or application semantics.

## Hooks and version qualification

`hook_event.py` is a **passive, opt-in adapter** that reads an event payload from standard input and retains only an allowed event label/time. It is **not installed as an active Codex hook**. Hook configuration, event names, trust behavior, and plugin packaging differ by Codex version. Confirm against the actual CLI `codex --version`, current official hook guide and local disposable test before wiring it into an installed plugin. Never assume repository `.codex/config.toml` controls an externally loaded plugin's hooks. Hooks are observations, not non-bypassable approval/network barriers. The adapter intentionally ignores unsupported events and never records tool arguments or outputs.

## Security / deployment boundary

Do not equate YOLO / full access with application authority. Paper-only restrictions remain normative. Use a dedicated WSL2 instance without wallet or host credentials and enforce network controls outside Codex. Runtime CLI configuration must be inspected: this archive deliberately retains conservative `on-request` / `workspace-write` defaults and does not silently change its security posture to match a user's local YOLO invocation. No host/network negative probes were run in this artifact-generation environment.

For manually qualified P0 after independent probes and package-verdict generation, record the observed client version and host conditions in `control-plane/client-qualification.json` (including `status: "QUALIFIED"` and three verification flags set true), **rerun the package checks after that edit**, and then run:

```bash
python3 -m tools.control_plane.tasks manual-verify --task P0-baseline --gate-verdict artifacts/control-plane/package-verdict.json
```

At P7 the operator must additionally record independent WSL2/network denial probes and an operator-host-review assertion using `tools.control_plane.review --kind operator-host ...`, then evaluate the `host-qualified` gate before `manual-verify`. Never mark the host qualified based solely on this tool's output.

## Opt-in CLI task dispatch

After the operator actually qualifies P0, the handoff tool can generate a task prompt or invoke one installed Codex CLI agent process:

```bash
python3 -m tools.control_plane.drive                    # preview next task and exact prompt
python3 -m tools.control_plane.drive --execute          # invokes `codex exec <task prompt>` using current effective local permissions
```

This driver preserves exclusive writer ownership at task granularity: it refuses to launch while any task is `in_progress`, and never calls `--dangerously-bypass-approvals-and-sandbox` or silently changes permissions. It records the task state before launch. It does **not** automatically verify or promote the task after Codex exits, because independent review and executed receipts must be checked first. For phase-wide tasks, the agent is instructed to implement one coherent contract-backed slice, not claim phase completion. A failed or interrupted agent leaves state `in_progress` for inspection and recovery. Run `tasks block` / `tasks resume` explicitly before retrying. The exact Codex `exec` syntax and runtime capabilities require qualification on the target host. No Codex executable was available in the packaging environment.
