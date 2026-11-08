# Authority matrix (advisory; not runtime enforcement)

| Action | Default handling |
|---|---|
| Read local project files and inspect Git | Within actual runtime permissions |
| Edit assigned project files | Only within user task and effective sandbox |
| Install dependencies or use network | Request scoped approval; verify destination, provenance and licenses |
| Access Solana read-only data | Only if explicitly authorized, blueprint provider gates satisfied |
| Wallets, signing, transactions, live orders | Prohibited by blueprint |
| Commit, push, PR, merge, publish, deploy | Separate explicit user authorization for each effect |
| Change blueprint economics, methodology or security | Stop and obtain owner decision |

Rules and AGENTS are not an authorization firewall. Enforce external effects through actual runtime and host controls. Review denial is terminal for that invocation; never route through another tool to bypass it.
