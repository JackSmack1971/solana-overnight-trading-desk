# Local development friction intelligence (DESIGN)

This subsystem collects **structured, non-sensitive development-tool incidents** outside the repository, analyzes exact recurring fingerprints, and retains remediation hypotheses and reported evaluations. It is not in the Solana trading runtime, never writes `AGENTS.md` or Codex policy automatically, and does not establish trading, provider, network, host or Git authority. Blueprint v2.6 and the seven existing workflow Skills remain normative.

## Storage and constraints

By default, `python3 -m tools.friction` creates a local SQLite DB at `${XDG_STATE_HOME:-~/.local/state}/codex-friction-intelligence/solana-overnight-desk-v2.6/incidents.sqlite3` (user-local, not Git). Python standard library only; SQLite WAL, bounded queries and private directory/file modes on POSIX. No API calls or telemetry export. A custom `--db /absolute/path` is for testing/operator-managed storage and is rejected if inside the packaged repository. SQLite is durable local storage, **not** immutable audit proof. Keep this store on a local Linux filesystem under WSL2, not a shared/network drive. Protect backups and remove data according to local retention policy.

Only typed, bounded fields are accepted: incident category, shell, opaque tool identifier, stable failure/recovery codes, outcome, optional opaque client version/session reference, and optional SHA-256 digest. Never submit raw commands, arguments, paths, prompt text, stderr/stdout, environment dumps, secrets, personal data, RPC payloads, campaign/trade data, or provider responses. An SHA-256 evidence hash does not make excluded underlying evidence safe to retain. Fingerprints hash `category + shell + tool + failure_code`; they do not establish a common root cause.

## Commands

Run from repository root; the following are examples of *synthetic* development friction, not actual recorded incidents:

```sh
python3 -m tools.friction record --category shell-syntax --shell bash --tool git --failure-code unsupportedFlag --outcome recovered --recovery-code correctedFlags
python3 -m tools.friction clusters --minimum 2
python3 -m tools.friction propose --fingerprint <sha256-from-clusters> --target local-script --fix-code preflightGitVersion
python3 -m tools.friction evaluate --proposal-id <uuid-from-propose> --check-code targetedUnitSuite --exit-code 0 --output-sha256 <sha256-of-sanitized-output>
python3 -m tools.friction report
```

`evaluate` records a **self-reported** result; it does not execute tests or independently verify output. Independent validators, the real Git diff, the `desk-review-gate` workflow, and explicit user authority remain required for applying any changes. No `promote`, `approve`, or silent self-edit command exists. To claim a verified root cause, reproduce it with a controlled fixture and separately retain actual check evidence under existing change-management rules.

## Workflow

Observe → classify → correlate (record count, not session proof) → reproduce → propose → independently verify → seek owner approval → edit in authorized scope → test/regression review → monitor. When an incident suggests an economic/methodology/safety change, stop and request a separate blueprint owner decision; the friction workflow never resolves it. Failed or absent collection is nonblocking. Retain a code-specific record of what remains unverified, and never turn a tool denial into a workaround instruction.

## Native integration limitations

The collector is **opt-in** through agent instructions and the Skill. This package does not configure Codex hooks or claim universal tool-result capture because the installed Codex build and its callback schema are unqualified (`control-plane/client-qualification.json`). Native hook and OTel coverage must be tested on a pinned binary before adopting an adapter. No background process, Windows/WSL service, network exporter, daemon or automatic instruction reloading is installed. Any future event adapter must use this same allowlisted schema, explicit source attribution, and measured capture coverage.
