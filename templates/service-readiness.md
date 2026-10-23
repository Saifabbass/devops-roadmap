# Service readiness review: <release>

- Service owner:
- Commit / artifact digest / deployment configuration version:
- Environment and review date:
- Reviewer:
- Decision: ready for the stated lab / changes required

Each item needs a link or measurement; an unchecked assertion is not evidence.

| Area | Evidence | Score 0-3 | Gap / owner / due date |
|---|---|---|---|
| Reproducible clean setup and scoped teardown | | | |
| Unit, integration and system tests; failing gate | | | |
| Threat model, identities, secrets and denied actions | | | |
| Compatible rollback and verified data restore | | | |
| SLI/SLO, logs, actionable alert and tested runbook | | | |
| Load profile, latency, throughput and errors | | | |
| Cost estimate, resource inventory and cleanup | | | |
| Architecture, decisions, incident and handoff docs | | | |

## Operating limits

Measured workload, hardware, dependency assumptions and observation window:

RTO/RPO targets and actual exercise results:

Accepted risks and expiry dates:

## Blocking checks

- No real secrets in code, artifacts or logs.
- No unintended public administrative endpoint.
- Required failed tests block promotion.
- Destructive targets and rollback are explicit.
- Untrusted CI work cannot access sensitive environments.
- Recovery and performance claims match evidence.

## Handoff

Independent setup/operation result:

Total score and remaining actions:

Next review date:
