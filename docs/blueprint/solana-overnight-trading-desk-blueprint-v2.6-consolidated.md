# Solana Overnight Trading Desk — Consolidated Implementation Blueprint v2.6

**Decision date:** 2026-11-06. **Mode:** paper-only. **Host:** Windows with WSL2. **Status:** specification only; application implementation and field validation have not been performed.

This document replaces the supplied v2.5 blueprint in full. All core requirements and amendments have been integrated by subject. Read from the purpose and decision register into the relevant topical contracts; no historical amendment hierarchy applies. Existing decisions are retained, not reopened or newly approved by this consolidation.

**Evidence notation:** [R#] identifies an inherited source in §21. [D] identifies delegated engineering/experimental choices. Unless expressly attributed to a source, numerical thresholds, schedules, limits and cost scenarios are [D]. This consolidation performs no fresh research or market observation. Source retrieval statements in §21 describe prior revisions and retain their original limitations.

## Contents

- [1. Purpose, boundaries and implementation authority](#1-purpose-boundaries-and-implementation-authority)
- [2. Complete decision register](#2-complete-decision-register)
- [3. Market scope and canonical identity](#3-market-scope-and-canonical-identity)
- [4. Provider and collection contract](#4-provider-and-collection-contract)
- [5. Required eligibility and security boundary](#5-required-eligibility-and-security-boundary)
- [6. Time, data quality and event ordering](#6-time-data-quality-and-event-ordering)
- [7. Study gate and preregistration](#7-study-gate-and-preregistration)
- [8. Signals, controls and selection](#8-signals-controls-and-selection)
- [9. Counterfactual execution contract](#9-counterfactual-execution-contract)
- [10. Capital, risk and accounting](#10-capital-risk-and-accounting)
- [11. Position exits and session lifecycle](#11-position-exits-and-session-lifecycle)
- [12. Storage, schema, idempotency and crash recovery](#12-storage-schema-idempotency-and-crash-recovery)
- [13. Interfaces, configuration and repository deliverables](#13-interfaces-configuration-and-repository-deliverables)
- [14. Reports and statistical interpretation](#14-reports-and-statistical-interpretation)
- [15. WSL operations and resource budget](#15-wsl-operations-and-resource-budget)
- [16. Implementation sequence and phase outputs](#16-implementation-sequence-and-phase-outputs)
- [17. Acceptance tests and exact completion labels](#17-acceptance-tests-and-exact-completion-labels)
- [18. Hand-calculated acceptance fixtures](#18-hand-calculated-acceptance-fixtures)
- [19. Change control and unresolved-event policy](#19-change-control-and-unresolved-event-policy)
- [20. Verification scope and implementation handoff](#20-verification-scope-and-implementation-handoff)
- [21. Consolidated research register and evidence limits](#21-consolidated-research-register-and-evidence-limits)
- [22. Requirement traceability and change records](#22-requirement-traceability-and-change-records)

## 1. Purpose, boundaries and implementation authority

This is the single normative blueprint for the bounded Solana Overnight Trading Desk v1. It consolidates the supplied v2.5 core and every amendment into topic sections. There is no amendment precedence chain and no separate operating addendum. Historical decision and acceptance IDs are retained for traceability; their version prefixes are identifiers, not alternative specifications.

Build a complete prospective paper-research system for a sampled cohort of classic SPL tokens in supported direct Raydium CPMM/native-USDC pools. The system must run without an AI agent, preserve every financial transition, reproduce historical reports, and report unavailable evidence honestly. It is not a comprehensive launch scanner or a safety-certified token selector. Unsupported holder, developer, bundle and LP-lock assessments remain NOT_ASSESSED.

The scope is paper-only: no wallets, signing, transaction building/submission, live trading, paid services, external publication, or automatic host configuration changes. A profitable strategy is not a completion criterion. External access, deployed compatibility, host readiness, sample sufficiency and profitability are verification obligations; their failure paths are explicit.

Numerical thresholds are preregistered design choices [D], not academically optimal or expert-validated trading parameters. The restricted cohort and strict evidence gates may yield no provider experiment. Complete the offline pipeline and retain the blocked outcome rather than expanding scope.

Internal code organization, schema column spelling and compatible dependency patch selection are implementation choices. Economic, experimental, compatibility and failure semantics are fixed. A new fact outside these contracts produces its typed block or a documented change request; it does not authorize an improvised trading rule.

## 2. Complete decision register

Implement `DECISIONS.md` and `config/decisions.json` from the complete OD-001–OD-049 table below. Each record contains ID, exact choice, status, decision date, rationale, affected contract sections, and approval provenance `current_user_delegation_2026-11-06`. Preserve previous decisions as superseded history, not active gates.

| ID | Binding choice | Status |
|---|---|---|
| OD-001 | Windows/WSL2; Ubuntu 24.04 LTS; Python 3.12; Linux filesystem | Prior host choice retained; details delegated |
| OD-002 | Restricted direct CPMM/USDC scope in §3 | DELEGATED_DESIGN_APPROVED |
| OD-003 | H2 fixed before study; enable only by §7 feasibility gate; H0 otherwise | DELEGATED_DESIGN_APPROVED |
| OD-004 | Stop entries 15 minutes before session end, attempt exits through end+15 minutes, persist unfilled exposure | DELEGATED_DESIGN_APPROVED |
| OD-005 | Complete engineering paper system plus separately labeled prospective evidence | Prior goal retained |
| OD-006 | Classic SPL target only; exact mainnet program/mints; source/deployment compatibility gate | DELEGATED_DESIGN_APPROVED |
| OD-007 | DEX Screener discovery; Solana public RPC for limited prototype; zero paid-provider budget | DELEGATED_DESIGN_APPROVED |
| OD-008 | Finalized batched chain state; freshness, monotonic slot, and latency limits in §6 | DELEGATED_DESIGN_APPROVED |
| OD-009 | No wallet attribution, bundle, holder-distribution or LP-lock claims in v1 | EXCLUDED_V1 |
| OD-010 | 10,000 USDC initial virtual capital, 100 USDC order cap, three positions, explicit costs | DELEGATED_DESIGN_APPROVED |
| OD-011 | 14 study sessions + 28 prospective sessions; no optimization or automatic edge claim | DELEGATED_DESIGN_APPROVED |
| OD-012 | Manual foreground launches, persisted recovery; no automatic Windows power/scheduler modification | DELEGATED_DESIGN_APPROVED |
| OD-013 | SQLite WAL/FULL, one writer, canonical snapshots | DELEGATED_DESIGN_APPROVED |
| OD-014 | Same as OD-004; no independent policy | RESOLVED_BY_OD004 |
| OD-015 | §6.2: UTC grid, actual-time deadline barrier, no future boundary evidence | DELEGATED_DESIGN_APPROVED |
| OD-016 | §4.5: separate tasks, serialized writer, nonblocking collection/export | DELEGATED_DESIGN_APPROVED |
| OD-017 | §9.4: fixed cohort diagnostic plus immutable proposal-size checks | DELEGATED_DESIGN_APPROVED |
| OD-018 | §10.1: projected post-fill gate and immediate mark/trigger evaluation | DELEGATED_DESIGN_APPROVED |
| OD-019 | §4.6: one watch lifetime, FIFO admission, durable terminal retirement | DELEGATED_DESIGN_APPROVED |
| OD-020 | §11.3: distinct advancing snapshots and explicit reset rules | DELEGATED_DESIGN_APPROVED |
| OD-021 | §11.4: phase-specific snapshots and terminal recovery policy | DELEGATED_DESIGN_APPROVED |
| OD-022 | §13.1: executable schema phase with invariant-based acceptance | DELEGATED_DESIGN_APPROVED |
| OD-023 | §14.2: writer-owned cutoff, external deterministic exporter | DELEGATED_DESIGN_APPROVED |
| OD-024 | §4.7: documented permission evidence, no inference from API reachability | DELEGATED_DESIGN_APPROVED |
| OD-025 | §21.1: current source evidence and retrieval limitations | DELEGATED_DESIGN_APPROVED |
| OD-026 | §17.2: specific regression oracles and delivery checks | DELEGATED_DESIGN_APPROVED |
| OD-027 | §6.3: separate receipt and availability events; monotone acceptance watermark | DELEGATED_DESIGN_APPROVED |
| OD-028 | §4.8: deadline-aware dispatch, explicit per-pool batch outcomes | DELEGATED_DESIGN_APPROVED |
| OD-029 | §3.3: coherent Clock sysvar and observation-account validation | DELEGATED_DESIGN_APPROVED |
| OD-030 | §3.4: permanent model block; no version transfer or fabricated close | DELEGATED_DESIGN_APPROVED |
| OD-031 | §12.2: one versioned byte encoder and strict decoder | DELEGATED_DESIGN_APPROVED |
| OD-032 | §10.2: defined precision, integer risk tests and rational statistical means | DELEGATED_DESIGN_APPROVED |
| OD-033 | §9.5: typed quote outcomes and source-operation range checks | DELEGATED_DESIGN_APPROVED |
| OD-034 | §11.5: exact command/phase matrix and evidence-only embargo | DELEGATED_DESIGN_APPROVED |
| OD-035 | §12.3: local registry and explicit recovery from snapshot cutoff | DELEGATED_DESIGN_APPROVED |
| OD-036 | §17.3: behavior-based regression tests and staged handoff | DELEGATED_DESIGN_APPROVED |
| OD-037 | Finite availability protocol and explicit crash treatment (§6.4) | DELEGATED_DESIGN_APPROVED |
| OD-038 | Event-derived cutoff projections; ordinary SQLite isolation alone is insufficient (§14.3) | DELEGATED_DESIGN_APPROVED |
| OD-039 | Coherent Program/ProgramData capture and explicit fingerprints (§3.5) | DELEGATED_DESIGN_APPROVED |
| OD-040 | Resume only the original prospective liquidation window (§11.6) | DELEGATED_DESIGN_APPROVED |
| OD-041 | Portfolio marks and risk refreshed in fixed event order (§10.3) | DELEGATED_DESIGN_APPROVED |
| OD-042 | No economic continuation after failed persistence (§12.4) | DELEGATED_DESIGN_APPROVED |
| OD-043 | Frozen inferential scope and independent regression oracles (§17.4) | DELEGATED_DESIGN_APPROVED |
| OD-044 | §15.1: byte admission and nonblocking dispatcher | DELEGATED_DESIGN_APPROVED |
| OD-045 | §6.5: health watermarks and runtime generations | DELEGATED_DESIGN_APPROVED |
| OD-046 | §4.9: retirement cancels buys; positions stay pinned for exits | DELEGATED_DESIGN_APPROVED |
| OD-047 | §12.5: recorded historical predicates and distinct replay modes | DELEGATED_DESIGN_APPROVED |
| OD-048 | §11.7: explicit offline calendar reconciliation | DELEGATED_DESIGN_APPROVED |
| OD-049 | §3.6: isolated build-time reference harness | DELEGATED_DESIGN_APPROVED |

An agent may make reversible code-organization choices that preserve these contracts. It must not change thresholds, supported scope, experimental design, or failure handling to get a passing run. Unexpected requirements outside this scope become a documented change request; implement the specified fail-closed outcome and continue independent work. No phase requires asking again about choices resolved here.

OD-015–OD-049 retain decision date 2026-11-06 and provenance `current_user_delegation_2026-11-06`. OD-025 and OD-026 record evidence-register and acceptance obligations; they do not grant access or report tests as passed.

## 3. Market scope and canonical identity



### 3.1 Fixed supported identifiers

| Item | Value |
|---|---|
| Chain | Solana mainnet-beta |
| Target token program | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` |
| Pool program | `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C` [R1] |
| Quote mint | Native USDC `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` [R7] |
| Route | Exactly one supported pool, target↔USDC; no aggregator or intermediate SOL leg |
| Trade direction | Long target with USDC, then sell entire target position; no shorting/leverage |
| Pool fee support | Creator fee disabled and creator-fee rate zero; trade-fee rate decoded dynamically |

USDC is the accounting numeraire, not an assertion of USD parity. Reports use “USDC,” not dollar signs. Quote-mint issuer authorities are explicitly allowed; target-mint revoked-authority requirements do not apply to USDC. Both vaults must nevertheless be initialized and unfrozen.

Exclude Token-2022, transfer extensions, bonding curves, AMM v4, CLMM, order books, bridged USDC, routed swaps, pools without native USDC, and pools with enabled/nonzero creator fees. Exclusion is `UNSUPPORTED`, not a claim that the asset is malicious. The current CPMM implementation includes creator-fee behavior, so a historical fixed-fee assumption is unsafe [R2].

Identity: `pool_id = solana:mainnet-beta:<program>:<pool_address>`. Asset ID is chain+token program+mint, never symbol. Store mint0/mint1 and direction explicitly; provider base/quote orientation does not change on-chain order. Validate base58 decoded length is 32 bytes. At watch admission, consider at most eight provider-listed pools for a target, sorted by decoded pool address; retain excluded addresses as POOL_ADMISSION_CAP. Validate those bundles and select the largest fresh supported USDC curve reserve, tie by raw address bytes ascending. If none is valid, defer admission to the next minute. Pin that selected pool throughout the mint's watch lifetime; no performance-based switching. Once entered, the position remains tied to that pool even after watch retirement; never reroute to manufacture an exit.

### 3.2 Source and deployment compatibility

Before real-data simulation, implementation must:

1. Retrieve Raydium's official source, pin a concrete commit, and record source files, IDL/layout hashes, license, decoder version, and curve implementation in `contracts/program-lock.json`.
2. Decode current finalized pool, configuration, program and ProgramData accounts using that layout. Record deployed executable hash and deployment slot. Decode account discriminators, exact lengths, reserved bytes according to the pinned layout, owner program and referenced addresses. Never copy offsets from a blog or guess from a ticker.
3. Establish support using raw-account golden fixtures and independent curve results from the pinned official implementation. Preserve source commit in each fixture. This is a build task, not an unspecified product choice. No fabricated commit/hash is permitted.
4. Pin the observed deployment hash for each campaign. Recheck at startup and every five minutes. A change stops entries, rejects pending entries, and marks affected positions `OPEN_EXIT_BLOCKED/PROGRAM_CHANGED` permanently for that campaign, including exits. A replacement decoder cannot resume it. Keep legacy exposure and evidence; only a new separately funded campaign may use a new validated lock.

A matching IDL or program address alone does not prove the deployed binary matches source. Record `deployment_source_match=UNPROVEN` unless verified-build evidence establishes it. v1 results are explicitly source-model counterfactuals; never describe them as verified on-chain execution. If layouts, account semantics or curve fixtures cannot be validated, real-data simulation is `BLOCKED_PROGRAM_COMPATIBILITY`; offline synthetic implementation remains possible.

### 3.3 Coherent Clock and observation-account constraints

Include Clock sysvar `SysvarC1ock11111111111111111111111111111111` and the pool's observation account to each coherent bundle; deduplicate shared Clock within a batch. These are public read-only account requests using existing allowlisted methods. The 90-account cap is unchanged; account count must include these additions. Bootstrap may discover observation_key, but the full bundle must recheck that reference.

Decode Clock and verify its owner/layout using the pinned official Solana sysvar definitions; unsupported layouts block compatibility. Require its slot equal response context slot; otherwise CHAIN_CLOCK_INCOHERENT, no quote/fill. Pool opening uses the captured chain Clock unix_timestamp against pool open_time, with equality allowed. Host UTC continues to govern local scheduling/freshness, never pool opening. getBlockTime remains the independent coarse finalized-age gate; it is not a substitute for the instruction's chain clock. The instruction reads Clock and checks swap status/open_time [R28].

Verify observation account owner, discriminator/layout and pool linkage against the pinned implementation, including every non-user-account constraint required by the modeled swap instruction. Vault PDA, config and mint checks remain required. Record unsupported/missing observation state as execution-mechanics failure, not optional metadata. Do not add payer, wallet, transaction building or signer accounts: this remains a source-model quote, not full instruction execution.

Implement an adapter constraint manifest listing each source account constraint, its validated bundle field, entry/exit applicability and fixture. Any required non-user constraint without a model mapping yields BLOCKED_PROGRAM_COMPATIBILITY. Pin the official Clock layout source alongside the program source before provider mode. This revision does not assert a captured Clock fixture already exists.

### 3.4 Permanent deployment-change treatment

PROGRAM_CHANGED is permanent for that campaign under §6.1 and 23.7. Cancel all its pending orders, retain every charged fee, mark existing exposure OPEN_EXIT_BLOCKED/PROGRAM_CHANGED, and preserve quantities. No new modeled fills, including sells, are allowed under a replacement decoder in that campaign. Recover-only may capture diagnostics and report the block; it cannot bypass the lock. A new campaign may use a new validated lock with separate virtual funding; it receives no inventory, history rewrite or inferred legacy exit. Report legacy exposure alongside later campaigns so a new campaign cannot hide it.

Health staleness without an observed change remains transient and may recover under existing rules. Document this distinction in the CLI error. Frozen legacy inventory is a deliberate limit of the narrow model. Changing that limit requires a future explicit specification with independently audited bridge semantics; it is not an unresolved choice for this implementation.

### 3.5 Deployment fingerprints and coherent upgrade checks

Official Solana documentation distinguishes the executable Program account from the separate loader-v3 ProgramData containing code; an upgrade need not change the Program pointer [R33,R34]. Checking only the program address, executable flag or pointer is insufficient.

For this v1 adapter, support loader-v3 only. Pin official loader state decoding and owner identity alongside Clock/CPMM sources. At bootstrap, resolve ProgramData; then fetch Program and that ProgramData together in one finalized getMultipleAccounts response. Recheck the pointer in that response. A changed pointer during assembly invalidates the check and retries through the normal scheduler; it is not a healthy result. Missing, unknown loader or undecodable state gives BLOCKED_PROGRAM_COMPATIBILITY.

Record independently: program address/owner/executable flag, ProgramData address/owner, deployment slot, optional upgrade authority, complete raw account-data hashes, and SHA-256 of the complete ProgramData bytecode region following the pinned loader metadata layout **including allocated trailing padding**. No guessed ELF trimming. These are observation fingerprints, not a reproducible-build proof. `deployment_source_match` remains UNPROVEN absent the existing verified-build gate.

Campaign compatibility fingerprint includes loader identity, program address, ProgramData pointer, deployment slot and bytecode-region hash. Any difference from the pinned fingerprint gives permanent PROGRAM_CHANGED, even if a redeployment uses identical code bytes. Authority-only change is PROGRAM_AUTHORITY_CHANGED: retain evidence, block submissions pending a fresh coherent fingerprint check; if the fingerprint matches, resume transient health under the existing recovery rules. Do not equate an authority change with proven code change. Raw account hashes can change for metadata reasons without a bytecode difference; report the distinction.

Every check archives raw evidence, request/context slot and acknowledgment. A malformed/failed check is health UNKNOWN/STALE, never proof of upgrade. Periodic checks cannot prove no upgrade occurred between observations or that historical modeled fills match the deployed code at every instant. Retain this sampling limitation in reports. The source-model nature of all fills remains unchanged.

### 3.6 Independent build-time reference harness

The runtime remains Python-only with the declared Python dependencies. Source validation needs a separate **build-time** reference harness for the exact official Raydium source commit; it is not the Python quote function translated line-for-line and called an independent oracle.

Create `reference/README.md`, pinned harness source and `reference/fixture-manifest.json`. Invoke the pinned official Rust calculator/fee operations directly in an isolated temporary build workspace or an already available compatible toolchain. Record repository URL, commit, source/license hashes, Rust/Cargo versions, exact invocation, harness hash, dependency lock hashes, input/output fixture hashes and build outcome. Reference test inputs are independently authored, including both directions, fee-boundary rounding, protocol/fund allocations and source-operation overflow. Preserve raw integer outputs and expected failure variants. Build output and Cargo downloads are development artifacts, excluded from the application runtime and campaign source hashes except their declared provenance manifests.

Do not install a global toolchain, run an unpinned remote installer or silently alter the user's host. If a usable isolated/preexisting build environment is unavailable, produce REFERENCE_BUILD_UNAVAILABLE and block only source-parity/provider readiness. Synthetic Python engineering can still be verified against independently authored arithmetic examples, explicitly labeled SYNTHETIC_ONLY. If official source cannot be compiled with a compatible recorded dependency set, record the concrete build error; do not substitute a guessed commit, SDK quote or copied Python result. A reference match proves source-model parity for tested cases, not deployed-binary equivalence or transaction inclusion.

The exact compiler/dependency versions are discovered, tested and pinned during implementation; they are not policy choices for the owner and must not be fabricated in this document. License compatibility review and restrictions remain recorded build gates, never implied permission to redistribute arbitrary dependencies.

## 4. Provider and collection contract



### 4.1 Provider choices and budget

Use `https://api.dexscreener.com` for public discovery/metadata and `https://api.mainnet.solana.com` for read-only JSON-RPC. No paid account, API key, historical-data purchase, Jupiter API, or wallet is required. Public RPC is a prototype dependency without an availability guarantee; Solana explicitly discourages it for production [R3]. The system must expose `INSUFFICIENT_PROVIDER_CAPACITY` rather than silently buy access or widen staleness limits.

Read-only JSON-RPC POST is permitted. Allowlist only `getMultipleAccounts`, `getAccountInfo`, `getSlot`, `getBlockTime`, `getGenesisHash`, and `getVersion`. Reject all other methods locally, including transaction submission. Only these fixed HTTPS origins are allowed; disable redirects. Provider metadata links are never fetched. Do not execute text from payloads. Redact request headers and endpoint credentials from logs.

Before collection, archive URLs/date for public API terms and retention restrictions in `provider-contract.json`; record whether local research retention is permitted, using the explicit evidence states in §4.7. If permissions are explicitly incompatible or cannot be determined, return `BLOCKED_PROVIDER_TERMS`, retain only allowed diagnostics, and run synthetic mode. This is an evidence gate, not a license assumption.

### 4.2 Discovery algorithm

Every 60 seconds GET `/token-profiles/latest/v1`, retain entries with `chainId == solana`, and deduplicate by mint. Latest profiles are a sampled listing, not an exhaustive launch feed [R4]. Do not use boosts or advertisements as evidence of token quality.

For previously unseen mints, request `/token-pairs/v1/solana/{mint}`. Queue by first-received UTC timestamp, then decoded mint bytes. Maximum 20 pair lookups/minute, queue capacity 1,000. Overflow retains the oldest requests and writes `DISCOVERY_QUEUE_OVERFLOW` counts and omitted mint IDs. Retry failed lookups on the next minute, maximum three attempts, then retain `LOOKUP_FAILED`. Rediscovery after one hour may create a new lookup attempt, never a new mint identity.

Persist every returned pool and exclusion reason. Admit at most eight target mints for active observation, in first-seen order. Among each mint's pools choose by §3 after chain verification. If full, use a FIFO waiting list. No eviction because of poor returns. Retire a watched mint after 48 hours since first seen, or 60 consecutive minutes without any valid supported pool; retain its history. Positions and pending orders pin their pool until closed, even after retirement; up to 18 additional distinct pinned pools are supported across the six portfolios (three per portfolio); deduplicate shared pool addresses. Emit `CAPACITY_EXCLUDED` for each waiting mint-minute. No backfilled first-seen time or fictional historical coverage.

Pair metadata is refreshed for watched mints every five minutes. Profile discovery and metadata only identify addresses/context; they do not supply fills, signal prices, or mandatory liquidity/volume/market-cap gates. This avoids treating cached metadata as a synchronized market state. Raw `pairCreatedAt`, volume and market cap remain optional descriptive fields with provider definitions; no FDV substitution for missing market cap.

### 4.3 Polling, quotas and transport

Poll the selected pool bundles every five seconds. First fetch pool references, then include pool, both vaults, both mints, AmmConfig, Clock sysvar and pool observation account in one coherent `getMultipleAccounts` response per bundle. Multiple complete bundles may share one request, with at most 90 distinct accounts; never split a bundle across requests. Revalidate references inside the returned pool; if changed, discard that bundle and fetch a newly assembled one. RPC supports at most 100 accounts per request [R5].

Use one in-flight RPC request at a time; client token bucket capacity 1, refill one request/second. Additional getSlot/getBlockTime/program checks consume the same bucket. Reserve priority for pinned open positions, then pending orders, then watched pool data, then discovery validation. Rotate within each priority by oldest last-polled time and pool bytes. DEX requests have a separate bucket at one request/second, burst 1. These conservative client caps are below the currently documented DEX endpoint ceilings [R4]; provider throttling can still occur.

HTTP connect timeout 3 seconds; total request timeout 10 seconds; response-size limit 10 MiB. On 429 respect Retry-After; if absent use 30 seconds. For timeout/5xx retry at 1, 2, then 4 seconds, no random jitter, respecting buckets; afterward resume normal cadence. For 400/401/403/schema error, no immediate retry; disable that adapter until a five-minute health probe succeeds. Do not hide gaps by making replacement observations. Record intended poll time, request start, response receipt, status, attempt number and bytes. `Retry-After` beyond a session is allowed and yields missing coverage.

### 4.4 Adapter contract and validation availability

RPC uses base64 full account data, explicit finalized commitment and exact JSON-RPC request/response ID matching. Null accounts, wrong owner, missing keys and malformed base64 produce typed errors, never empty reserve values. Reject duplicate JSON object keys and nonfinite numbers. Parse provider decimal values from their original text, not binary float. Ignore additive unknown metadata fields but retain raw evidence; missing required identity fields invalidate that item. A malformed item does not invalidate independently parseable sibling items; retain indexed error records.

DEX profile endpoint documentation currently describes an object schema while discovery expects a list [R20]. Before provider-backed collection, capture an actual public response, record its shape/hash and lock a tested adapter contract. Accept either a list of profile objects or one profile object normalized to a singleton list; no recursive search for token addresses. An unexpected envelope disables that endpoint with SCHEMA_DRIFT. Pair lookup must be a list; validate chain and that the requested mint is one of each pair's two mints; do not trust dexId as on-chain program identification. Ignore malformed addresses with explicit item-level reasons. Terms evidence may be fetched manually during build; runtime origin allowlisting remains unchanged.

Every RPC result and subsequent block-time response is a separate raw observation. Snapshot decision availability requires the finite two-transaction/witness protocol in §6.4 after parsing and block-time validation. `available_at` means its witnessed `usable_at`; `available_seq` identifies its durable availability ordering. Receipt freshness still applies. A late validation must never make an earlier bar valid retrospectively. Null block times are retried at most once on the next poll using the same global bucket; if validation cannot finish before receipt expiry, retain the bundle as invalid for decisions. Batch bundles sharing a context slot share one block-time lookup. There is no unlimited validation backlog.

### 4.5 Concurrent collection and bounded validation

One process contains a scheduler task, network adapter tasks and a single writer. No writer transaction or scheduler callback awaits network, sleeps for provider backoff, invokes blocking subprocess.run, or performs report rendering. Use httpx asynchronous transport, asyncio subprocess APIs for clock probes, and retained task references; Python's task documentation supports concurrent I/O but does not supply application ordering guarantees [R23]. Perform compression/hash preparation outside the economic transition; only durable commit establishes availability. Bound preparation queues under §15. Short synchronous SQLite commits remain serialized; measure writer lag and apply §6.2 when storage stalls. Do not claim a hard realtime guarantee.

The single RPC in-flight rule includes block-time and program requests. Each bundle result creates a bounded pending-validation item; share/cache block-time results by context slot. Poll batches contain complete bundles in priority order, deduplicate account addresses, and greedily stop before the 90-account limit. Repeatedly take the next batch while the bucket permits; overdue ticks are failures, not a license to exceed quotas. Bootstrap reference fetches do not count as complete poll opportunities. Retries re-enter the common scheduler; they never sleep while holding writer ownership. Capture request IDs before dispatch, monotonically increasing per campaign, so timeout/drop diagnostics remain attributable.

HTTP total timeout includes streamed body reading. Enforce the size cap on decompressed bytes as well as wire bytes, terminate oversize streams, retain a bounded diagnostic, and never parse truncated JSON as a valid observation. Retry-After supports nonnegative delay seconds and HTTP-date; for an invalid header use 30 seconds, and for a past HTTP-date use zero before applying the shared bucket. Provider-level backoff applies to all calls to that origin. A transport failure does not create an empty pool snapshot. RPC JSON error responses are typed failed observations even when HTTP status is 200. No queue eviction may remove committed financial work.

### 4.6 Candidate lifecycle and permanent retirement

Persist states DISCOVERED, LOOKUP_PENDING, WAITING, WATCHED, RETIRED, LOOKUP_FAILED with reason and transition events. first_seen is immutable campaign evidence time. Each mint has at most one watch lifetime per campaign. A RETIRED mint cannot re-enter through rediscovery. The one-hour retry rule applies to unresolved/failed lookup before retirement only; it does not reset first_seen, retirement age, FIFO rank or prior exclusions. A mint not admitted before first_seen + 48 hours retires from waiting at that boundary. This prevents an old waiting queue from creating arbitrary fresh observation lifetimes.

At each running minute boundary apply due retirements, then admissions in FIFO order. Candidates discovered at that same boundary join only after their evidence is durable. The sixty-minute missing-supported-state retirement uses fresh supported snapshots for the pinned pool, not provider listing presence; no snapshot at a minute boundary increments the streak. Restart does not infer an unobserved streak. Pool pinning does not change on metadata refresh. Retired pools with open positions continue exit-only polling and do not create entry bars/signals or watched-minute denominators. Their pinned-poll denominator continues while the process is scheduled to monitor. A watch-pinned overlap counts once for a pool-poll denominator, never twice.

### 4.7 Provider permission evidence

provider-contract.json contains per-origin terms URLs, retrieval UTC time, terms content hash/copy where permitted, intended local collection/retention, restrictions and evidence state PERMITTED, INCOMPATIBLE or UNDETERMINED. PERMITTED requires explicit applicable official permission/license for the intended use or documented provider permission; absence of an express prohibition alone is not sufficient. INCOMPATIBLE and UNDETERMINED produce BLOCKED_PROVIDER_TERMS. Do not invent legal certainty or treat an HTTP 200 as permission. This is a strict evidence gate; if the official free APIs do not establish it, the correct deliverable is offline verification plus the specific blocked dependency. Changing that standard is outside agent discretion.

This revision does not establish permission, capacity or a live response contract. The developer may complete documentation review during implementation without paid services or contacting third parties. Any paid/access/permission exception remains an explicitly scoped future change. This is a concrete failure path, not an unresolved policy question.

### 4.8 RPC dispatch priority and opportunity outcomes

Before every request dispatch: honor origin backoff, token bucket and single in-flight request; then dispatch overdue/startup program-health requests, then pending block-time validation by earliest receipt-expiry deadline, then pool work in §4.3 priority order, then bootstrap/discovery. Runtime clock probes use their own nonnetwork task and do not consume RPC quota. A program check becoming due must not wait indefinitely behind recurring high-priority position polls. A running request is not preempted; timeout still applies. Any resulting missed pool deadline counts as missing. These priorities are deterministic and preserve quota; they do not promise feasible public-provider capacity.

Greedy batches retain the priority/oldest-poll/raw-address ordering in §4.5. Every pool in a batch gets a separate intended-opportunity ID and outcome. Entire-response errors fail all members. A null/malformed account fails only bundles that depend on it; valid independent bundles may continue. An invalid common context/ID/envelope fails the whole response. Shared account validation errors propagate to every dependent bundle. Never average coverage over requests in place of pool opportunities.

Within an opportunity, dispatch at most one initial bundle request for that pool; retries retain that opportunity ID. A failed opportunity cannot be repaired by a subsequent opportunity's success. Each pool has at most one outstanding bundle request and one pending-validation bundle. If validation is still pending at its next opportunity, record VALIDATION_BACKLOG and skip that pool for that opportunity. Expire pending validation once original receipt freshness expires. When returning to the scheduler, do not submit a backlog of historical polls. This fixes queue growth without relaxing coverage/freshness gates.

### 4.9 Retirement ordering, orders and pinned exposure

At the effective retirement time, the mint stops being entry-eligible in every portfolio. Before any possible buy fill at that time, cancel its submitted buys with WATCH_RETIRED, retain their already-debited fees and release reservations/slots. Locally unsubmitted proposals reject without fees. A fill requires active watch membership at actual fill processing time in addition to all inherited gates. A delayed retirement reconciliation cannot authorize a fill after the already known scheduled 48-hour expiry.

Retirement based on 60 invalid running minute opportunities becomes effective at the minute that completes that streak. Process it with lifecycle/health boundaries before fills and new signals. A valid response made usable after that boundary cannot reverse retirement or repair the completed streak. The first applicable immutable terminal order outcome wins; later reasons may be diagnostics only. Never charge a second fee for cancellation.

Existing filled positions remain owned by their original campaign/pool and remain pinned. Retirement alone does not create a new exit trigger: they follow existing stops, holding/session/recovery exits and hazards. Never transfer inventory into a replacement watched mint or another pool. If cancellation removes the last order pin and no position remains, release that pin; capacity admission occurs at the next ordinary admission opportunity, without backfill. All scenarios receive retirement from the same membership event but release only their own reservations.

## 5. Required eligibility and security boundary

Required gates, all evaluated using fresh evidence:

1. Supported chain, target program, quote mint, pool owner and validated layout.
2. Pool initialized, swap enabled, open time reached; distinct mints and positive effective curve reserves.
3. Target mint initialized, positive supply, mint authority absent, freeze authority absent. Classic SPL authority meanings are documented in [R6]. Target decimals 0–18; larger is explicitly unsupported v1.
4. Vault mint identities match pool references; vault authority matches the pool PDA derived from pinned official seeds; both vault token accounts initialized and not frozen.
5. Supported fee configuration, valid fee numerator/rates, no arithmetic overflow, and current program hash supported.
6. Required evidence freshness and state coherence satisfy §6.
7. At least 16 valid consecutive minute prices for the selected pool, including a full 15-minute history.
8. USDC effective reserve at least 20,000 USDC; proposed input at most 0.1% of USDC reserve.
9. Size-specific curve price impact at most 1% at entry; same-snapshot modeled buy-then-sell loss, including primary modeled costs, at most 2%.
10. Risk/session gates in §10, §11.

These checks establish **model eligibility**, not token safety. No claim is made about developer identity, launch bundles, wash trading, holder concentration, LP permanence, program governance or rug risk. Set those report fields to `NOT_ASSESSED`, never `PASS`. LP/holder/developer/bundle filters are excluded from v1 eligibility. A future safety-screened strategy must supply its own verified attribution/LP contracts.

Each gate result contains rule ID/version, input evidence IDs, observed value, threshold where relevant, and `PASS|FAIL|UNKNOWN|STALE|CONFLICT|UNSUPPORTED|INVALID`. Every required result must be `PASS` before an entry. Optional NOT_ASSESSED fields are separate from required gates. Exit eligibility requires execution mechanics, supported identity and fresh reserves, but not entry momentum, minimum reserve, revoked target authorities, position count or session loss rules. Current supported program and synchronized-clock evidence remain required for every modeled submission; stale health keeps exits requested but unsubmitted. Record changes in target authority as hazards; a mechanically valid exit may still be simulated. Never let entry-only gates prevent risk reduction.

## 6. Time, data quality and event ordering

Use UTC integer microseconds for stored time, timezone-aware conversion only at the boundary, and a monotonic clock for waiting. Preserve `provider_time` nullable, `request_started_at`, `received_at`, `context_slot`, `commitment`, `block_time` nullable, and `available_seq`. API HTTP Date is not market event time.

Use finalized commitment for all chain snapshots. This intentionally trades timeliness for replay clarity; report “finalized-state paper model,” not low-latency execution. `minContextSlot` is a lower bound, not a request for historical state. A complete bundle must share one response context. Accepted context slots are nondecreasing per pool; a lower one is discarded. Equal slot/state can refresh transport health but cannot create a new market observation or execution snapshot. A still-fresh previously validated snapshot may supply a minute bar; record that reuse explicitly. A newer context slot with unchanged reserves is a new snapshot, not a conflict. Different account states for the same account and finalized context slot are CONFLICT, with permanent affected-pool/campaign scope and cancellation rules in §6.3.

At decision time, a bundle must have been received within 10 seconds; request elapsed time at most 10 seconds. Resolve `getBlockTime(context_slot)` and cache by slot; its age at receipt must be between -5 and 90 seconds. Missing block time means `UNKNOWN`, not receipt-time substitution. Block time is approximate and this gate is a coarse lag check, not a clock synchronization proof. Validate the host is time-synchronized during preflight; an observed UTC step versus monotonic time exceeding 2 seconds puts the session into recovery. Future metadata timestamps >5 seconds are INVALID; undated optional metadata remains undated.

One writer assigns increasing `event_seq` as observations become durable. Live processing and replay consume this sequence, not a retrospective sort by chain timestamp. Late observations never change prior decisions. For replay, store timer events and their ordering as data; never derive timers from replay wall time. At equal logical time use the explicit scheduler priority in §6.1; never rely on asyncio callback ordering. Sort simultaneous pools by raw address bytes. Run a final risk check before committing any buy fill.

Minute price at boundary t is the latest complete fresh bundle with both received_at and available_at at or before t. Define `p = (USDC_reserve / 10^6) / (target_reserve / 10^target_decimals)`. Record selected evidence, not a synthetic trade close. If no valid bundle exists, the bar is missing. Do not interpolate or use future/backfilled responses. Returns and rankings use Decimal precision 50, ROUND_HALF_EVEN; compare thresholds with unrounded values. Display rounding never affects decisions.

### 6.1 Scheduler and freshness expiry [D]

One writer owns a priority queue of timer events. Process due work on a one-second monotonic tick independently of network completion. At equal UTC microsecond, subject to the hard-boundary barrier in §6.2: (1) commit ready validated observations by receipt ordinal then pool bytes, without waiting for earlier unvalidated items, (2) enforce operator/schedule boundaries and health/mark expiry, (3) update marks and exit triggers including holding deadlines, (4) resolve pending fills and execution deadlines, (5) freeze minute bars/equity, (6) evaluate entries, (7) schedule collection. Portfolio tie order is H1-primary, H1-stress, H1-severe, H2-primary, H2-stress, H2-severe; pool/mint ties use raw bytes. Persist timer ID, intended time, actual processing time, priority and missed-tick count. No backdated order or inferred fill is permitted after a delayed tick. Reconstruct missed denominators, not missed decisions. Actual processing time controls expiry. Python explicitly leaves equal-time delayed-callback order undefined [R18]; application priority is therefore required.

Freshness is evaluated at every use and every timer tick. A mark expires when receipt age exceeds ten seconds or its cached block time age exceeds ninety seconds. Emit MARK_EXPIRED once, clear current value, block entries, recompute conservative equity and loss limits, and continue time-based exit handling without needing another RPC response. Record `invalid_since`; after sixty continuous seconds without a valid mark request an exit. A fresh mark clears only transient data blocks, never a latched session halt or permanent fee deficit. UNKNOWN and a valid zero liquidation value are distinct.

A program check is current for five minutes plus a ten-second request allowance. If not renewed, block new submissions with PROGRAM_CHECK_STALE; keep positions/exit requests and resume only after a matching fresh check. An actually changed program hash permanently blocks that campaign's model. Matching checks may resume after transient outages; changed source/decoder contracts require a new campaign, and legacy exposure stays in its original blocked campaign. No automatic inventory transfer or source-model revision of old fills is permitted. Runtime clock status is sampled at startup and every five minutes using `timedatectl show -p NTPSynchronized --value` with a two-second subprocess timeout. Missing command, unknown synchronization or false result blocks provider mode with CLOCK_UNVERIFIED; do not install or configure a time service automatically. Compare UTC and monotonic elapsed time each tick; a step exceeding two seconds cancels all pending orders including sells (fees retained), requests exits, clears feature buffers and blocks entries until three advancing recovery polls in the current generation/epoch plus synchronized clock evidence restore transient health. Retain session loss latches.

### 6.2 UTC grid, hard boundaries and missed timers

Use integer UTC microseconds, with one-second ticks at multiples of 1,000,000, polls at multiples of 5,000,000, and minute boundaries at multiples of 60,000,000 since Unix epoch. Discovery uses minute boundaries; five-minute health refreshes use the same grid. Starting mid-grid schedules the next boundary, not a launch-relative cadence. Local session dates only determine persisted session boundaries. Run preflight and recovery immediately at launch; do not wait for the next periodic refresh.

Every writer cycle samples actual UTC/monotonic time before applying economic transitions. Hard stop, entry cutoff, final-window expiry, freshness and execution-deadline predicates are tested against actual processing time. Observations may be durably stored first, but that never authorizes an economic transition forbidden by an already elapsed boundary. No backdated fill is allowed. At the exact entry cutoff, BUY cancellation wins over a possible fill. At exact final-window expiry, every unresolved order is canceled before any fill. An ordinary execution deadline is inclusive: resolution at the deadline is permitted; resolution after it fails NO_EXECUTION_STATE even if evidence arrived earlier. Record late processing separately from missing provider state.

Freeze boundary features/equity using only evidence with received_at AND available_at no later than the intended boundary and event_seq before that boundary's recorded cutoff. Do not use a later mark simply because the timer ran late. A delayed writer can reconstruct a boundary valuation only from fully durable pre-boundary evidence, never from future observations; otherwise its boundary value is unavailable. Record boundary processing lag. Opening/closing snapshots count as on-time for §14.1 only when processed within one second of the intended boundary, with no intervening UTC-step recovery. A late opening cannot be repaired into interval eligibility by retrospective reconstruction. Minute entries may run late only while the original signal remains unexpired, all actual-time session gates pass, and the original boundary evidence still passes current freshness. Skip older entry timers; do not run a burst of historical signals.

Process missed timer intervals as missing coverage records, followed by one current health/deadline evaluation; never fabricate historical heartbeats. The first fresh coherent candidate means the first candidate made decision-available in durable sequence, not the smallest chain timestamp or shortest later-discovered request time. A disabled/frozen bundle with supported identity/layout is a valid execution candidate whose mechanics fail; it must not be filtered out as generic invalid data so that a later favorable state can fill.

Clock/program health is valid only through its last successful check plus 310 seconds. Failed or absent clock refresh blocks submissions even without an observed clock step. NTPSynchronized is evidence of the kernel's reported synchronization status, not a measured error bound or proof that WSL's clock matches an exchange clock [R22]. Preserve that limitation. A UTC step invalidates all pending orders, including sells, with CLOCK_STEP; retain fees and exit requests, then require fresh health and recovery evidence for a new attempt. Monotonic time controls waits; it cannot rewrite persisted UTC evidence.

### 6.3 Receipt ordering, slot watermarks and conflicts

A network response creates RAW_RECEIVED with immutable request ID, response receipt ordinal and receipt time. Receipt alone does not make a snapshot usable. The finite durable availability protocol in §6.4 exclusively defines usability and its witness.

Ready items in the same writer cycle sort by receipt ordinal then raw pool bytes. Do not hold ready B waiting for earlier-received but unvalidated A. Per-pool accepted slot watermark advances only when the snapshot reaches witnessed decision availability under §6.4. SNAPSHOT_READY alone does not advance it. If A later validates below that watermark, retain it as OUT_OF_ORDER, never as a historical bar repair or fill candidate. Equal-slot identical account state is duplicate evidence; it may refresh transport statistics but not snapshot availability or market freshness. This prevents identical replies from extending the life of old market evidence.

Detect a conflicting account at an already observed finalized slot even if a newer slot has since been accepted. Compare identity/owner/executable/data for the same account+context slot; receipt metadata and JSON key order are not account state. Preserve both payloads. Latch POOL_CONFLICT for every pool referencing the conflicted account for the campaign; cancel their pending buys, invalidate their pending sells with fees retained, and block further submissions. Keep inventory, null marks and evidence. No automatic resolution by accepting whichever version arrived later. Conflicts involving shared mints/configuration affect every referencing pool; program evidence affects the whole campaign. This gives §6's conflict halt an exact scope and reset policy.

### 6.4 Finite durable snapshot availability

Use this finite protocol for every snapshot:

1. Persist raw evidence and validated snapshot in transaction A. A successful commit makes the snapshot durable but not decision-available.
2. After A returns successfully, sample UTC and monotonic time and append SNAPSHOT_READY in transaction B, referencing A. No dependent decision executes before B returns successfully.
3. Immediately after B returns, sample `usable_at` and monotonic time. This is effective decision availability. Queue an AVAILABILITY_WITNESS containing snapshot ID, B sequence, usable_at, and clock epoch. Commit that witness before or in the same transaction as the first dependent timer/decision. It may be batched with independent witnesses. The witness records a completed earlier acknowledgment; its own acknowledgment does **not** redefine usable_at. There is no recursive witness.
4. Use requires B to have succeeded, the witness to be durable by the dependent decision's commit, and usable_at <= intended boundary where a boundary is involved. Actual-time deadlines and freshness still apply at decision processing. Witness event sequence must precede dependent economic event sequence, even if they share a transaction.

If killed before B succeeds, the snapshot is unavailable. If B succeeds but no witness survives, it cannot be treated as historical decision-available evidence on restart. If witness and dependent decision commit atomically, both survive or neither does. Replay uses only persisted witnesses, with their recorded clock epoch and order; it never estimates a missing acknowledgment. Ordinary restart still cancels pending orders and clears live features. This protocol deliberately prefers missing evidence over retrospective availability.

Example: A acknowledgment at 59.900, B acknowledgment/usable_at at 60.050 means the snapshot cannot supply the minute at 60.000, even if its response arrived at 59.000. Persisting its witness at 60.100 does not backdate availability to response receipt or to A. Reusing a valid witness in later decisions creates no new market observation. Duplicate equal-slot state never refreshes its usability/freshness under §6.3.

### 6.5 Runtime generations and health watermarks

Every invocation that can collect data gets a durably incremented `runtime_generation` before dispatch. Every request and validation task carries generation plus `clock_epoch`. Increment clock_epoch on a detected UTC step before processing further market/economic work. The existing pending-order cancellations and feature resets still apply. A completion belonging to another generation or earlier clock epoch is retained as LATE_GENERATION evidence, never used for bars, freshness recovery, new submissions or fills. Canceling an async task is not itself proof that no completion can arrive.

A response received before the step but still awaiting validation/witness is also ineligible after the step. Previously witnessed snapshots remain historical evidence but cannot supply current decision state after recovery starts. Each pool must obtain its three advancing recovery polls wholly in the current generation/epoch; the clock check must also complete there. No process-global cache may bypass this. Historical witnesses and economic events are not rewritten or erased.

Maintain an independent finalized-context watermark for successful coherent program checks. Startup initializes it from the pinned deployment capture. Request `minContextSlot` at least that watermark; validate the returned context explicitly. An older returned context cannot refresh health or clear authority-change recovery even if its code matches. Equal context with identical fingerprint is duplicate evidence: retain it but do not extend program-health validity. Only a strictly advancing coherent check can refresh that validity. A conflicting same-context program/ProgramData state uses the existing permanent campaign conflict policy. Compare fingerprints only after structural/context/generation validation; a malformed old response is not proof of PROGRAM_CHANGED.

For a successful program check, the health-age anchor is its response receipt time; availability is after durable successful validation/witness. A check that takes too long to validate does not acquire a new 310-second lifetime when it is finally processed. A clock check's anchor is subprocess completion time in the current epoch. For both, validity expires strictly after anchor+310 seconds, with equality allowed, as inherited. Apply current UTC/monotonic consistency and existing hard-boundary barriers. These rules bound local observation age; they do not prove uninterrupted deployment identity between sampled checks.

Official getMultipleAccounts exposes commitment, context and minContextSlot [R38]. The watermark and generation protocol are application design choices, not a provider guarantee of historical reads or cancellation.

## 7. Study gate and preregistration



### 7.1 Study

Run 14 consecutive scheduled nightly study sessions, 20:00–06:00 America/Detroit. These are **calendar sessions**, not “14 successful nights”; missed launches/outages count as missing. Study performs collection, feature computation and hypothetical quote diagnostics, but no position creation. Freeze discovery, scope, timestamps, costs, hypotheses and report metrics before session 1. Persist preregistration SHA-256 and time.

Define denominators before observing outcomes:

- A scheduled pool-poll opportunity is every five-second tick while that pool occupies a watched/pinned slot. Transport failures and disabled adapters count as failed opportunities.
- A valid opportunity is a complete bundle accepted under §6 by the following tick. Additional late bundles remain evidence but do not repair coverage.
- Minute feature coverage is valid minute bars / scheduled watched pool-minutes.
- Mechanically eligible pool-minute means identity/security gates 1–6 pass, before reserve, history, signal, cost and risk gates.
- Quote diagnostic success means the 100-USDC quote (or reserve-capped amount, if smaller) and full reverse quote can be computed with the primary model. Report capped and uncapped diagnostics separately; only the capped-or-full quote defined in §7.3 supplies the pass-gate numerator.

Feasibility passes only if: all 14 session records exist; at least 95% of planned wall-clock study time has an active collector heartbeat; valid bundle coverage ≥95%; minute-bar coverage ≥95%; at least ten distinct supported target mints and 1,000 mechanically eligible pool-minutes are observed; quote diagnostics succeed for ≥95% of mechanically eligible pool-minutes; no unresolved conflict, deployment change, or ledger integrity error remains. Minimum samples are operational adequacy choices, not statistical power claims. Zero denominators mean fail, never 100%.

### 7.2 Automatic strategy selection after study

If feasibility passes, select fixed H2 for the prospective primary paper portfolio. If it fails, disable all H1/H2 real-data order generation, select H0 and emit `STUDY_INSUFFICIENT` with each failed criterion. No threshold tuning, no choosing the best study P&L, no extending the study until it passes, and no migration to a different provider without a new campaign specification. H2 can be fully implemented and tested with fixtures before the study; its real-data activation waits for this gate.

After study, close the study dataset, enforce one full scheduled night as embargo/warm-up with no entries, then run 28 consecutive prospective nightly sessions. Reset all study feature buffers before embargo. The holdout is not used to revise parameters. Final results are exploratory paper evidence; no automatic “edge proven” or promotion to real trading exists. Research on backtest overfitting and selection bias motivates restricting trials and retaining negative outcomes [R8, R9].

### 7.3 Calendar and denominator construction [D]

`init` freezes the next 20:00 America/Detroit boundary strictly after its invocation as study start, then fourteen consecutive local session dates, one embargo date and twenty-eight prospective dates. There is no automatic rolling start or replacement night. `study-evaluate` runs after the scheduled final study boundary; before that it returns STUDY_NOT_FINISHED. If evaluation is late, the embargo and prospective dates still do not move. All run modes derive their phase from the manifest; an incompatible CLI mode fails. Embargo uses collection without orders. Study failure produces H0-only prospective records for the same frozen calendar, and statistics remain INSUFFICIENT_EVIDENCE.

First-seen and retirement wall-clock age continue while stopped. Watch membership, selected pool, admissions and retirements are durable events. Reconstruct five-second opportunities for persisted memberships over [session start, session end), including downtime. A membership ends at its scheduled 48-hour retirement even if the process is down; on restart record that scheduled expiry and actual reconciliation time without retroactively admitting another mint. A missing-response streak is measured on scheduled minute boundaries while running, resets on a valid observation, and is not inferred from unobserved hours; use the 48-hour retirement for stopped periods. No-watch intervals have zero pool opportunities but remain in heartbeat and discovery coverage denominators. A heartbeat is durable once each five-second tick; it covers that tick's interval only, never an entire gap. Report scheduled/observed discovery ticks as an additional diagnostic, not a new study-pass threshold.

A poll opportunity belongs to its intended five-second tick; one accepted bundle can satisfy only one opportunity per pool. Receipt and validation must finish by the next tick, inclusively, to count valid. Retry responses arriving later remain evidence but cannot repair that denominator. Missing minute bars and returns remain missing. Mechanically eligible minutes require a fresh boundary snapshot; quote success denominator counts those minutes even if minimum order size prevents a trade. Diagnostic size is min(100 USDC, floor(0.001 × quote reserve)); nonpositive/unquotable size is a failure. Do not use observed rows as the scheduled denominator.

## 8. Signals, controls and selection



### 8.1 H2 primary hypothesis

At each minute boundary in the entry window, on each eligible selected pool:

- `r15 = p(t)/p(t-15m)-1`; `r5 = p(t)/p(t-5m)-1`.
- Require `0.03 <= r15 <= 0.20` and `r5 > 0`.
- Rank descending r15, then descending current USDC curve reserve, then ascending mint bytes, then pool bytes.
- Submit in that order until capital/position capacity is exhausted. A pending buy reserves a slot and capital immediately.
- A signal expires at boundary time plus 30 seconds, with submission strictly before expiry; evaluation cannot reuse it after expiry. One pending order per mint; one open position per mint per portfolio. No pyramiding and no re-entry in the same session after a buy fill, regardless of subsequent close. A rejected buy may be reconsidered at the next minute if all gates pass.

No composite score, learned weights, holder feature, “smart money,” volume confirmation, or narrative override is implemented. The 3%/20% thresholds are unvalidated experimental parameters, chosen for a simple falsifiable hypothesis. They are not claimed to be the best trading rule.

### 8.2 Controls and cost scenarios

H0 holds virtual USDC, zero trading cost and zero return in that numeraire. H1 is a deterministic randomized-timing control: at each eligible mint-minute compute SHA-256 of UTF-8 `campaign_id|H1|mint|UTC_minute_ISO_Z|seed=20261106`; interpret first eight bytes as unsigned big-endian. Trigger if integer modulo 60 equals zero. Rank triggered entries by that integer ascending, then mint bytes. All other rules match H2. This is a sparse random benchmark, not an exposure-matched causal experiment; report differing exposure and turnover.

Run H1 and H2 in independent portfolios under three fixed scenarios:

| Scenario | Fill delay | Adverse output haircut | Execution-cost proxy per modeled submitted order |
|---|---:|---:|---:|
| Primary | 5 seconds | 25 bps | 0.10 USDC |
| Stress | 15 seconds | 100 bps | 0.50 USDC |
| Severe | 30 seconds | 300 bps | 2.00 USDC |

Each portfolio starts with its own 10,000 USDC. Share immutable observations, never capital or virtual inventory. These are sensitivity assumptions, not measured network-fee forecasts. H2-primary is the predeclared main result; never select the scenario with the best P&L. Primary signal expiry of 30 seconds applies to submission; fill deadlines are separately defined below.

### 8.3 Portfolio and scenario isolation [D]

The six funded portfolio IDs are `H1-primary`, `H1-stress`, `H1-severe`, `H2-primary`, `H2-stress`, `H2-severe`. H0 is an analytical constant-USDC series, not a seventh ledger. During study these accounts exist but do not trade; the sole initial-capital event occurs at init, and no study expenses are invented. Each remains at initial cash until prospective activation.

Shared entry eligibility uses the primary model at the fixed diagnostic size defined in §9.4, independent of portfolio. Each actual proposal must additionally pass the size-specific checks there. This defines the common eligible cohort; stress/severe round-trip losses are reported but do not add another two-percent gate. Each portfolio independently calculates its own available size, costs, equity and risk. Delay, haircut, failed orders and costs may produce different entries and exposure. Report these as separate policy paths under cost assumptions, not a matched-trade cost decomposition. Common signal thresholds and mint history never consume another portfolio's cash, order slot or same-session entry restriction. H1 hash uses UTC minute formatted exactly `YYYY-MM-DDTHH:MM:00Z`, without fractional seconds; mint means its canonical base58 string. Rank after portfolio-specific gates. Evaluating one scenario must not mutate another scenario's features or evidence.

## 9. Counterfactual execution contract



### 9.1 Meaning and limits

A paper fill means the specified curve model could exchange a size against a later observed pool state under declared costs. It is not a submitted or simulated Solana transaction and does not establish inclusion probability, MEV cost, transfer success, or realizable profit. There is no transaction builder, signer, `simulateTransaction`, wallet address, or key parser. The all-or-none model reflects the single atomic swap being modeled; no arbitrary partial fills or order-book queues are invented.

### 9.2 Curve arithmetic

Only the zero-creator-fee subset in §3 is supported. From each side's raw vault amount subtract its accrued protocol, fund and creator-fee balances according to pinned source; negative or zero effective reserves fail. Token amounts and reserves are integers. Decode trade fee rate f with denominator D=1,000,000 [R10]. For input A and source/destination effective reserves X,Y:

- `fee = ceil(A*f/D)`; `a = A-fee`.
- `curve_out = floor(a*Y/(X+a))` for this supported constant-product model.
- Reject nonpositive input/a/output, output ≥Y, out-of-range u64 inputs/reserves, or arithmetic exceeding the pinned u128 intermediate bounds.
- `model_out = floor(curve_out*(10000-haircut_bps)/10000)`.

Trade fees are embedded in output, not charged again in USDC. Record them in the input token and their descriptive USDC conversion at the decision price. Separate the output impairment from curve fees. Underlying constant-product and fee-rounding behavior must agree exactly with pinned official reference fixtures [R10, R11]; a mismatch blocks provider-backed simulation rather than being hidden by a numerical tolerance.

Price impact gate uses `1 - (curve_out/a)/(Y/X)` before the adverse haircut, with exact rational comparison; zero fee-adjusted input rejects. For round-trip eligibility, model buy and then sell on a **temporary post-buy reserve copy**, adding the full input A less protocol/fund fee shares to the input curve reserve and subtracting the curve output from the other reserve. Credit the trader only impaired output. Include both execution-cost proxies in round-trip loss; charge nothing to the ledger for this diagnostic.

### 9.3 Order timing and fills

On accepted proposal, calculate reference impaired output from fresh state; set immutable `min_out = floor(reference_model_out * 0.98)`. Reserve buy notional plus one execution-cost proxy. Record `SUBMITTED` atomically; at that moment debit the execution-cost proxy, including if the later modeled submission fails. A locally rejected proposal costs nothing.

Fill eligibility time is submission time plus scenario delay. Use the first complete bundle whose request **started at or after** that time, has received_at and available_at no later than execution_deadline = submission time + scenario delay + 20 seconds, and is actually resolved by that deadline under §6.2, passes freshness and has context slot greater than submission slot. The interval is inclusive at both ends; a request begun before delay expiry never qualifies even if received later. Do not select the best snapshot from the interval. Malformed, stale, incoherent or unsupported bundles do not qualify; retain their rejection reasons. The first fresh coherent supported candidate is binding: disabled/frozen mechanics, below-minimum output, or failed fill-time risk terminates the order, rather than waiting for a better candidate. If none arrives, order fails `NO_EXECUTION_STATE`; release reserved notional/quantity. If modeled output is below immutable min_out, fail `SLIPPAGE`; do not fill at the threshold. Recheck execution mechanics and risk before the buy fill; a newly latched halt cancels pending buys. Fill and balance/position updates occur in one transaction.

Sell attempts use full remaining target quantity, reserve it, and have their own fresh min_out/delay/deadline. Failure leaves quantity untouched, marks exit pending, and permits the next scheduled retry. No route or invalid state means no submission and no modeled submission fee. A session halt does not cancel already submitted exits.

Across real snapshots, virtual orders do not mutate observed pool reserves. Within a portfolio, only one position/pending order per target/pool prevents repeated same-pool buy pressure; primary sizing is limited to 0.1% reserve. This is a small-participant counterfactual, not a persistent market-impact simulation. Document that omission, including potential interactions between the participant and later market activity. Severe liquidity-withdrawal fixtures must demonstrate losses and blocked exits; stress haircuts cannot be advertised as a calibrated rug or MEV model.

### 9.4 Cohort diagnostics and temporary reserve accounting

Shared eligibility gate 9 uses q = min(100, floor_atomic(0.001 × USDC effective reserve)), in USDC, identical to the §7 diagnostic. q below 10 USDC is ineligible for entries but still enters quote-diagnostic reporting as §7 specifies. Compute primary-model impact and round-trip loss at q. H1 and H2 use the identical cohort before portfolio constraints. After computing each portfolio's notional A under §10, independently rerun impact and the primary-model round-trip gate at A; fixed fees make a smaller order potentially less efficient. Failure rejects the proposal; do not search for a different amount that passes. Stress and severe use primary costs for this eligibility recheck, then their own costs for submission and fills. There is no circular resize loop.

For any such diagnostic, let C be the primary per-submission USDC cost, B the impaired buy target output, and S the impaired USDC sell output on the temporary post-buy state. Define round_trip_loss = (A + 2C − S) / A, without clamping negative results. Compare exact integer/rational quantities to 0.02. A excludes fees; the two proxies are additional expenses. The diagnostic never debits real ledger cash. Fixed min_out is computed from each actual scenario's reference output and actual immutable amount, not from q.

On the temporary post-buy state, curve source reserve increases by A minus protocol and fund fee shares, while destination reserve decreases by curve_out, not by impaired output. Protocol/fund shares are floor(trade_fee × share_rate / 1,000,000), subject to exact agreement with pinned source fixtures; unsupported share semantics block provider mode. Creator share is zero in this scope. The difference between curve_out and impaired output is a model loss attributed outside trader inventory; do not put it back into the simulated pool. The reverse trade spends only B. Integer floor/ceil order must match the pinned reference gate. No source retrieval in this revision established a deployment-compatible curve lock; that obligation remains NOT_RUN, not verified [R24].

Target and USDC vault accounts must be owned by the classic SPL program; USDC mint must decode to six decimals. Standard initialized target mint/account layouts only; unexpected lengths or account semantics are UNSUPPORTED, not decoded with guessed offsets. Verify target and quote token account delegates/native-account flags against supported pinned token semantics; support only absent delegates and non-native token accounts. Token account close authority is recorded as a hazard, not evidence of permanence. Entry safety claims remain excluded.

### 9.5 Zero outputs, net marks and source-operation overflow

Reject an order quote if curve_out is positive but model_out is zero: ZERO_MODEL_OUTPUT, locally rejected with no submission fee. A nonpositive immutable min_out also rejects locally; never create a zero-quantity position or zero-protection order. For valuation, mechanically valid full-inventory quote with impaired output at or below prospective fee produces a valid net mark of zero. Keep the distinction: zero valuation can exist without an executable new order. Trigger exits as specified; an unquotable sale keeps inventory and does not charge a fee until a later valid submission.

Validate f in [0,D), protocol/fund shares each in [0,D], sum <=D, accrued fees and raw token amounts in their declared ranges. Creator fee exclusions remain exactly §3, including configured rate. Validate source raw-vault post-transfer amounts and accrued-fee counter updates against their declared integer ranges, as well as effective reserve/intermediate arithmetic. Python arbitrary integers must not make an on-chain overflowing operation appear supported. Map each checked operation to its pinned source fixture; extra model haircut multiplication may use arbitrary precision because it is not an on-chain operation. Quote failures are typed and cannot be turned into a different formula.

Official instruction source retrieved here confirms the invariant check and fee update sequence [R28]. Full calculator/fees and constant-product source retrieval was incomplete in this audit; the existing illustrative arithmetic is not upgraded to an independently verified source fixture. Do not invent a source commit or deployment equivalence.

## 10. Capital, risk and accounting

Each portfolio begins the prospective campaign with 10,000 USDC; no daily reset or replenishment. Fixed buy notional is the minimum of 100 USDC, 1% of current conservative equity, 0.1% of USDC curve reserve, available unreserved USDC less the submission-cost proxy, and remaining 300-USDC aggregate entry-cost capacity. Floor to USDC atomic units; reject below 10 USDC. Maximum three open+pending-buy positions per portfolio. Entry-cost exposure includes remaining original buy notional on open positions, even if marked down to zero. Pending buy notional counts toward the cap.

At each valid observation for an open position, compute modeled full-quantity liquidation proceeds using that scenario's fee/haircut, less one expected exit-cost proxy, floored at zero. This is a mark, not a fill. Stale/missing/unexecutable marks are null. Last known marks may be displayed with age but cannot become current equity.

`conservative_equity = cash_USDC + sum(fresh_net_liquidation_marks, substituting 0 for unknown marks)`. Reserved cash is a subset of cash, not a second asset. Unknown marks also latch a no-new-entry condition until fresh evidence returns. Record conservative losses from unknown marks separately from realized losses.

Session starting equity is conservative equity at session open after recovery; if any position has unknown value, entries stay blocked. If equity falls to ≤98% of session starting equity, latch `SESSION_LOSS_LIMIT` for that session, cancel pending buys, and request exits. This cannot guarantee a 2% maximum loss. Portfolio cash may become negative solely because a submitted emergency exit costs more than available cash; record an explicit virtual fee deficit and permanently disable new entries until campaign ends. No simulated capital injection is allowed.

Position cost basis is buy USDC notional plus that successful buy's submission proxy. Failed or still-pending entry fees are portfolio expenses, not a fictional position; on fill, reclassify the successful submission fee into position basis without debiting cash again. All already-debited sell-attempt fees, including pending, failed and canceled submissions, are immediately position expenses. A successful sell fee is included once in the same cumulative total, never debited or attributed twice. Realized P&L on close equals gross sell USDC proceeds minus basis minus all sell-attempt proxies. Open-position unrealized P&L equals current net liquidation mark minus basis minus all already-debited sell-attempt fees. Portfolio total P&L equals equity minus initial capital, and must also equal closed realized + open unrealized − fees of failed/canceled/still-pending buys, using conservative open values when unknown. Store both accounting identity and unknown-valuation flags.

At buy submission, cash decreases only by the proxy and reserved notional remains a subset of cash; fill then debits that notional and releases it. Remaining exposure capacity counts the accepted notional, not the submission fee. At final buy check compare total reserved/open counts INCLUDING this order against the caps; do not add it twice or shrink a submitted notional. Other portfolio risk gates are reevaluated. Risk failure cancels the order and retains the submitted fee. Exits may incur a negative cash fee balance as specified.

Liquidation marks always subtract one additional prospective exit fee, including while a sell is pending. Already-paid sell fees are separate expenses. This is explicitly a conservative retry-cost reserve in valuation, not a second cash debit; the allowance disappears when the position closes. A pending sell may therefore cause a temporary extra conservative expense that reverses on successful fill. Compare total P&L to the stated mark convention, not to an imagined guaranteed pending fill.

Store balances in atomic integer units. Python integers must be range-checked against declared source types; database token amounts use canonical base-10 TEXT to avoid signed-64 overflow. USDC balance also uses integer-string representation. Ledger accounts are portfolio cash, per-position token inventory, pool/counterparty transfers, fee expense and realized P&L attribution. Event-level cash/quantity deltas are authoritative; positions and balance caches are transactional projections. Never recompute historical fees from a later config.

### 10.1 Atomic post-fill risk and initial marks

Before a BUY fill, project its exact notional debit, already-paid proxy, acquired quantity, and the new position's scenario net liquidation mark against that same candidate snapshot. Revalue other positions using their currently fresh marks; unknown means zero and blocks entry. Apply the session-loss threshold to this projected equity, not merely the pre-fill equity. If the projected state would reach or breach the threshold, cancel the buy with FILL_RISK_SESSION_LOSS, retain its fee, latch the halt, and request exits on existing positions. Do not book the rejected fill or its hypothetical valuation. This is a conservative admission rule, not a prediction that actual trading caps losses.

After a successful fill, compute and persist its first mark and high-water value immediately; evaluate exit triggers in that transaction's ordered follow-up before generating any further entry. A sufficiently bad stress/severe mark can trigger an immediate exit request. Stops compare the net mark to basis as §11 specifies, not a price-only return. Already-paid sell fees affect portfolio equity and P&L but do not modify the basis or trailing rule. Subsequent orders continue in the fixed portfolio order and see committed state. Latches are per portfolio unless the cause is shared clock/program/integrity health. One portfolio's loss threshold never stops another solely through shared observations.

### 10.2 Exact gate arithmetic and reproducible statistics

Keep §6's prescribed Decimal(50, ROUND_HALF_EVEN) prices/returns/ranking; construct a local context explicitly inside each pure calculation. Do not rely on thread/task defaults. Trap InvalidOperation, DivisionByZero, Overflow and FloatOperation. Inexact/Rounded are recorded where useful but allowed for nonterminating price divisions. A bar's canonical internal price stores the full resulting Decimal value with fixed-point notation and trailing fractional zeroes stripped; zero is '0'. Display prices remain twelve significant digits. Recompute signals from stored internal values, never displayed prices. Python documents precision/context-dependent operations [R30]; 50-digit arithmetic is a design choice, not exact real arithmetic.

Curve quantities, min_out, fixed costs and exposure remain integers. Compare session loss via 100*equity <= 98*baseline; stop via 100*mark <= 94*basis; trailing arm via 100*mark >= 112*basis; trailing stop via 100*mark <= 95*high_water. Size percentages floor by integer division. Do not round a ratio before a gate. Basis/high-water/mark use atomic USDC, so these comparisons are exact. Rational quote impact and round-trip comparisons remain exact per §9 and 23.4.

For reported session returns and bootstrap means, use fractions.Fraction from integer equity deltas and positive integer starting equity until final display; sort bootstrap statistics as rational values. RNG/index algorithm and nearest-rank endpoints remain §14's. Floating-point arithmetic is forbidden for those statistics; the estimand is unchanged. Human display converts with sufficient local Decimal precision for required HALF_EVEN rounding. H0 return is exact zero. Missing/nonpositive denominator yields null, never Fraction(0,0).

The minimum sample gates allow exploratory intervals only; they are not a power calculation. The backtest-overfitting literature warns that holdout use alone can fail to protect strategy selection [R31]. Retain all unsuccessful campaigns. No new optimization, causal benchmark claim or live promotion rule is introduced.

### 10.3 Mark refresh and economic transition ordering

On a newly available pool snapshot: (a) validate shared health/mechanics and conflicts; (b) refresh all existing positions referencing that pool under their own scenarios; (c) evaluate their exit triggers and portfolio latches; (d) resolve pending orders in existing fixed portfolio order; (e) apply immediate post-fill mark/trigger rules; (f) process new entry proposals only at a qualifying minute. No quote mutates shared observed reserves.

Any cash fee debit immediately recomputes that portfolio's conservative equity and session loss gate using currently fresh marks. If it breaches the threshold, latch SESSION_LOSS_LIMIT and cancel pending buys before another buy may fill. Exit requests remain active. An already debited successful BUY fee is not charged again during projected post-fill checking. Equality remains the exact integer tests of §10.2. A sell fill removes its prior mark and inventory atomically and replaces them with gross USDC proceeds less the fee already debited at submission. Recompute risk before the next economic transition.

High-water/trailing and per-position stop still compare fresh net mark to original basis as specified. Already-paid failed-sell fees affect portfolio equity and realized/open P&L attribution; they do not reset basis or manufacture a new trailing high. Permanent fee-deficit latches remain campaign-long. This does not change thresholds or promise bounded loss.

## 11. Position exits and session lifecycle



### 11.1 Exit trigger priority

On every accepted bundle (not just minute boundaries), use the first applicable trigger:

1. Operator stop, session liquidation, session loss halt, or recovery requiring exit.
2. Target authority hazard or pool disablement: request exit; submit only if execution mechanics permit it.
3. Net liquidation mark ≤94% of position basis: stop-loss trigger.
4. Trailing rule: arm once net liquidation mark reaches ≥112% of basis; thereafter exit when mark ≤95% of highest fresh net liquidation mark since entry.
5. Maximum holding time 120 minutes since buy fill.

No fixed take-profit is implemented. When freshness alone blocks valuation, keep the position and retry data; after 60 consecutive seconds without a valid mark, request an exit that remains pending until a mechanically valid state arrives. Track the high-water mark only from fresh observed values. Clock-based exits remain due even if marks are unavailable. All triggers create an exit request, never guaranteed proceeds. Exit reason remains the first triggering reason, with subsequent hazards appended. One sell order at a time; after failure retry at the next five-second poll boundary with a fresh reference and new order attempt ID. Buy and sell minimum-output protection is never relaxed to force success.

### 11.2 Nightly schedule

Timezone `America/Detroit`; session ID is local date at 20:00 plus campaign ID. Session start 20:00, entry cutoff 05:45 next local day, liquidation time 06:00, final exit window ends 06:15. Compute each boundary with timezone rules then persist UTC; daylight-saving nights may have different elapsed hours. Study excludes the 06:00–06:15 liquidation extension from its planned observation denominator. During prospective sessions continue monitoring to 06:15.

At cutoff cancel unfilled buys; at 06:00 request all exits; at 06:15 cancel any not-yet-filled modeled orders, preserve quantities and fee expenses, mark residual positions `OPEN_EXIT_BLOCKED`, snapshot report, and stop the process. A canceled submitted order keeps its modeled submission-cost expense. Do not monitor or imply protection while the process is stopped.

At the next launch, recover persisted exposure before any entry. Obtain three consecutive valid polling bundles for each carried pool and reconcile balances. Request exits for all carried positions regardless of current profit; no new entries in that portfolio until all carried positions close. If data never returns, the portfolio remains blocked, inventory persists, and reports use zero conservative value with null market value. No age-based write-off or automatic “closed at zero” trade is permitted.

A launch after 20:00 joins the scheduled session, records missing time and needs full feature warm-up. A launch after 05:45 performs recovery/exits only. A launch after 06:15 requires explicit `recover-only`, with a 15-minute exit window and no entries; it does not create another experimental night. Missing launches generate MISSED_SESSION through writer startup or explicit reconcile-calendar; report remains read-only. Mid-session restart never resets cash, losses, cooldowns or schedule.

### 11.3 Recovery polls, feature continuity and latches

Three recovery polls mean three fresh supported complete bundles for that pool from distinct scheduled poll opportunities, strictly increasing context slots, no intervening invalid/missed opportunity. Equal-slot transport responses do not increment the streak; they are not a failure unless stale. Any invalid/missed opportunity resets it. Clock-step recovery applies this requirement to every watched or position-pinned pool before its entries/submissions resume, plus a fresh successful clock check. Normal restart additionally cancels surviving submitted orders under §12. Recovery cannot clear program-change or fee-deficit campaign latches.

At process restart, clear all signal feature buffers; preserve immutable historical bars as evidence, not a live warm-up shortcut. Clear live feature buffers at study-to-embargo and embargo-to-prospective transitions. Ordinary off-session stop/start is a restart and requires 16 new consecutive minute bars. A missing minute invalidates consecutive-history eligibility until 16 consecutive valid boundaries exist again. Carried positions retain basis, high-water, trailing state, fee attribution and first exit reason across every restart. A session loss latch resets only when the next scheduled session opens after recording its new baseline; carried exposure still blocks entries until closed. Off-session recovery has no entries and cannot reset latches or mint re-entry history for the current session.

### 11.4 Phase termination and final campaign exposure

Study and embargo stop collection at 06:00, create their closing snapshots at that boundary, and do not invent a 06:15 trading extension. Prospective sessions have the 06:15 closing boundary. Study heartbeat, pool and minute denominators cover [20:00,06:00); prospective operational coverage covers [20:00,06:15), while entry signals cover [20:00,05:45). A minute-bar opportunity is each minute boundary strictly inside its collection interval plus the opening boundary if already watched; final equity snapshot is separate. Membership start is inclusive, retirement is exclusive. Document these endpoint conventions in denominator fixtures.

An early operator stop ends active collection after its bounded exit window and creates an early-stop snapshot. The scheduled closing equity remains unavailable unless observation actually continues to that boundary; the early snapshot does not make the session complete. At end of the last prospective session, prohibit further strategy entries permanently for that campaign. Preserve blocked inventory, reports and ledger. Explicit recover-only remains available and produces append-only recovery supplements and economic bridges. No automatic extension, capital reset, later entry session, write-off, or transfer into another campaign is permitted. After the defined retention window, deletion still requires explicit operator action; expiry is not an automatic deletion job.

### 11.5 Operational phase and invocation matrix

| Manifest phase / invocation | Permitted behavior |
|---|---|
| Before first scheduled study opening | preflight/verify/report/backup; run returns NOT_IN_SESSION, code 3, no collection or capital reset |
| Scheduled study date | run --mode study; collect to 06:00; never create orders |
| Scheduled embargo date | run --mode study; derived phase EMBARGO, collect to 06:00; no orders; do not add undocumented CLI mode |
| Scheduled prospective date after study pass | run --mode paper; H1/H2 portfolios permitted only within entry window |
| Scheduled prospective date after study failure | run --mode paper; H0 observational outcome, six funded accounts unchanged except preexisting ledger events |
| Prospective date with evaluation not yet recorded | run --mode paper performs deterministic study-evaluate first from closed study data; then follows its immutable result |
| Prospective date during [06:00,06:15) | run --mode paper resumes the existing session exit-only, ending at its original 06:15 boundary; no new baseline or funding |
| Study/embargo at or after 06:00; prospective at or after 06:15 | run returns NOT_IN_SESSION, code 3; explicit recover-only/recover follows the bounded recovery contract |
| After final prospective closing boundary | campaign strategy entries permanently disabled; report/verify/backup and recover-only remain available |

Between 06:00 and 06:15 only prospective sessions may resume existing liquidation; study/embargo run returns NOT_IN_SESSION. A prospective launch within that interval is recovery/exits only. For dates outside the frozen calendar, no extra study or prospective session is created. Embargo is a frozen calendar separation, not an assurance that a process was running; log missing embargo coverage, and still reset buffers at the prospective transition. An unavailable or incomplete study always fails the feasibility gate when evaluation becomes due. Repeated study-evaluate returns the identical recorded result; it cannot overwrite a previous decision after adding later evidence.

### 11.6 Session resume and off-session recovery

`run --mode paper` invoked during [06:00,06:15) may resume the existing scheduled session in exit-only recovery. It first cancels surviving submitted orders, retains their fees, reconciles evidence and requests exits. It may never create a new 15-minute allowance: all retries terminate at the original 06:15 boundary. Existing exit requests retain their first reasons; a newly discovered carried position gets RECOVERY_EXIT. No entries, no capital reset, no shifted baseline.

Study/embargo `run` at/after 06:00 returns NOT_IN_SESSION. Prospective `run` at/after 06:15 does likewise. Explicit recover-only outside a collection interval retains the defined 15-minute window and economic bridge. If that window crosses a scheduled opening, it stays exit-only until its own deadline; close it before a separate scheduled run, and never double-count overlapping heartbeat/pool opportunities. A campaign has one writer and one active invocation. Missing scheduled coverage remains missing. UTC boundaries persisted at init govern DST; never assume every night is ten elapsed hours.

### 11.7 Offline calendar reconciliation

Implement `python -m desk reconcile-calendar --campaign campaign-001`. This is a local writer operation requiring both existing campaign locks, integrity verification and idempotency. It uses no provider, clock-health probe or portfolio capital creation. Sample invocation UTC once; reconcile only sessions whose frozen closing boundary has elapsed. Study/embargo close at 06:00; prospective close at 06:15. Future dates remain untouched. All writer-capable startup paths perform the same reconciliation before current-session work.

For an entirely unlaunched elapsed session, append MISSED_SESSION with its frozen boundaries, missing heartbeat/discovery coverage, durable watch-derived denominators and unavailable scheduled equity values. For an interrupted session, retain actual observations and append incomplete closure at its scheduled boundary with `recorded_at` equal to reconciliation time. Neither event claims it was committed on time. Do not backdate event timestamps, generate heartbeats, fabricate opening/closing equity or infer exits. Existing unclosed positions and paid fees persist. Surviving pending orders are canceled under the existing restart/restore rules at actual reconciliation time, never treated as fills inside the missed interval.

Create a report cutoff for each reconciled session with economic as-of boundary and explicit `valuation_unavailable`/late-reconciliation status. Its input selection uses that session's evidence and event ownership, not every later financial event merely because it precedes the new cutoff sequence. The reducer selects the historical boundary state then attaches the reconciliation metadata. Later cancellation fees are already paid historical fees; new economic effects outside the interval belong to the bridge. Record both `economic_as_of` and `cutoff_recorded_at`; this is an explicit exception to treating all cutoff-event timestamps as economic as-of time in §14.3. Such sessions never qualify for the uncertainty interval.

Repeated reconciliation with no newly elapsed/incomplete dates makes no changes. It never replaces an existing finalized cutoff/report. A report request lacking a cutoff continues to return NO_REPORT_CUTOFF, code 3, with the exact reconcile-calendar command in its diagnostic; report itself remains read-only. After the last scheduled close, the operator runs reconcile-calendar, study-evaluate if due, verify and campaign report. No additional night or automatic extension is introduced. A collection block must not prevent truthful local closure/reporting of the failed campaign.

## 12. Storage, schema, idempotency and crash recovery

Use Python stdlib SQLite; WAL mode, `synchronous=FULL`, `foreign_keys=ON`, `busy_timeout=5000`. SQLite documents the stronger WAL durability behavior of FULL [R12]. One application process owns writes; hold both registry-identity and data-root OS flock locks for the whole writer invocation, acquiring registry first. A second writer exits with code 4. Reports use consistent read snapshots. No DuckDB or external message broker is needed in v1.

Raw responses: redacted body bytes in content-addressed files `raw/<sha256>.json.gz` (gzip mtime=0); store uncompressed content hash and separate receipt metadata. Write temporary file, fsync, atomic rename, then commit its database reference. Orphaned files are harmless; a missing referenced payload is an integrity failure. Secrets must be removed before hashing; preserve original public market fields.

Required tables (PKs and constraints are normative):

| Table | Required columns beyond common created_at/event_seq |
|---|---|
| schema_migrations | version PK, SQL hash, applied_at |
| campaigns | campaign_id PK, blueprint/config/contracts/dependency/code hashes, start date, preregistration hash, status |
| sessions | session_id PK, campaign FK, scheduled UTC boundaries, actual start/stop, mode, status, start equity per portfolio |
| observations | observation_id PK, provider, request ID, received time, context slot, payload hash, parser version, quality, error code |
| pool_snapshots | snapshot_id PK, observation FK, pool ID, raw account refs, normalized reserve/fee/mint fields, available_seq, quality |
| candidates | mint ID PK per campaign, first seen, retirement, watch status, source observation |
| gate_results | decision ID, rule ID, portfolio, input refs, value, threshold, status, reason; composite unique decision+rule |
| bars | campaign,pool,minute composite PK, price decimal string, evidence refs, quality |
| signals | signal_id PK, hypothesis, portfolio, minute, mint,pool, inputs, rank, expiry, outcome |
| orders | order_id PK, idempotency_key UNIQUE, portfolio, position ID nullable, side, integer-string amount, reference, min_out, state, deadlines, reason |
| fills | fill_id PK, order_id UNIQUE FK, snapshot FK, atomic input/output/fee, impairment, fill time |
| positions | position_id PK, portfolio,mint,pool, quantity, cost basis, state, entry time, high-water mark, trailing flag, first exit reason |
| ledger_entries | entry_id PK, event FK, portfolio, account, asset, signed atomic delta, reason |
| events | event_seq INTEGER PRIMARY KEY, event_id UNIQUE, type, entity, UTC time, canonical JSON payload, previous_hash, event_hash |
| reports | report_id PK, session/campaign, cutoff_seq, snapshot hash, output hashes, schema version |

Quality enums are `VALID, UNKNOWN, CONFLICT, STALE, UNSUPPORTED, INVALID`. Unavailable numeric fields are SQL NULL with a reason; never NaN, infinity or zero substitution except the expressly labeled conservative valuation.

Order states: `PROPOSED → REJECTED` or `SUBMITTED → FILLED|FAILED|CANCELED`. Position states: `OPEN → EXIT_PENDING → CLOSED`; `EXIT_PENDING → OPEN_EXIT_BLOCKED → EXIT_PENDING` on recovery; no direct blocked-to-closed transition without a fill. Failed sells remain EXIT_PENDING until retry/window expiry. Every terminal order outcome is immutable. Session states: `CREATED → RECOVERING → STUDY|PAPER|NO_TRADE → LIQUIDATING → CLOSED|CLOSED_WITH_OPEN_EXPOSURE`, with `ABORTED_INTEGRITY` reachable on failure. A killed process retains its last state until recovery.

Deterministic IDs: SHA-256 of canonical JSON arrays. Signal ID fields: campaign, portfolio, mint, pool, UTC minute, strategy version. Buy idempotency key: signal ID+`BUY`. Position ID: successful buy order ID. Sell key: position ID+`SELL`+durably incremented attempt number. Duplicate input replay must return the existing order, never re-debit fees. Observation IDs include request ID and payload hash so identical content at different receipts retains timing.

In one `BEGIN IMMEDIATE` transaction append outcome event, insert fill if applicable, write ledger deltas, update projections and release reservations. Acknowledge only after commit. On startup: lock, `integrity_check`, verify hash chain and input references, rebuild projections into temporary tables, compare with stored balances/positions, then reconcile. Mismatch yields read-only `ABORTED_INTEGRITY`; never auto-repair money history. A submitted order surviving a process outage is canceled with reason `RESTART_GAP`, retaining any recorded fee; do not fabricate missed fills. Live application restart uses current fresh data; offline replay reproduces recorded historical processing, not that recovery rule at arbitrary replay boundaries.

### 12.1 Schema and evidence invariants [D]

Use STRICT SQLite tables (TEXT amounts; INTEGER timestamps/flags) with explicit NOT NULL except declared nullable fields. `ledger_entries` primary key is `(event_seq, leg_index)` with FK to events; entry_id is additionally UNIQUE. For each economic event and asset, signed ledger legs sum to zero using Python integer arithmetic. Funding transfers from a virtual funding counterparty, buys exchange cash/target with virtual pool counterparties, sells reverse those legs, and fee charges pair cash with a same-asset fee counterparty. Cost basis and realized-P&L attribution are projections, never additional cash-transfer legs. Financial aggregation and amount ordering occur in Python integers; SQL SUM/CAST on amount TEXT is forbidden because SQLite may coerce to approximate or overflowing numeric types [R17].

Include explicit `portfolios`, `reservations`, `watch_events`, `timer_events`, `health_events` and `commands` tables. Their primary keys are respectively portfolio_id within campaign, order_id, event_seq, timer_id, event_seq, command_nonce. Foreign-key portfolio ownership for all money/order rows. Add partial UNIQUE indexes for one active BUY per portfolio+mint, one active SELL per position, and one unclosed position per portfolio+mint. Application checks plus transactionally updated reservation rows enforce aggregate caps. Monetary amounts use grammar `0|-?[1-9][0-9]*`, with field-specific nonnegative/u64 restrictions. A CHECK on `typeof(amount)='text'` and an application grammar/range check are both required. Store full transition/reservation/fee attribution in event payloads so replay can rebuild all projections.

Hash-chain serialization is UTF-8 canonical JSON. Compute event_hash over the canonical object including previous_hash and excluding event_hash; do not also concatenate previous_hash outside that object. Hash registries identify exact ordered source files and migrations; manifests never include their own hash. Definition-of-done requires schema tests for each UNIQUE/FK/CHECK invariant. No table is a license to make hidden trading policy decisions.

Raw rename is followed by parent-directory fsync before its database reference commits. Content-address hash is over sanitized uncompressed bytes; verify gzip integrity and uncompressed hash on replay. No reference to a mutable external URL substitutes for payload bytes. Reports and backups use temporary paths plus atomic rename; reports do not write operational events, so readers remain read-only. The writer persists report cutoff metadata before export; failed export can be retried from that cutoff without changing decisions.

### 12.2 Canonical bytes and identifiers

Define encoder DESK_JSON_V1 for every config/event/ID/hash manifest: UTF-8, no BOM, json.dumps(sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False), no trailing newline in hashed bytes. All object keys are strings; permitted values are null, bool, signed integers, strings, lists and objects. Floating-point and Decimal objects are forbidden. Financial decimals are canonical strings, amounts follow §12.1, times are integer UTC microseconds. Reject unpaired surrogates, duplicate object keys and nonfinite literals on decode. Preserve string code points without Unicode normalization. Operational names/identifiers are ASCII; arbitrary provider text is not an identifier. These choices are a project format, not a claim of RFC 8785 compliance. Python defaults alone accept duplicate keys/nonfinite numbers [R29].

Genesis previous_hash is 64 ASCII zeroes. SHA-256 output is lowercase hexadecimal. Event payload timestamps, receipt IDs and timer IDs are replay inputs, not regenerated system-clock values. Random IDs/UUIDs are forbidden in deterministic projections. Request ID is a campaign-local monotonically increasing integer allocated durably before dispatch; gaps are valid after a crash. No request ID reuse.

Raw sanitized response bytes keep original JSON spacing and number lexemes; never round-trip them through DESK_JSON_V1 before hashing. Thus raw hash and normalized semantic hash serve different purposes. Raw bodies are untrusted source data, not canonical event JSON. Canonical report JSON uses the same encoder plus one final LF for the exported file; report file hash includes that LF. A registry distinguishes value_hash (no LF) and file_sha256 (actual bytes). Markdown/CSV exports also end in exactly one LF. Report receipts include nondeterministic export time outside the deterministic report bytes.

### 12.3 Trial registry and backup restoration

Maintain a local append-only trial registry under the default desk root, separately from campaign databases. Serialize updates with its own flock, then atomically replace/fsync its JSON file using DESK_JSON_V1. Register campaign ID, absolute resolved data root, init UTC, preregistration/code hashes, frozen dates and final report status. Init registers before any funding; idempotent retry completes a partially initialized campaign exactly once. Registry failure prevents new campaign init, not risk-reducing recovery of existing exposure. Alternative data roots still register in the default registry. Include registry export in campaign summaries and backups. Never scan unrelated user directories.

This registry cannot discover deleted/exported campaigns or trials on other machines. Reports state local_registry_only and disclose known external trials supplied by the operator; they never claim global completeness. No telemetry or external publication is introduced.

Implement target CLI command `python -m desk restore --backup MANIFEST --destination NEW_LINUX_DIRECTORY`. Restore only into an empty/new destination, verify database integrity/event chain/raw hashes and label RESTORED_AT_CUTOFF. Never merge it into a newer original campaign. Preserve original campaign identity; funding is not repeated. Restored run acquires that campaign's writer lock and requires explicit data-root selection; simultaneous original/restored writers for the same registry identity are refused on that host. Recovery cancels submitted orders with RESTORE_GAP, retaining fees, and applies the usual fresh-evidence/recovery gates. Time after backup cutoff is an irrecoverable evidence gap unless original verified records are separately available; do not reconstruct it from provider history. Do not claim same-disk backups provide disaster recovery or prevent cross-machine duplication.

### 12.4 Persistence failure and process locks

If raw fsync, directory fsync, evidence insert, ledger commit, witness commit or required checkpoint fails, stop dispatch and decision advancement immediately. Do not retry economic transitions against guessed commit outcomes. Emit a bounded redacted stderr diagnostic, exit 5, and leave locks to OS release on process exit. Network tasks may be canceled; no new simulated fee/fill is acknowledged. An uncommitted halt cannot be claimed durable.

Next startup first performs SQLite integrity/foreign-key checks, event-chain/raw hash verification and event-derived projection reconciliation. Resolve commit outcome from durable records/idempotency keys; never from an earlier UI acknowledgment. Missing referenced evidence fails integrity. Unreferenced raw objects remain harmless and are not counted as observations. No emergency “sell without persistence” exists in this paper system.

Use two lock scopes: a registry identity lock keyed by campaign ID held across original/restored data roots, plus the data-root writer lock. Acquire registry first, data-root second; release on any acquisition failure. Read-only reports need neither writer lock. Migrations require both. The registry path and ownership follow §12.3; inability to open it blocks provider operation rather than creating a second registry silently. Across machines there is no distributed exclusion guarantee. No external lock service is introduced.

### 12.5 Recorded replay and audit recomputation

Expose the following offline operations through `replay` options, defaulting to `--kind recorded`; no network, funding, clock probe or new economic event is allowed in either mode.

| Mode | Authoritative inputs | Required outcome |
|---|---|---|
| recorded | Persisted events, availability witnesses, timers, historical gate results and frozen contract hashes | Pure reduction to the same cutoff state and report bytes |
| audit | The same ordered evidence plus pinned historical decoder/rules/environment | Recompute validation, quotes, gates and proposed transitions; compare to recorded results |

Recorded reduction applies historical transition facts; it must not use today's provider permission, current clock, current deployment or export time to retroactively permit/reject a fill. Audit recomputation uses the health state and permission evidence actually valid at the recorded decision sequence and recorded actual processing time. A snapshot used for a historical boundary must satisfy that boundary's state and availability rules, not later state. Both modes enforce evidence hashes, event-chain integrity and pinned contract identity. A violated recorded invariant is an integrity failure, never an instruction to silently repair the financial record.

Persist each decision's actual processing time, runtime generation/clock epoch, health evidence IDs/expiry anchors, membership state reference, gate-input evidence IDs, result/reason and applicable rule hash. Existing event payloads may hold these fields; a new SQL table is not required. Replay must not depend on mutable gate/health caches outside the cutoff. Audit with missing pinned code/dependencies/reference evidence returns AUDIT_DEPENDENCY_UNAVAILABLE, code 3; recorded reduction remains possible when its own pinned reducer/contracts/evidence are available. A reproducible disagreement is REPLAY_DIVERGENCE, code 5; emit expected/observed event and rule IDs without changing history.

Dependency changes require explicit historical validation as §14.3 requires. No migration may claim old reports are byte-identical unless checked. Replay segmentation and restart of the replay process do not create live RESTART_GAP cancellations.

## 13. Interfaces, configuration and repository deliverables

Implement a single Python package with typed dataclasses, explicit Decimal construction from strings, and pure functions for validation/features/curve/risk. Use stdlib asyncio, sqlite3, tomllib, argparse, zoneinfo, hashlib and gzip; use `httpx` for HTTP and `solders` only for public-key/PDA utilities. Do not import signer/keypair functions. Development dependencies: pytest, hypothesis, ruff. No LLM dependency or model API key is needed. Choose compatible patch versions during build, freeze exact versions/hashes in `requirements.lock` and `requirements-dev.lock`, verify clean Python 3.12 installation; do not invent tested versions in advance.

Required layout:

- `src/desk/{__main__,cli,config,clock,models,collector,normalize,chain_checks,features,strategy,risk,execution,positions,store,replay,study,reports}.py`
- `src/desk/providers/{dexscreener,solana_rpc}.py`; `src/desk/pools/raydium_cpmm.py`
- `contracts/{DATA_CONTRACT,CHAIN_SECURITY,STRATEGY_SPEC,RISK_SPEC,EXECUTION_MODEL,STATE_MACHINE,ACCEPTANCE_TESTS}.md`, derived from corresponding sections here; no conflicting copies.
- `contracts/program-lock.json`, `contracts/provider-contract.json`, `config/{paper.toml,decisions.json}`, `sql/001_initial.sql`, `tests/{unit,integration,fixtures}`, `README.md`, `AGENTS.md`, `DECISIONS.md`, `CHANGELOG.md`, dependency files.

Interface contracts:

| Function | Input → output; side effects |
|---|---|
| collect(request, clock) | request descriptor → RawObservation; network only, no ledger writes |
| normalize(raw, parser_lock) | raw bytes/metadata → typed observation or explicit error; pure |
| decode_bundle(raw_accounts, program_lock) | account bundle → PoolSnapshot or Unsupported/Invalid; pure |
| evaluate_gates(snapshot, history, config) | evidence → ordered GateResult list; pure |
| generate_signals(bars, eligible, minute, config) | frozen data → sorted Signal list; pure |
| risk_check(proposal, portfolio, session, evidence) | proposal → Accept(reservations) or Reject(reason); pure |
| quote(snapshot, side, amount, scenario) | exact units → quote with fees/impact/output or error; pure |
| advance_order(order, event, state) | state/event → proposed event/deltas; pure |
| commit_transition(expected_seq, transition) | one atomic transaction; only writer performs it |
| build_report(snapshot) | frozen rows+contract hashes → deterministic JSON/Markdown/CSV; no network |

All configuration keys must be schema-validated; unknown keys fail. `mode` accepts `study|paper|replay|recover-only`; any live mode fails. Reject signing/key/wallet fields, negative budgets, invalid timestamps, unsupported identifiers, and changes to registered experiment parameters after campaign creation. Config file names do not imply approval; compare hashes to campaign manifest. Secret-like configuration values are never echoed in errors.

The following is the authoritative core configuration; less central constants are fixed by the section rules and must be included in the emitted resolved configuration manifest. No hidden execution defaults:

```toml
schema_version = 1
blueprint_version = "2.6"
mode = "study"
timezone = "America/Detroit"
chain = "solana:mainnet-beta"
starting_capital_usdc = "10000"
paid_provider_budget_usd = "0"
pool_family = "raydium_cpmm_zero_creator_fee"
commitment = "finalized"
discovery_seconds = 60
poll_seconds = 5
max_watched_mints = 8
max_positions = 3
max_buy_usdc = "100"
min_buy_usdc = "10"
max_entry_cost_exposure_usdc = "300"
max_position_equity_fraction = "0.01"
max_input_reserve_fraction = "0.001"
min_quote_reserve_usdc = "20000"
max_price_impact_fraction = "0.01"
max_round_trip_loss_fraction = "0.02"
stop_loss_fraction = "0.06"
trailing_activation_fraction = "0.12"
trailing_drawdown_fraction = "0.05"
session_loss_fraction = "0.02"
max_hold_minutes = 120
signal_expiry_seconds = 30
fill_wait_seconds = 20
slippage_tolerance_fraction = "0.02"
study_sessions = 14
embargo_sessions = 1
prospective_sessions = 28
random_seed = 20261106
```

Campaign manifest additionally freezes session dates, all scenarios, source/decoder/dependency hashes, program hash, discovery algorithm, report schema, and the machine-readable decisions. Serialize JSON with sorted keys, UTF-8, no insignificant spaces, integer strings for amounts, no nonfinite numbers. Decimal strings use normalized fixed-point formatting with `-0` normalized to `0`. SHA-256 over canonical bytes supplies manifest/evidence hashes. Each event hash covers the canonical event object including previous_hash and excluding event_hash; previous_hash is not concatenated a second time; the first previous_hash is 64 ASCII zeroes. Stable event IDs hash campaign ID, event type, entity ID and its durable transition ordinal. Newly requested campaigns use the CLI campaign ID; duplicate IDs resolve existing campaigns and never reset them. Reject dirty source for prospective experiments; offline development/replay may record dirty diff hash.

### 13.1 Executable contracts and reproducibility

Literal absence of every coding choice is neither feasible nor useful. Schema column spelling, dataclass decomposition and compatible dependency patch selection are implementation choices; economic, experiment and failure semantics are fixed here. Complete the executable contracts BEFORE runtime implementation: migration SQL; typed request/result/error dataclasses; machine-readable configuration schema with every resolved constant; transition tables; and report schema/version with exact column lists and sort orders. A schema that cannot represent any acceptance fixture fails this phase. Do not ask the owner to choose SQL column names.

Avoid circular hashes: freeze design/source/dependency/decoder/config manifests at init; exclude runtime data, reports, the manifest's own bytes and derived hashes from those source hashes. Store a code tree hash from tracked implementation files excluding runtime outputs, plus clean Git commit when available. Campaign init requires a version-controlled source tree for provider experiments; offline fixture mode may use an explicit directory tree hash. Read-only diagnostic preflight never creates portfolio capital. Source/deployment capture is a build/preflight activity completed before campaign init; no mutable 'latest' decoder inside a campaign. Unknown config keys are errors; run-mode CLI is an operational phase selector checked against the manifest and must not mutate its registered config hash.

Preserve and extend stable requirement IDs as defined in §22. Traceability must cover every active section of this consolidated blueprint, not only rows with preexisting IDs. Enforce per-field nullability, signed/unsigned amount grammar, enum domains and composite campaign ownership in executable tests. Table migrations and exact dependency locks are outputs of implementation, not fabricated completed artifacts of this document revision.

### 13.2 Active contracts and compilation

Before runtime implementation, author and review executable contracts: migration SQL; typed request/result/error dataclasses; configuration schema with every resolved constant; state transition tables; report schema with exact columns and sort orders; and `contracts/ACTIVE_RULES.json`. Complete schemas must represent every acceptance fixture.

ACTIVE_RULES.json is the navigable index generated from explicitly authored contract records, not inferred from prose. Each active atomic requirement has one definition, stable ID, current and original source sections, supersedes links, units, predicates, time endpoints, null behavior, error code and test links. It cannot override this blueprint. Contract checks reject duplicate active IDs, undefined decision/test references, inconsistent blueprint versions, conflicting constants and missing rule coverage with CONTRACT_CONFLICT. Do not silently discard inconvenient requirements; record an exact conflict and block dependent work while continuing independent modules.

The active blueprint_version is 2.6; schema_version remains 1 unless implementation actually changes that schema. Freeze OD-001–OD-049 and every existing acceptance ID. Historical prefixes identify provenance only. Before dependent runtime code, deliver queue admission transitions, generation/health state machine, retirement ordering, replay modes, calendar reconciliation, and reference-harness provenance contracts and fixtures.

Complete contracts, offline end-to-end accounting/replay/reporting and fault injection before gated host/provider operation. Reference acquisition may proceed independently. A network-dependent stub is not complete paper trading, and profitability is not an engineering prerequisite.

## 14. Reports and statistical interpretation

Produce immutable Markdown, JSON and CSV for every session, including missed/no-trade sessions, plus a campaign report. Use frozen `cutoff_seq`; generation wall time belongs in a separate receipt, not the reproducible content. Re-running the same snapshot produces byte-identical files. Later recovery produces a separately versioned supplement; never rewrite a finalized morning report.

Include: campaign/session IDs and schedule; code/config/source/data hashes; discovery cohort definition; all exclusions and missing denominators; provider coverage, request latency percentiles, context-block age and conflicts; valid/invalid opportunity counts; exact filter rejection counts; all order outcomes/fees; open quantities and blocked exits; realized/unrealized/conservative P&L; null market valuations and last-known ages; maximum drawdown; turnover; exposure; scenario comparisons; clock/outage intervals; all operator interventions; first and last evidence sequence; and limitations.

Definitions:

- Return = (ending conservative equity − initial campaign capital) / initial capital. Session return uses session starting equity; zero/nonpositive denominator → null.
- Drawdown = max over minute conservative equity of `(running_peak-equity)/running_peak`, peak initialized at campaign capital. Missing market marks use the explicit conservative treatment and are flagged.
- Turnover = sum of buy notional and gross sell proceeds / initial capital.
- Exposure = minute original-entry-cost outstanding / initial capital; report mean and maximum.
- Request-latency quantiles use sorted durations and nearest-rank `ceil(q*n)-1`; empty sample → null.
- Quote failure, exit failure and rejection rates each name their own attempted/scheduled denominator. Do not label unsupported discovery objects as failed trades.

Primary comparative statistic is mean daily H2-primary return minus H0 return across **all 28 scheduled sessions**; mark missed-session values as unavailable, not zero performance. Provide an uncertainty interval only if all 28 are observed, there are at least 30 closed H2-primary positions across ten target mints, and no final blocked inventory or unresolved integrity defect remains. These are minimum reporting safeguards, not sufficient power or proof of representativeness. Otherwise output `INSUFFICIENT_EVIDENCE` and descriptive results.

When permitted, compute a paired stationary bootstrap of session returns with geometric block length mean 3, 10,000 replications, seed 20261106, wrapping indices. Resample all strategy/scenario columns with identical session indices to retain shared-market dependence. For reproducibility use Python `random.Random(seed)`; each replicate starts with `randrange(n)`, at each following draw restart with probability 1/3 using `randrange(n)`, otherwise increment index modulo n. Use 2.5th/97.5th percentile endpoints via nearest-rank. Dependence-preserving resampling is motivated by Politis and Romano [R13]; its stationarity/weak-dependence assumptions may fail in crypto. Label intervals exploratory and report that limitation. Do not resample trades as independent observations.

No automated p-value, annualized Sharpe, “95% probability of profit,” strategy winner selection, or multiple-scenario significance claim is implemented. Keep H1/scenarios descriptive. Even a positive interval is not a live-trading approval or a proven edge. Research on multiple trials and nonnormal returns explains why uncorrected attractive performance summaries can mislead [R9]. Record all campaigns and code/config changes; never hide failed trials.

Report every campaign, including failed feasibility, all attempted trials and parameter changes, cohort/coverage and final blocked inventory. No causal interpretation of H1 or market-wide representativeness is permitted. A later campaign does not erase an earlier result. The minimum sample gates are not a power calculation.

### 14.1 Reporting boundaries, completeness and serialization [D]

Snapshot each session's opening equity before new actions and its phase-specific closing equity (06:00 study/embargo; 06:15 prospective), and a separately labeled off-session cash/valuation bridge. A late launch has unknown scheduled opening equity unless a durable exact-boundary snapshot exists; do not replace it with launch equity for statistical returns. Launch equity still defines that session's operational loss control and is labeled ACTUAL_LAUNCH_BASELINE. Partial-session performance is descriptive. Recover-only fees and carried-inventory changes between scheduled sessions appear in the bridge; campaign P&L always uses the complete ledger, even where nightly returns cannot be computed. Do not claim nightly returns necessarily compound to campaign return when off-session bridges exist.

An observed session for interval eligibility requires an on-time opening and final snapshot, at least ninety-five-percent heartbeat and valid bundle coverage, no unknown marks on any minute with exposure, no incomplete financial transitions, and no carryover or off-session economic bridge for H2-primary. Zero bundle denominator does not qualify. All twenty-eight H2-primary session returns must be present; never remove a bad or missing night. For H1/other scenarios, suppress only their interval/paired comparison if columns are missing; this does not silently discard H2-primary's otherwise valid main interval. Primary bootstrap statistic is arithmetic mean of sampled `(H2-primary session return − H0 session return)`; retain exactly twenty-eight sampled indices per replication and nearest-rank percentiles as §14 defines. Do not take a bootstrap of compounded terminal wealth instead.

Money/quantity JSON and CSV preserve exact atomic strings; human USDC values use six decimals, prices twelve significant decimal digits, returns/ratios six decimal places, percentages four decimal places, all HALF_EVEN display rounding. Scientific notation is forbidden in canonical financial output. CSV is UTF-8 with LF, standard quote escaping and deterministic declared column/row order (event_seq, leg_index where applicable). Prefix provider-supplied strings beginning `=`, `+`, `-`, `@`, tab or CR with an apostrophe only in presentation CSV; never alter canonical source/financial values. Escape provider text in Markdown/HTML contexts; do not emit provider-supplied active links.

### 14.2 Cutoffs, export ownership and backup snapshots

The writer commits session/campaign cutoff records at lifecycle boundaries. The standalone report command reads the latest existing cutoff for the requested session, exports deterministically outside the writer, and writes only output files and a separate export receipt; it never appends operational events or inserts report rows. For an active session, use its most recent persisted minute cutoff and label the export PROVISIONAL; no cutoff means NO_REPORT_CUTOFF, exit 3. At session close the writer's cutoff row records report schema and input hashes; exporter receipts contain resulting output hashes. Distinguish cutoff metadata from export receipt so no future output hash is needed to commit the cutoff. Failed exports can be retried byte-identically.

Backups while a writer is active use SQLite's online backup API for a consistent snapshot, then read cutoff_seq from THAT snapshot and enumerate raw references from THAT snapshot, not from live tables afterward. A backup never writes money events. Hold the campaign lock for migrations and recovery; do not require an exclusive writer lock for ordinary read-only reports. Periodic health/watch/mark state used by reports must be derivable from events through cutoff_seq. A hash chain detects accidental/inconsistent edits, not malicious rewriting by someone with full disk access; no external notarization is claimed.

### 14.3 Historical cutoff reconstruction

A SQLite read transaction freezes the database at the time that read starts; it does not restore old mutable rows to a historical cutoff [R35]. Therefore a report for cutoff K must not directly export current positions/balances/health and merely filter events to K.

Build a pure reducer from immutable events <=K, pinned contracts and referenced evidence. Reconstruct all report-relevant state: portfolio cash, reservations, inventory, position status/basis/high-water, fees, marks and freshness, latches, watch membership, denominators, timers, study results and intervention history. Alternatively use a verified checkpoint at sequence J<=K followed by events J+1..K. Checkpoint contains complete state, schema/reducer version and hash; changing reducer version requires an explicit migration/revalidation, never silent rewriting of historical report output.

The report's logical as-of time is its recorded economic_as_of, not export wall time. Ordinary cutoffs use the cutoff event time; late calendar reconciliation explicitly records the original boundary separately from cutoff_recorded_at as defined in §11.7. Mark age and freshness are evaluated there. Final reports retain their original code/report-schema/contract hashes. `verify` compares event-derived current projections with operational caches; any mismatch is INTEGRITY_PROJECTION_MISMATCH, exit 5. Exact cached report output may be reused only after validating its input/schema hashes.

Acceptance example: export a cutoff with one open position; later close it and charge a fee. Re-export the old cutoff: it still has the old open inventory/cash/mark and identical bytes. A new recovery supplement contains the close. Merely opening a new read transaction after the close cannot pass this test.

## 15. WSL operations and resource budget

Reference host: Windows 11 with WSL2 Ubuntu 24.04 LTS and Python 3.12. Use a project `.venv`; no global pip installs. Project/runtime data live on Linux ext4, not `/mnt/c`. Runtime root is `~/.local/share/solana-desk/<campaign_id>`, mode 0700; files 0600. Use environment variable `DESK_DATA_DIR` only for an explicit alternative Linux path. Never repurpose HOME or CODEX_HOME.

Preflight records WSL version/distro, Python/SQLite version, free disk, available memory, synchronized clock status, DNS/TLS reachability, RPC genesis hash/mainnet validation, account/layout compatibility, local write/fsync and DB transaction tests. Minimum available disk 10 GiB and memory 2 GiB. Do not claim host readiness from this document's execution environment. If Ubuntu/Python differs, issue `UNSUPPORTED_RUNTIME` with exact mismatch; fixture development may proceed, but that host cannot pass the specified acceptance gate.

v1 runs in a foreground WSL terminal. Operator must keep Windows awake and the terminal/session available; no sleep/reboot resilience guarantee. Do not modify Windows power policy, install scheduled tasks, enable systemd, or auto-launch after boot. WSL supports systemd [R14], but availability alone does not solve host sleep or startup. Unattended deployment is explicitly excluded from this release. Application handles loss of connectivity, abrupt termination and resumption as outages, not continuous observation.

Commands to implement (these are target application commands, not claims of existing executable code):

```bash
python -m desk preflight --config config/paper.toml
python -m desk init --config config/paper.toml --campaign campaign-001
python -m desk run --campaign campaign-001 --mode study
python -m desk study-evaluate --campaign campaign-001
python -m desk run --campaign campaign-001 --mode paper
python -m desk stop --campaign campaign-001
python -m desk recover --campaign campaign-001 --exit-only --minutes 15
python -m desk report --campaign campaign-001 --session latest
python -m desk replay --fixture tests/fixtures/integrated_session --kind recorded
python -m desk replay --fixture tests/fixtures/integrated_session --kind audit
python -m desk reconcile-calendar --campaign campaign-001
python -m desk verify --campaign campaign-001
python -m desk backup --campaign campaign-001
python -m desk restore --backup MANIFEST --destination NEW_LINUX_DIRECTORY
```

`stop` writes an atomic local command file containing campaign ID, nonce and `STOP`; the running writer consumes it within one poll, persists acknowledgment, cancels entries, and enters a 15-minute liquidation window capped at the scheduled final boundary. SIGINT has the same behavior; a second SIGINT exits after committing a checkpoint with unclosed positions preserved. `report` resolves `latest` deterministically by scheduled session date. `run --mode paper` consults the study result; H0 selection creates a no-trade observational session, not a fake study pass. Only `init` creates capital, once per portfolio/campaign; repeated init returns existing identity.

Exit codes: 0 command succeeded (including legitimate NO_TRADE); 2 configuration/argument failure; 3 preflight/provider/data gate blocked; 4 writer already running; 5 integrity failure; 6 acceptance test failure. JSON status always disambiguates successful command execution from experiment success.

Runtime limits: bounded queue 1,000 observations, memory target ≤1 GiB, total campaign data budget 20 GiB INCLUDING raw data, database/WAL, reports, diagnostics and local backup snapshots. Apply the item/byte admission and transient buy-block rules in §15.1; overload records identify unadmitted requests/opportunities, with no committed-event eviction. Never silently drop committed evidence or money events. Disk free <5 GiB or campaign data >18 GiB halts entries, attempts bounded exits and snapshots; at <1 GiB stop network ingestion and orderly terminate after final persistence. If persistence itself fails, stop all simulation immediately; stderr/local status reports failure, and restart integrity checks decide whether data are recoverable. Do not pretend an uncommitted halt is durable.

Keep raw inputs, ledger, contracts and experiment reports for the entire campaign plus 90 days; never auto-delete within that window. Rotate diagnostic logs at 10 MiB × five files. If retention would exceed disk budget, stop with `STORAGE_BUDGET_EXCEEDED`, not selective evidence deletion. Create one backup at each session close and before explicit migration; keep the latest seven completed backup manifests/DB snapshots using SQLite's backup API [R15]. Raw content objects are immutable and shared by hash across these local backups rather than copied seven times. Each manifest contains its cutoff sequence and complete raw hash set; verify referenced objects and restore to a new path. This is transaction/recovery protection on the same disk, not an independent raw-data copy. Do not delete any raw object within retention even if an older backup is removed. Count all snapshots against the total budget. Never copy only a live `.db` file and omit its WAL. Local backups do not protect against Windows disk/WSL distro loss; record that limitation. Off-host backup is outside v1.

### 15.1 Byte admission, nonblocking queues and overload

Python asyncio Queue maxsize bounds item count and `await put` can wait when full [R37]. Neither property supplies a byte budget or permission to stall the single writer. The observation item cap is 1,000. Use a shared **64 MiB uncompressed body budget** for responses being streamed, queued, parsed or prepared for persistence. Reserve 10 MiB before dispatch for each active response; after receipt replace that reservation with its actual uncompressed byte length. Keep that reservation until preparation has released the body. Count a shared body once, even when several pool bundles reference it; do not duplicate whole body buffers per pool. Wire and decompressed stream limits remain §4.5.

A dispatch without sufficient byte capacity remains undispatched; record RESOURCE_BACKPRESSURE against its intended opportunity, never wait holding writer ownership. The single RPC request and single DEX request can each reserve capacity independently. Only one body-normalization/preparation job runs at a time; other bodies wait within the byte/item budgets. Pending semantic bundle work retains compact IDs and decoded required fields, not extra raw-body copies. Parsing errors, MemoryError and abnormal preparation termination produce explicit failed observations; if process integrity is uncertain terminate under §12.4. No financial transition may continue after a persistence failure.

Suspend discovery dispatch when either item occupancy or body-byte occupancy reaches 80% (compare integers; equality suspends). At the item cap or inability to admit a required response, block new buys with RESOURCE_BACKPRESSURE, retaining exits and health/deadline processing. Once both occupancies are below 80%, discovery and the transient buy block may resume subject to all ordinary gates; this never clears session/permanent latches. Avoid `await queue.put` in the scheduler/writer. Use explicit capacity admission and nonblocking enqueue; QueueFull means an auditable overload outcome, not silent eviction. No committed event, money transition or command acknowledgment can be evicted.

The 64 MiB figure bounds body storage, not total Python process memory. Retain §15's ≤1 GiB memory target and measure peak resident memory with a representative maximum-bundle synthetic run, including parsing, reducer and export. Failure to meet it blocks the resource acceptance gate; do not claim a formal heap bound or relax the limits. Run report exports separately as already required. Resource pressure causes missing coverage; it cannot create historical retries or preferentially omit losing trades.

## 16. Implementation sequence and phase outputs

1. **Contracts and scaffold:** create decision/config schemas, module interfaces, threat model, manifests and CLI. Inspect existing repo and user changes first; do not overwrite unrelated work. No provider access needed.
2. **Ledger and deterministic replay:** implement canonical events, amounts, reservations, state machines, raw evidence and crash-safe transactions. Complete synthetic integrated session before adapters.
3. **Provider/decoder:** implement discovery sampling, strict RPC allowlist, time/quality handling, pinned CPMM subset and captured account fixtures. Failed compatibility yields explicit blocked status.
4. **Execution/risk:** implement quotes, delayed fills, fee expenses, exits, marks, session scheduling and restart. No signal can bypass risk.
5. **Strategy/reports:** implement H0/H1/H2, independent scenarios, reconciliation, statistical gating and deterministic reports. All can be tested offline.
6. **Host/integration validation:** run actual WSL preflight, recovery/failure checks and read-only smoke collection. Record each environment-specific result. No study pass is inferred from a smoke test.
7. **Study and prospective operation:** run prescribed calendar schedule and freeze outputs. Feasibility failure is a valid research result; never claim 28-session completion before elapsed observations exist.

Codex/other implementing agents are development and inspection tools, not runtime components. The application must run without them. Repository `AGENTS.md` must enforce paper-only, no wallet/signing code, scoped changes, preserved user edits, no unrecorded policy changes, and truthful verification. Do not add a Codex daemon or depend on an LLM to remember stops. No external issue/PR/publication is required by this specification.

## 17. Acceptance tests and exact completion labels

Implement tests below; checking filenames alone never passes a phase. Record command, timestamp, environment, exit code, captured result hash and tested commit in `ACCEPTANCE_TESTS.md` plus `acceptance.json`. Money and state equality tolerance is **zero atomic units**. Decimal outputs compare canonical strings; derived report percentages allow no mismatch after prescribed display rounding. Performance metrics must not weaken financial correctness.

| Gate | Required test/evidence |
|---|---|
| Contract/config | Parse every default; reject unknown/live/signing fields, invalid IDs, changed campaign hashes and negative limits; every OD mapped to active choice/exclusion |
| Curve | Golden pinned-reference outputs both directions, fee rounding, protocol/fund deductions, small amounts, extreme valid u64 values, overflow, zero reserve, creator fees rejected; exact match |
| Property tests | 1,000 generated valid zero-creator-fee inputs: output nonnegative and <reserve, nondecreasing output with input, no negative balance from buys, consistent rounding; deterministic test seed recorded |
| Timing | Late/out-of-order/stale/null/future timestamps; equal vs decreasing slots; minContextSlot not treated as history; request-before-delay never fills; first qualifying snapshot chosen even if later one is better |
| Strategy | Exact boundary fixtures for 3%,20%,r5=0; missing bars; ranking ties; alternate pools; same-session re-entry; H1 hash reproducibility; no study entries |
| Risk | Cash and slot reservations serialize competing orders; cap equality vs excess; expired signal; loss halt before fill; pending orders canceled at cutoff; unknown marks block new entries |
| Exit | Gap below stop does not fill at stop; trailing activation and high-water; time limit; repeated failures; frozen vault; program change; illiquid and zero-value cases remain open |
| Accounting | Hand-calculated buy/exit, failed buy, failed sell, canceled submitted order, fee deficit, open unknown mark; ledger and report identities hold exactly |
| Recovery | Inject kill before/after raw rename, before transaction commit and after commit before acknowledgment; no duplicate fills or fees; held capital and attempt numbers reconstructed; pending submitted orders canceled on live restart |
| Isolation | Second writer rejected; six portfolios share observations but not balances; report reads cannot mutate state; RPC submission and unknown origins blocked |
| Evidence | Missing payload/hash tampering aborts; no secret fields in logs; HTML/script payload remains inert; optional unsupported information never appears as PASS |
| Session | DST spring/fall, late start, missing entire night, cutoff/end/exit window, reboot gap, no-trade report, blocked carryover and recover-only mode |
| Replay/report | Same fixture and manifests twice produce byte-identical ordered event/ledger/report hashes; changed input hash detected; snapshot report unchanged after later recovery supplement |
| Resource/backup | Queue overflow visible; disk-full abort; quota/403 backoff; SQLite backup restored to a new directory with exact event/balance equality; log rotation does not delete evidence |
| Integrated fixture | At least one profitable close, losing close, rejected entry, failed submitted order, stale interval and blocked exit through recovery; report reconciles all |
| Actual WSL smoke | One uninterrupted scheduled night with heartbeat ≥95%, plus deliberate process termination/restart; zero duplicate fills/ledger discrepancy; observed host/version evidence |
| Study gate | Tests cover each failed criterion and zero denominator; fixture passing gate activates H2, failing gate activates H0; no undocumented intervention |
| Statistics | Known bootstrap indices/results; paired columns; missing sessions/too few samples/open exit suppress interval; no profitable-run selection |

Completion labels are independent:

- `ENGINEERING_VERIFIED_OFFLINE`: all applicable synthetic/fixture tests passed; no claim of actual WSL/provider readiness.
- `PAPER_DESK_VERIFIED`: offline gates plus actual WSL smoke, valid provider compatibility and a captured-data end-to-end replay pass. Real-time orders may be zero; synthetic fills prove execution plumbing, not actual liquidity.
- `STUDY_PASSED` or `STUDY_INSUFFICIENT`: determined only by §7 actual records.
- `PROSPECTIVE_COMPLETE`: all 28 scheduled outcomes recorded, including gaps/failures; coverage limitations remain visible.
- `INSUFFICIENT_EVIDENCE` or `EXPLORATORY_RESULTS_AVAILABLE`: statistical reporting decision, never production readiness or proof of edge.

Do not conflate these labels. A robust application can complete engineering and correctly report insufficient market evidence.

### 17.1 V21 regression suite

| Test ID | Required regression |
|---|---|
| V21-T01 | No network completion for eleven seconds expires a mark; a holding deadline still requests exit; sixty-second invalid interval preserves blocked inventory |
| V21-T02 | Bundle received before minute boundary but validated after it cannot supply that bar or an expired fill |
| V21-T03 | Delay/deadline equality, pre-delay request, exact cutoff, disabled first candidate and adverse first candidate produce the specified terminal outcomes |
| V21-T04 | Pending sell, canceled sell and successful sell each reconcile cash, conservative marks and all already-paid fees at every intermediate event |
| V21-T05 | An order counts its own reservation once; filling one scenario leaves all other scenario state unchanged |
| V21-T06 | Outage/reboot cannot erase watch opportunities; a fully missed night and empty watch interval have honest separate denominators |
| V21-T07 | Delayed study evaluation does not move embargo/holdout dates; premature phase activation fails |
| V21-T08 | SQLite TEXT quantities above signed-64 max remain exact through persistence, ordering, ledger balancing and restore |
| V21-T09 | Equal-time callbacks in different arrival orders cannot bypass durable ordering; replay of the recorded order remains identical |
| V21-T10 | Stale program check and unsynchronized clock block submissions without falsely reporting deployment change |
| V21-T11 | Actual profile object/list fixtures parse; unknown envelope blocks discovery visibly; malicious CSV text remains inert |
| V21-T12 | Late launch produces null scheduled session return; off-session recovery appears in bridge and campaign reconciliation |
| V21-T13 | Inclusive backup budget, interrupted export, raw parent-directory fsync boundary and restore detect missing evidence |
| V21-T14 | Primary shared eligibility permits independently costed stress paths; H0 creates no seventh funded account |

### 17.2 V22 regression suite

| ID | Exact behavior required |
|---|---|
| V22-T01 | Candidate available at 05:44:59.9 but processed at 05:45:00 cannot fill BUY; fees persist and reservation releases |
| V22-T02 | Ordinary execution deadline equality fills if every gate passes; one microsecond later fails; exact 06:15 cancels even with otherwise valid evidence |
| V22-T03 | Boundary snapshot processed late cannot use later-received/available mark; missing scheduled opening remains null for interval eligibility |
| V22-T04 | Ten-second RPC timeout does not prevent one-second health scheduling; a deliberately blocked storage commit causes visible lag and no historical fill |
| V22-T05 | Shared 100-USDC diagnostic passes but smaller proposal fails because fixed cost/A increases; reject without resizing/search |
| V22-T06 | Temporary reverse quote removes curve output rather than impaired output from reserve; protocol/fund floor-rounding has independent reference fixtures |
| V22-T07 | Projected buy loss crossing the session threshold cancels BUY without inventory; a successful severe fill can immediately request an exit |
| V22-T08 | Repeated retired-mint profiles cannot re-admit it; expired waiting mint cannot reset first_seen or consume a slot |
| V22-T09 | Recovery equal-slot responses do not satisfy three advancing polls; a missing opportunity resets the streak; restart clears entry features but retains trailing high-water |
| V22-T10 | Study/embargo end at 06:00, prospective at 06:15; final campaign recovery cannot create another entry session |
| V22-T11 | Read-only report export works while writer runs, changes no operational rows, and repeats byte-identically from the same cutoff |
| V22-T12 | Backup raw-reference set is taken from the backed-up database despite a concurrent later observation; restore hashes and balances match its cutoff |
| V22-T13 | Stale clock check blocks submissions; clock step cancels pending sells with fees retained and fresh attempts require recovered health |
| V22-T14 | HTTP 200/RPC error, compressed oversize stream, invalid Retry-After and unknown terms status produce their typed failure outcomes |

### 17.3 V23 regression suite

| Test | Required behavioral oracle |
|---|---|
| V23-T01 | Earlier receipt validates after newer slot: no retrospective fill/bar; later-ready item proceeds without waiting |
| V23-T02 | Crash after snapshot commit before availability acknowledgment: replay/recovery cannot use it at an earlier boundary |
| V23-T03 | Conflicting shared config/mint at an older finalized slot invalidates every dependent pool and cannot auto-resume |
| V23-T04 | Due program refresh progresses amid continuous position polls; skipped validation opportunities remain missing |
| V23-T05 | Batch with one null private account preserves unrelated pool; null shared Clock invalidates all dependent pools |
| V23-T06 | Host time past open_time but coherent chain time before it: no execution; chain equality passes opening check only |
| V23-T07 | Changed deployment plus replacement decoder cannot close legacy inventory or transfer it into a new campaign |
| V23-T08 | Canonical key-order/Unicode/large-integer vectors match bytes; duplicate keys, float values, nonfinite literals and surrogates reject |
| V23-T09 | Zero impaired quote, zero min_out, overflowed raw vault and exact risk equality have the specified outcomes; no zero inventory |
| V23-T10 | Embargo CLI, late evaluation, end-of-calendar invocation, idempotent registry/funding and restore-gap cancellation follow their matrix |

### 17.4 V24 regression suite

| Test | Exact expected behavior |
|---|---|
| V24-T01 | Crash before B, after B without witness, and after atomic witness/decision commit yields respectively unavailable, historically unavailable, and available exactly once; replay never repairs an earlier bar |
| V24-T02 | Witness usable_at 60.050 excludes boundary 60.000 despite earlier receipt/A; no recursive acknowledgment is scheduled |
| V24-T03 | Historical report remains byte-identical after position close/fee/mark expiry; reducer cache mismatch exits 5 |
| V24-T04 | Same program pointer with changed code or deployment slot permanently blocks; authority-only change is distinguished; incoherent pointer capture is not healthy |
| V24-T05 | Prospective restart 06:10 ends at 06:15, never 06:25; study restart 06:10 returns code 3; no new baseline or funding |
| V24-T06 | Fee debit crosses exact session threshold: pending buy cancels before fill; other portfolios retain independent latches |
| V24-T07 | Sell replaces mark with proceeds atomically; accounting identity holds before submission, while pending, after failure and after fill |
| V24-T08 | Inject every persistence boundary failure: no subsequent simulated economic transition; restart derives committed outcome exactly once |
| V24-T09 | Original/restored roots with same registry identity cannot both write; lock acquisition failure releases the first lock |
| V24-T10 | Compile contracts with conflicting constants/missing references: fail CONTRACT_CONFLICT; corrected compiled contracts map every active rule to implementation and behavioral evidence |

### 17.5 V25 regression suite

| ID | Behavioral oracle |
|---|---|
| V25-T01 | Small item count but insufficient byte capacity prevents dispatch; health timer still runs; body bytes shared by multiple pools count once |
| V25-T02 | Full nonblocking queue produces an explicit overload record, no writer await, no committed-event eviction and no new buy until recovery |
| V25-T03 | Pre-step validation completes after clock_epoch increment: never a current bar, recovery poll or fill candidate; historical evidence survives |
| V25-T04 | Older/equal program check cannot refresh health; strictly advancing valid check can; malformed old result cannot prove a code change |
| V25-T05 | Exact watch-retirement boundary cancels pending buys once with fees retained; positions stay pinned and are not force-closed by retirement alone |
| V25-T06 | Recorded replay/report remains identical after current health/config changes; audit missing dependencies blocks, and recomputed disagreement exits 5 |
| V25-T07 | Fully missed final session can receive an honest report cutoff through reconcile-calendar without network or capital creation; repeating command is a no-op |
| V25-T08 | Late reconciliation preserves null scheduled equity and excludes later recovery economics from the missed session while including them in the bridge |
| V25-T09 | Official-source reference harness metadata binds exact input/output/source hashes; unavailable build never reports parity PASS |
| V25-T10 | Maximum-response preparation and reporting resource run records peak resident memory; item and byte caps hold under delayed writer/validation |

## 18. Hand-calculated acceptance fixtures

Synthetic arithmetic example, units intentionally abstract: X=1,000,000, Y=2,000,000, A=10,000, f=2,500 and D=1,000,000. Trade fee is 25; effective input 9,975; curve output is 19,752; 25-bps impairment gives 19,702. Test must independently calculate these integer results. Test reversed reserve orientation separately, never assume symmetry in units.

Synthetic USDC accounting example: capital 10,000; successful buy spends 100 plus 0.10 execution proxy; cash becomes 9,899.90. Full sell produces 108 gross and costs 0.10; cash becomes 10,007.80; realized P&L 7.80. If one failed sell submission cost 0.10 before that successful sale, final cash is 10,007.70 and P&L 7.70. If instead the position remains open with unknown liquidation value after the buy, cash is 9,899.90, conservative equity is 9,899.90, market equity is unavailable, and no closed trade exists.

Synthetic restart example: submission transaction commits fee 0.10 and reserves 100; process dies before a fill. Recovery records one CANCELED order, cash remains 9,999.90, releases 100 reservation, creates no position and no fill. Repeated recovery changes neither cash nor event outcomes.

## 19. Change control and unresolved-event policy

No active design question is intentionally deferred to owner selection within v1. Remaining real-world uncertainty maps to exact system behavior:

| Observation during implementation/operation | Required behavior |
|---|---|
| No supported pools/candidates | Complete pipeline/report, NO_TRADE; fail feasibility sample gate |
| Public RPC inadequate or provider unavailable | Throttle, retain missingness, STUDY_INSUFFICIENT; no purchase or fallback fabrication |
| Data use/retention permission not established | BLOCKED_PROVIDER_TERMS; synthetic mode only |
| Program source/account compatibility not demonstrable | BLOCKED_PROGRAM_COMPATIBILITY; no real-data fills |
| Current source supports an unmodeled fee/layout | UNSUPPORTED; versioned adapter work required, never generic curve fallback |
| Actual WSL host unavailable to agent | Offline implementation may pass; actual-host gate remains NOT_RUN |
| Runtime installation absent | Give exact local setup prerequisites; do not claim environment validation |
| Profitable-looking small sample | Descriptive only; no performance promotion |
| No possible sell | Keep inventory, null mark, conservative zero, blocked carryover |
| Requirement outside scoped contracts | Record change request; preserve v1 behavior and finish independent work |

This is how an implementable specification handles uncertainty: it defines outcomes, rather than promising that documentation can remove external dependencies or establish a trading edge.

## 20. Verification scope and implementation handoff

This consolidation changes document organization and resolves superseded wording; it does not implement or validate the application. Source references and prior retrieval limitations are preserved as inherited evidence, not freshly verified research. No runtime test, provider call, WSL operation, reference build, study or prospective experiment is claimed by this revision.

For each implementation phase, report only changes, affected files, exact verification commands/results, and remaining blockers or unverified gates. Do not infer specification completion from file existence or system readiness from document checks. Numerical policy changes require a versioned specification and a new campaign with retained history.

## 21. Consolidated research register and evidence limits

Sources R1–R16 were inherited from the supplied blueprint; this revision does not claim every inherited URL was successfully refetched. Additional retrieval/verification for v2.1 was performed on **2026-11-06**, audit recorded at **2026-11-06T17:58:07Z**. R17–R21 record the new evidence and access limitations. These are architecture/methodology sources, not trailing-week market data. URLs are mutable; the implementing agent must pin source/code versions as required above. These sources support the cited technical facts and research principles; they do not endorse this desk or establish optimal trading parameters.

| Ref | Primary source | Supports / limitation |
|---|---|---|
| R1 | [Raydium official program addresses](https://github.com/raydium-io/raydium-docs-v1/blob/main/reference/program-addresses.mdx) | CPMM program identity; does not prove any particular pool is safe |
| R2 | [Raydium official CPMM fees](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/cpmm/fees.mdx) | Separate fee components and creator-fee modes; motivates narrow support |
| R3 | [Solana clusters and public RPC](https://solana.com/docs/references/clusters) | Public mainnet endpoint, rate-limit variability, production caveat |
| R4 | [DEX Screener API reference](https://docs.dexscreener.com/api/reference) | Profile/pair endpoints and quotas; does not promise complete launch coverage |
| R5 | [Solana getMultipleAccounts](https://solana.com/docs/rpc/http/getmultipleaccounts) | Request account limit, response context, commitment/minContextSlot parameters |
| R6 | [Solana token accounts and authorities](https://solana.com/docs/tokens) and [Freeze account](https://solana.com/docs/tokens/basics/freeze-account) | Mint/authority/account semantics; no rug-risk guarantee |
| R7 | [Circle: supported native USDC](https://help.circle.com/support/en/usdc-supported-blockchains-minting-redemption-faqs?id=kb_article_view&sysparm_article=KB0010590) | Native Solana USDC identity; no USD-parity assumption in accounting |
| R8 | [Bailey, Borwein, López de Prado & Zhu: The Probability of Backtest Overfitting](https://escholarship.org/uc/item/4w1110bb) | Repeated selection can overfit investment backtests; a simple holdout is not a universal cure |
| R9 | [Bailey & López de Prado: The Deflated Sharpe Ratio](https://doi.org/10.3905/jpm.2014.40.5.094) | Selection bias and nonnormal returns undermine naive performance claims; DSR itself is not implemented here |
| R10 | [Raydium official fee arithmetic](https://github.com/raydium-io/raydium-cp-swap/blob/master/programs/cp-swap/src/curve/fees.rs) | Fee denominator and ceil/floor conventions; pin the actual source during implementation |
| R11 | [Raydium official source repository](https://github.com/raydium-io/raydium-cp-swap), especially `curve/constant_product.rs`, `curve/calculator.rs`, `states/pool.rs`, `instructions/swap_base_input.rs` | Required curve/layout reference. Fee/pool source retrieved; some direct curve-file fetches were unavailable in drafting. Exact pinned-source parity remains a mandatory build gate, not claimed verified |
| R12 | [SQLite WAL](https://www.sqlite.org/wal.html) and [PRAGMA synchronous](https://sqlite.org/pragma.html) | Transaction durability/concurrency settings; application still needs recovery tests |
| R13 | [Politis & Romano: The Stationary Bootstrap](https://doi.org/10.1080/01621459.1994.10476870), [Stanford author report](https://statistics.stanford.edu/technical-reports/stationary-bootstrap) | Block resampling for dependent stationary observations; crypto may violate assumptions |
| R14 | [Microsoft: systemd on WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd) | WSL service-manager capability; not an unattended-host guarantee |
| R15 | [SQLite Online Backup API](https://www.sqlite.org/backup.html) | Consistent database backup mechanism |
| R16 | [Solana transaction fees](https://solana.com/docs/core/fees) | Actual network fees are SOL-based and include priority components; the USDC costs here are expressly scenario proxies, not retrieved network quotes |
| R17 | [SQLite Floating Point Numbers](https://www.sqlite.org/floatingpoint.html) | Retrieved in this revision: signed-integer storage limits and approximate REAL arithmetic; supports exact application-integer aggregation |
| R18 | [Python 3.12 asyncio event-loop documentation](https://docs.python.org/3.12/library/asyncio-eventloop.html) | Retrieved: monotonic timers and undefined equal-time delayed-callback order; motivates explicit scheduler |
| R19 | [Bailey et al., author-hosted paper](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf), [Politis/Romano institutional report](https://statistics.stanford.edu/technical-reports/stationary-bootstrap) | Retrieved paper and institutional abstract respectively; reinforces restricted experimentation and dependent-data resampling, not chosen sample/parameter optimality |
| R20 | [DEX Screener official API reference](https://docs.dexscreener.com/api/reference), [Solana getMultipleAccounts](https://solana.com/docs/rpc/http/getmultipleaccounts) | Rechecked API identity/shape and coherent batched account mechanism; no promise of completeness or capacity |
| R21 | [Raydium official swap instruction](https://github.com/raydium-io/raydium-cp-swap/blob/master/programs/cp-swap/src/instructions/swap_base_input.rs) | Retrieved official instruction shows fee/curve/mechanics interactions. Direct official curve-file retrieval failed; a crate source rendering was inspected but is not accepted as deployment/source verification. Mandatory official pinned-reference build gate remains NOT_RUN |

### 21.1 Inherited R22–R27 evidence and limits

Sources below were retrieved on 2026-11-06 UTC through web research. Detailed source pages support engineering constraints and methodological caution; none establishes the chosen token thresholds, trading profitability, sample power or production readiness. R1–R21 retain their original inherited/retrieved labels; they were not all freshly audited here.

| Source | Official/primary URL and verified scope | Consequence |
|---|---|---|
| R22 | https://freedesktop.org/software/systemd/man/latest/org.freedesktop.timedate1.html — NTPSynchronized reports kernel synchronization status | Health evidence is narrower than a measured clock-error guarantee |
| R23 | https://docs.python.org/3.12/library/asyncio-task.html — asynchronous tasks, cancellation and timeout behavior | Isolate I/O waits from scheduler/writer; application ordering remains explicit |
| R24 | https://github.com/raydium-io/raydium-cp-swap/blob/master/programs/cp-swap/src/curve/calculator.rs and fees.rs — direct retrieval failed in this revision; official instruction/repository search results located, not independently validated curve source | Do not promote illustrative arithmetic to deployment verification; pinned build/fixture gate remains mandatory |
| R25 | https://solana.com/docs/rpc/http/getmultipleaccounts — ordered account array, explicit commitment/configuration, maximum 100 accounts | Preserve bundle-to-address mapping; existing 90-account application cap remains conservative |
| R26 | https://sqlite.org/pragma.html and https://www.sqlite.org/wal.html — FULL/WAL sync and checkpoint behavior | Retain durable single-writer commits and measure stalls; sync depends on underlying host/storage |
| R27 | https://scholarworks.wmich.edu/math_pubs/42/ — authors' institutional abstract of The Probability of Backtest Overfitting | Prespecification/holdout do not establish edge; record all trials and keep claims exploratory |

No academic or expert-consensus source settles which momentum band, stop size, direct-USDC cohort or haircut is best for this strategy. Those decisions remain transparent [D] hypotheses. The academic caution is particularly relevant because a holdout alone does not neutralize selection across repeated campaigns. Keep the global campaign/trial history required by §14 and do not turn an exploratory interval into a promotion rule.

### 21.2 Inherited R28–R32 evidence and limits

Fresh retrieval date: 2026-11-06 UTC; document revision UTC is recorded at the top. References below support only the stated facts. Numerical trading/operational defaults remain [D]. Architecture sources are not trailing-week market observations.

| Ref | Primary source and retrieved finding | Application / limit |
|---|---|---|
| R28 | https://github.com/raydium-io/raydium-cp-swap/blob/master/programs/cp-swap/src/instructions/swap_base_input.rs and https://github.com/raydium-io/raydium-cp-swap/blob/master/programs/cp-swap/src/states/pool.rs | Official mutable source: chain clock/open_time, status, fee updates, reserve fee deductions and invariant check. Requires immutable pin/fixtures during build; not deployment equivalence. |
| R29 | https://docs.python.org/3.12/library/json.html | Default decoder accepts repeated names and nonfinite extensions; strict canonical protocol must be explicit. |
| R30 | https://docs.python.org/3.12/library/decimal.html | Context controls precision, rounding and signals; finite decimal operations need explicit conventions. |
| R31 | https://scholarworks.wmich.edu/math_pubs/42/ | Authors' institutional abstract, Probability of Backtest Overfitting: holdout methods can be unreliable in investment selection. Full paper not freshly audited; no new theorem/power claim made. |
| R32 | https://solana.com/docs/rpc/http/getmultipleaccounts | Official reference confirms ordered account result/context and account-count limit; supports complete-bundle mapping. |

Access limitations: direct retrieval of official fees.rs and constant_product.rs did not succeed; attempted academic stationary-bootstrap PDF retrieval also failed. DEX Screener terms page retrieval did not succeed. No conclusion of provider permission or updated curve equivalence follows. Existing provider permission and deployment compatibility gates remain unresolved evidence dependencies with fully specified blocking behavior, not unanswered design decisions.

### 21.3 Inherited R33–R36 evidence and limits

Fresh retrieval: 2026-11-06 UTC, revision timestamp at document start. These are official technical references. Inherited academic sources remain useful methodological context; no additional academic optimality or calibrated trading claim is made.

| Ref | Primary source | Retrieved fact and application |
|---|---|---|
| R33 | https://solana.com/docs/core/accounts/account-types | Loader-v3 executable code resides in separate ProgramData; motivates coherent fingerprint capture |
| R34 | https://solana.com/docs/core/programs/program-deployment | Upgrades update ProgramData code/slot while Program pointer can stay unchanged; supports explicit change classification |
| R35 | https://www.sqlite.org/isolation.html | WAL read transactions retain a snapshot from the read transaction's start; historical logical cutoffs require reconstruction |
| R36 | https://github.com/raydium-io/raydium-cp-swap/blob/master/programs/cp-swap/src/instructions/swap_base_input.rs | Current indexed official instruction rejects chain timestamp below open_time; equality remains consistent with §3.3. Mutable source requires immutable pin during implementation |

Direct raw GitHub retrieval failed in this revision; official indexed instruction content was retrieved. No live RPC request, code commit pin, deployed-bytecode capture, provider retention permission, WSL validation, strategy test or statistical experiment was performed. Sources R33–R35 were retrieved through indexed official documentation. Operational numbers above remain [D].

### 21.4 Inherited R37–R41 evidence and limits

Fresh retrieval audit: 2026-11-06 UTC. The revision timestamp in the front matter applies to this register. These are technical/methodological sources, not trailing-week market measurements. No live pool measurements or optimal thresholds were inferred.

| Ref | Retrieved primary source | Supported fact; design application |
|---|---|---|
| R37 | https://docs.python.org/3.12/library/asyncio-queue.html | Queue maxsize measures items; await put can block. Supports explicit nonblocking admission; 64 MiB is [D], not a Python recommendation. |
| R38 | https://solana.com/docs/rpc/http/getmultipleaccounts | Ordered account results with context and commitment/minContextSlot configuration. Watermark/generation policy is [D]. |
| R39 | https://www.sqlite.org/datatype3.html and https://www.sqlite.org/lang_aggfunc.html | SQLite conversion/aggregation semantics require care; signed INTEGER and approximate REAL do not provide arbitrary-precision token math. Reaffirms existing §12.1 rather than inventing a new requirement. |
| R40 | https://www.sqlite.org/floatingpoint.html | Binary floating point is approximate. Exact integer monetary decisions remain required. |
| R41 | https://scholarworks.wmich.edu/math_pubs/42/ | Authors' institutional abstract of Probability of Backtest Overfitting warns that conventional holdout methods can be unreliable in investment selection. Abstract rechecked; no new full-paper audit, power calculation or theorem claimed. |

A separate attempted Berkeley-hosted academic PDF was inaccessible and is not relied on. No newly verified Raydium source commit or deployed-source match is claimed. The existing independent official-source fixture gate remains mandatory. Academics support disciplined experimentation and cautious inference; no credible expert consensus supplies the best momentum band or loss thresholds for this particular sampled cohort.

## 22. Requirement traceability and change records

Create `contracts/traceability.csv` with one row per active atomic rule/gate and fields `requirement_id,section,decision_id,implementation_symbol,test_id,evidence_path,status`. Status is NOT_IMPLEMENTED, IMPLEMENTED_UNVERIFIED, VERIFIED or BLOCKED. File existence never establishes VERIFIED.

Preserve all V21–V25 acceptance IDs and frozen V22, V23, V24 and V25 requirement IDs, including V23-24-n requirement rows. For inherited rules without a frozen ID, assign V22-<original-section>-<ordinal> once, splitting compound requirements into stable rows. Preserve original-source locations in provenance fields even though this consolidated blueprint uses topical section locations. Record superseded IDs explicitly; do not renumber existing IDs to match the new section layout.

Every active rule must map to a reviewed executable contract, implementation symbol, public-behavior acceptance test and evidence status. Unavailable dependencies block only their dependent stages. The implementing agent must complete independent offline engineering and report each stage at its actual evidence level.
