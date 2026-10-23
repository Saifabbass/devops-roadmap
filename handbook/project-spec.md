# Taskboard: the project you will operate for a year

Build a small service whose behavior stays understandable while its operational demands grow. A user creates tasks, sees their own tasks, and completes them. The learning challenge is preserving those promises through deployment, failures, recovery, and change.

The course supplies a staged starter and reference application in the downloadable lab files. Week 3 begins with an unfinished validator; later stages add persistence and ownership. Local unit, adapter and HTTP checks have been executed; PostgreSQL and container execution remain unverified in the authoring environment. Follow the guided weekly lessons for implementation, commands and acceptance evidence. This specification defines the behavior those lessons must preserve. A frontend, account registration, deletion, search, attachments, and microservices are outside the required core. Add complexity only when an exercise needs it.

## 1. Freeze a small contract

The target API contract is **1.0**, frozen at week 7. Application releases are separate: `v0.1` is the week-3 prototype; `v0.2` is the week-8 release. Database schema versions have their own migration history. Record all three in release evidence.

A task response has exactly these fields:

| Field | JSON type | Meaning |
|---|---|---|
| `id` | string | Server-generated UUID; immutable. |
| `title` | string | Submitted title after trimming surrounding whitespace. |
| `completed` | boolean | Initially `false`; becomes `true` on completion. |
| `created_at` | string | Server timestamp in UTC RFC 3339 format, ending in `Z`. |
| `completed_at` | string or null | Initially null; first completion timestamp, subsequently unchanged. |

The server stores an immutable `owner_id`, derived from the authenticated identity. Clients cannot choose it. It need not appear in responses.

For creation, accept only `{"title":"Ship first release"}`. Require an actual string, trim using Python's `str.strip()` semantics, then require 1–120 Unicode code points. Reject nulls, numbers, arrays, empty or whitespace-only strings, oversized strings, and additional fields. This means `{"title":"x","owner_id":"someone-else"}` fails validation. Treat timestamps as server data.

| Request | Successful response | Important behavior |
|---|---|---|
| `POST /tasks` | `201`, task object; `Location: /tasks/{id}` | Creates a new task owned by the caller. |
| `GET /tasks/{id}` | `200`, task object | Returns only a task belonging to the caller. |
| `GET /tasks` | `200`, `{"items":[...]}` | Returns only the caller's tasks, ordered by `created_at`, then `id`; empty list is valid. |
| `POST /tasks/{id}/complete` | `200`, task object | Send an empty body. Complete the caller's task; repeating the request preserves its first completion timestamp. |

No reopening or general update endpoint is required. Creation is **not** idempotent: retrying a successful creation can create another task. Completion is designed to be idempotent. Explain this distinction before adding automatic retries.

The unpaginated list is a deliberate lab limit: use at most 1,000 tasks per identity. Document that larger workloads require pagination and resource-limit decisions; this contract alone does not establish production scalability.

For authenticated requests, invalid UUID syntax or invalid creation input returns `422`. A well-formed UUID that is missing **or belongs to another user** returns the same `404`. Missing or invalid credentials return `401` with `WWW-Authenticate: Bearer`. An unavailable database returns `503` within five seconds in this lab; unexpected failures return a sanitized `500`. Do not turn failures into empty successful responses.

Use this task-route error shape:

```json
{
  "error": {"code": "TASK_NOT_FOUND", "message": "Task not found"},
  "request_id": "server-generated-identifier"
}
```

Use codes `VALIDATION_ERROR`, `UNAUTHENTICATED`, `TASK_NOT_FOUND`, `DEPENDENCY_UNAVAILABLE`, and `INTERNAL_ERROR`. Generate a request identifier server-side, return it as `X-Request-ID`, and attach it to logs. Never return stack traces, connection strings, or tokens. Test validation with valid credentials, and authentication with otherwise valid requests, so combined-invalid-input precedence is outside the contract.

