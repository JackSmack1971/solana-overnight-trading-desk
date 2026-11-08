# Installation and qualification

1. Extract into a **new** repository or selectively copy into an existing checkout after reviewing conflicts. This archive does not contain the application implementation.
2. In WSL2 run `git status --short` before modifying any tracked file. Preserve all existing changes. Verify the blueprint SHA-256 equals `9ab2ea573e88009e50a55f7829eb0b6cbf3e38c4826342c807073220f48ae905`.
3. Run `python3 -m tools.control_plane.validate`, `python3 -m unittest discover -s tests/control_plane -v`, and `python3 -m unittest discover -s tests/friction -v` from the repository root. Python 3.12 is the blueprint target.
4. Inspect `codex --version`, `codex --help` and the active effective configuration. Confirm project trust, chosen legacy sandbox family, approval behavior and subagent support on that exact binary. Update `control-plane/client-qualification.json` with *observed* results only.
5. Run authorized negative probes in a disposable environment: denied network, outside-workspace write, approval denial, child inheritance and resumed-thread policy. No probe should target production data or credentials.
6. Start P0/P1 only after recording the actual Git baseline. Application readiness requires independent blueprint acceptance, not package validation.

No model is hard-pinned: resolve available model and reasoning effort per run; fail rather than silently substitute when a task explicitly requires one. Do not assume project config overrides admin-managed requirements.

7. Optional development friction collection: read `docs/control-plane/friction-intelligence.md` and run `python3 -m tools.friction --help`. The database is local-user state outside the checkout. This does not enable automatic event hooks, grant additional Codex permissions, or qualify application runtime behavior.

After intentional package edits, regenerate the digest manifest with `python3 -m tools.control_plane.manifest` and rerun validation. Never regenerate the manifest merely to conceal an unexpected digest mismatch; inspect the differing files first.


8. Read `docs/control-plane/orchestration-v1.1.md`. Inspect `python3 -m tools.control_plane.tasks next` and capture a `handoff` before stopping. Optional hook adapters are not active by default; validate hook compatibility before integration.
