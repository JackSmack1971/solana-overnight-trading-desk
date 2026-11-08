# Failure and recovery

On interrupted work, stop overlapping writers and inspect Git status, staged/unstaged diff, worktrees, incomplete receipts and external side effects before retry. Do not blindly replay non-idempotent actions. Never reset or clean user changes. Treat missing receipts as NOT_RUN or BLOCKED, never PASSED. A review bound to a prior diff must be repeated if that diff changes. Record decisions, actor, baseline and verification outcomes without secrets.


For durable local handoff, run `python3 -m tools.control_plane.handoff --output artifacts/control-plane/handoff.json`, then inspect live Git status and task state on resumption. Handoff includes only Git counts, not a claimed clean tree. A new candidate digest invalidates earlier gate evidence.