FastAPI can validate request models and produce OpenAPI descriptions; configure strict types and forbidden extra fields deliberately. Its default error body differs from this contract, so implement and test the necessary exception handlers. [Request bodies](https://fastapi.tiangolo.com/tutorial/body/), [error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/).

## 2. Evolve the implementation in stages

**[Week 3](../index.html#week-3): in-memory prototype.** Use the internal owner `local-student`, bind locally, and implement validation plus create/list/get/complete. Losing tasks on restart is expected at this stage. Add `GET /livez` returning `200 {"status":"ok"}` and `/version` reporting `app_version`, `api_contract`, and `git_sha`. Log method, path template, status, duration, and request ID; avoid task titles and credentials.

**[Week 6](../index.html#week-6): PostgreSQL.** Persist tasks through application restarts. Introduce versioned migrations and a tasks table with UUID primary key, owner, title, completion state, and timestamps. Enforce essential invariants with database constraints as well as application validation. Use parameterized queries, transactions, and ownership predicates in reads and updates. Make repeated or concurrent completion preserve one timestamp. Add `/readyz`: `200 {"status":"ready"}` only when the database is reachable and the required schema is usable; otherwise `503 {"status":"not_ready"}`. Keep `/livez` independent of database availability. Use bounded checks. Health endpoints contain no sensitive diagnostics and remain local/private.

**[Week 7](../index.html#week-7): two synthetic identities.** Use a maintained framework bearer-authentication dependency to parse credentials, then map two distinct lab-only opaque tokens to server-controlled IDs `lab-alice` and `lab-bob`. Store tokens outside Git. Do not create a password system or homemade JWT verifier. Only known disposable seed records may be explicitly reassigned from `local-student`; never silently transfer ownership of existing real data. [FastAPI security reference](https://fastapi.tiangolo.com/reference/security/).

This teaching authentication remains local or behind a private tunnel through later cloud exercises. Public exposure requires an established identity provider, maintained verification of issuer, audience, and expiry, and demonstrated task authorization. GitLab workload OIDC authenticates deployment jobs; it does not authenticate Taskboard users.

**[Week 9 onward](../index.html#week-9): preserve behavior while changing delivery.** Run separate unit, integration, and system jobs; publish one tested image and deploy its digest. Terraform, Ansible, Kubernetes, and GitOps change how the service is provisioned and operated. They must not change what successful requests mean.

## 3. Prove behavior at the right boundary

Unit tests exercise isolated logic. Integration tests use a **real PostgreSQL instance** with an isolated test database or schema. System tests call the running service over HTTP. An in-process framework client is useful, but does not prove the deployed listener, container networking, or restart behavior. Keep test infrastructure unable to select a production database accidentally.

| Level | Exact example | What it proves |
|---|---|---|
| Unit | `"  Ship  "` becomes `"Ship"`; 120 characters pass; 121, spaces, null, and integer input fail. | The validation boundary is intentional. |
| Unit | Completing an already-completed task preserves its timestamp. | Repeated execution has the intended semantics. |
| Integration | Insert, read, and complete a task against PostgreSQL; attempt an invalid constrained row. | Queries, mappings, and database constraints agree. |
| Integration | Force a transaction failure after a write, then read from a new transaction. | Failed work does not leave partial state. |
| Integration | Complete one task concurrently twice and inspect the stored result. | Completion remains consistent under concurrency. |
| System | Alice creates `"Ship"`; get/list contain its ID and title; complete/read show `true`. | The deployed positive path matches the contract. |
| System | Missing/invalid token gives `401`; Alice's list excludes Bob's task. | Authentication and list isolation both work. |
| System | Bob reads or completes Alice's ID: both `404`; Alice then sees unchanged data. | Denial prevents both disclosure and mutation. |
| System | Valid token plus invalid title or UUID gives `422`; unknown valid UUID gives `404`. | Clients can distinguish invalid input from absence. |
| System | Restart the app, then the database separately; read a previously committed task. | Persistence survives both restarts from week 6 onward. |
| System | Stop only the disposable lab database: task request gives bounded `503`, readiness `503`, liveness `200`. | Dependency failure is visible without falsely declaring the process dead. |
| Integration + system | Upgrade a database containing an older-release fixture; verify ownership, title, and completion through HTTP. | Migration preserves meaning as well as rows. |
| System | Restore into a separate database; compare IDs, owners, titles, and completion values. | Recovery restores useful data, beyond a matching row count. |

Deliberately return `200` with the wrong title once: your system test must fail. Assert bodies and state, not just status codes. Use fixtures to isolate cases and clean up only their resources. [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html).

## 4. Change without trapping the previous release

Number migrations and record the schema version with every release. Never edit an already-applied migration to disguise history. Test upgrades from a populated previous schema, including a controlled migration failure and its documented recovery path.

Prefer expansion, backfill, then later removal. Before a rolling update, test whether both application versions can use the resulting schema. Renaming a response field, changing its type, or changing status semantics breaks contract 1.0 unless compatibility is maintained. An additive field still needs consumer checks. Image rollback does not reverse deleted columns or lost data. Document when recovery requires a forward fix or restore instead. Consult PostgreSQL's [constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) and [backup documentation](https://www.postgresql.org/docs/current/backup.html).

## 5. Four reviewable milestones

| Gate | Definition of done |
|---|---|
| [Week 8](../index.html#week-8) | Release `v0.2`; separate test commands pass; ownership tests pass; restart and isolated restore succeed. Record image digest, locked dependencies, migration version, and evidence. Recover a deliberately incorrect image selection using the previous artifact without rebuilding. State schema rollback limits. |
| [Week 24](../index.html#week-24) | Rebuild a disposable VM environment using Terraform and Ansible, deploy through GitLab, and restore data. Replace a removed lab host and recover a bad configuration. Record recovery duration, remaining manual steps, and scoped cleanup. |
| [Week 32](../index.html#week-32) | Deploy through GitOps, measure requests during a rolling update, and recover a readiness-failing image through the declared source of truth. Demonstrate image/config/schema compatibility and explain remaining single points of failure. A local cluster does not prove zone-failure resilience. |
| [Week 52](../index.html#week-52) | Another operator rebuilds, deploys, diagnoses, and recovers using your documentation—or label the exercise a fresh-environment self-review. Resolve critical failures; mark unmet gates incomplete. Present measured reliability, security tests, restore evidence, costs, limitations, and next-quarter priorities. |

For a repeatable performance sample, seed 1,000 tasks, use ten concurrent clients, warm up for one minute, then measure five minutes with 90% reads and 10% completion requests against seeded tasks. Report how many completion requests changed state versus repeated an already-completed operation. Record hardware, dataset, request rate, errors, and latency percentiles. A provisional `p95 < 300 ms` is a lab hypothesis to evaluate, not a universal requirement. Report fault-injection intervals separately and in the total results. Five successful minutes cannot establish a monthly availability SLO.

Your strongest deliverable is a defensible explanation of what works, what fails, and what the evidence cannot yet prove.
