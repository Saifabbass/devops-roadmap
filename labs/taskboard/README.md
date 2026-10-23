# Taskboard: build it, then learn to operate it

Taskboard is the small API used throughout Dev Opps. This folder contains **a learner starter**, **completed reference stages**, and exercises which make their promises observable. Follow week 3 before reading every reference module. The contract lives in `../../handbook/project-spec.md`; the supplied implementation does not replace your own practice.

All terminal commands below run in **this `labs/taskboard` directory** unless a command explicitly says otherwise. On Ubuntu 24.04, open Terminal (Bash). On Windows use the course's Ubuntu/WSL guide; the Python-only commands also work in PowerShell with the activation difference below. No command in this README creates a paid cloud resource.

## What is supplied, and what you build

| Entry point | What changes | What remains your work |
|---|---|---|
| `starter.app:app` | A working `/livez` endpoint; `starter/domain.py` has an unfinished title validator. | Implement the validator, see its tests pass, add one endpoint at a time. |
| `reference.stage03:app` | Complete in-memory implementation with validation, structured errors, request IDs, and create/list/get/complete. | Compare only after attempting the checkpoint. Explain each behavior. Data disappears when the process stops. |
| `reference.stage06:app` | Same contract, PostgreSQL, explicit migrations, readiness. | Learn the SQL/transaction boundary; prove persistence, constraints and rollback. |
| `reference.stage07:app` | Same database, two lab-only opaque bearer tokens and owner filtering. | Prove Alice/Bob cannot read or mutate each other's tasks. |

The references share `domain.py` (pure behavior), `api.py` (HTTP boundary), and a store (`memory.py` or `postgres.py`). That is a small seam for learning, not a recommendation to create dozens of abstractions. Read the functions in this order: `normalize_title` → `new_task` → `MemoryStore.create` → the `/tasks` handler → the associated tests. The SQL store becomes relevant in week 6, not on day one.

There is no frontend, deletion endpoint, JWT implementation, account registration, or public authentication service. At most 1,000 tasks per identity is the deliberate lab workload. The unpaginated list, connection-per-operation database access, synthetic tokens, and simple single-instance deployment are explicit limits. Repeated completion preserves its first timestamp. Retrying creation can create another task; never blindly retry an ambiguous POST.

## Prepare an isolated Python environment

First locate the downloaded course folder. In Bash, type `cd ` (including the space), drag the **labs/taskboard** folder into the terminal to insert its exact path, and press Enter. Run `pwd` and check that its final two components are `labs/taskboard`.

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --no-cache-dir -r requirements-dev.lock
python -m pip check
```

`--version` shows the interpreter you will use. `-m venv .venv` creates a project-local interpreter environment, preventing changes to system Python. `source` updates this terminal to use that interpreter. `-m pip` selects pip belonging to that Python; `-r` reads exact dependency versions, and `--no-cache-dir` avoids a duplicate download cache. `pip check` checks dependency compatibility. Python 3.12 or later is the intended learner baseline; this authored run used Python 3.14.3, and the pinned container uses Python 3.14. If Ubuntu reports that venv is missing, run `sudo apt-get update` then `sudo apt-get install python3-venv` once and retry environment creation. Those commands update the package index and install Ubuntu's virtual-environment support.

PowerShell equivalents for environment creation/activation are `python -m venv .venv` and `.\.venv\Scripts\Activate.ps1`. If activation is restricted, use `.\.venv\Scripts\python.exe` in place of `python`; changing the machine's execution policy is unnecessary. The Bash examples below should be followed inside Ubuntu rather than pasted blindly into PowerShell.

`requirements.lock` pins runtime packages; `requirements-dev.lock` additionally pins test packages. Versions were resolved from the official package index on 2026-10-20. Image digests in `Dockerfile` and `compose.yaml` were read from Docker Hub's registry API on that date. Pins are reproducibility evidence, not a permanent security guarantee: test upgrades and regenerate reviewed locks deliberately. The complete dependency lock is version-pinned, not hash-locked.

## Week 3: attempt, check, then compare

```bash
python -m pytest starter/test_domain.py -q
```

`pytest` runs the explicitly named starter tests; `-q` reduces output. At first all eleven cases fail with `NotImplementedError`: that is the exercise's visible starting point. Edit `starter/domain.py`, replacing the unfinished function according to its four comments, and rerun exactly this command. Expected end state: eleven passing cases, covering string type, whitespace trimming, length boundaries and Unicode. Do not change tests to accommodate a defect.

```bash
python -m uvicorn starter.app:app --host 127.0.0.1 --port 8000
```

Uvicorn is the HTTP server. `starter.app:app` means “import the `app` object in `starter/app.py`.” `127.0.0.1` accepts only this machine's traffic; `8000` is the listening port. Keep this terminal open. In a second terminal run `curl -i http://127.0.0.1:8000/livez`; `-i` includes response headers. Expect `200` and `{"status":"ok"}`. `Ctrl+C` stops only this foreground process.

Implement in four checkpoints: (1) strict request model and `POST /tasks` with a generated UUID; (2) list/get and unknown-ID `404`; (3) completion with one immutable timestamp; (4) structured validation/error handlers and safe request logging. The week-3 lesson explains the code pieces. After attempting each checkpoint, open the matching completed module and compare differences. Use the finished stage when a later infrastructure lesson requires a known working application:

```bash
python -m uvicorn reference.stage03:app --host 127.0.0.1 --port 8000 --no-access-log
```

`--no-access-log` disables Uvicorn's raw-path request log because the app writes a structured log using the path template (for example `/tasks/{task_id}`). The log includes a newly generated request ID, method, status, and elapsed milliseconds. It excludes titles, credentials, query strings and exception text. Do not run multiple worker processes in memory mode: each would own unrelated data.

From a second terminal:

```bash
curl -i -H 'Content-Type: application/json' -d '{"title":"  Ship my first task  "}' http://127.0.0.1:8000/tasks
curl -i http://127.0.0.1:8000/tasks
curl -i -H 'Content-Type: application/json' -d '{"title":"   "}' http://127.0.0.1:8000/tasks
```

`-H` sets the body format; `-d` sends the literal JSON body and selects POST. The first request returns `201`, a trimmed title, an ID, and a `Location` header. The second uses GET and returns `items`. The last returns `422`, `VALIDATION_ERROR`, and a request ID matching its `X-Request-ID` header. Never copy a displayed UUID from an example: use your response's actual ID.

## Test boundaries separately

```bash
python -m pytest tests/unit -q
python -m pytest tests/contract -q
python tools/run_local_system.py
```

The first command tests pure behavior and the memory store. The second tests the HTTP adapter in process, including synthetic identity isolation and sanitized failures; it does **not** prove a socket or container works. The third starts a real loopback listener on an unused port, sends HTTP requests through `tests/system`, writes a JUnit result and server log to `reports/`, and stops only its own child process. The memory run deliberately skips the authenticated-user case; it cannot prove week-7 PostgreSQL behavior.

To prove a test catches a defect, edit your **starter** validator to allow an empty string and rerun `starter/test_domain.py`; the empty-title case must fail. Undo just that edit, and confirm the test passes. Keep the failing and passing outputs in your course evidence. Do not weaken reference validation to bypass a later exercise.

## Week 5: package stage 3

Prerequisite: Docker Engine/Desktop with Linux containers and Compose v2. Check `docker version` (client **and server** must respond) and `docker compose version`. Docker permission errors mean the daemon or Linux user access needs attention; do not solve them by making its socket world-writable. The Dockerfile's base is pinned, uses a non-root UID 10001, and copies no `.env`, virtual environment, Git history or credentials.

```bash
docker build --target runtime -t devopps-taskboard:local .
docker run --rm --name devopps-memory -p 127.0.0.1:8000:8000 devopps-taskboard:local python -m uvicorn reference.stage03:app --host 0.0.0.0 --port 8000 --no-access-log
```

`build` creates the runtime stage; `-t` gives it a local name; `.` is the build context. `run` starts one container; `--rm` removes that container after it stops, `--name` makes its identity explicit, and `-p 127.0.0.1:8000:8000` publishes only to host loopback. `0.0.0.0` **inside** the container lets Docker's network reach the app. It does not publish the host port globally. In a second terminal inspect `docker inspect devopps-memory --format '{{.Config.User}}'`; expect `10001:10001`. `docker stop devopps-memory` requests graceful termination. The memory data is intentionally lost.

## Weeks 6–7: real PostgreSQL and two users

```bash
python tools/init_lab.py
docker compose up --build -d app
docker compose ps
```

The first command creates `.env` once using unpredictable local credentials without printing them; it refuses to overwrite an existing file. Keep `.env` outside Git and screenshots. Compose reads it automatically. `up --build -d app` builds the application and starts its dependencies in the background: database health, a successful explicit migration, then the app. `ps` shows container state. Only the app publishes a loopback port; neither PostgreSQL server publishes one. The internal network carries app/database traffic. The development database uses a named volume; the separate test database is disposable.

Default `TASKBOARD_STAGE=07` enables the two identities. For week 6, edit that one line in `.env` to `TASKBOARD_STAGE=06`, then run `docker compose up -d --force-recreate app`; this recreates only the app with the changed stage and preserves the database volume. Before week 7, set it back to `07` and recreate the app again. Stage 6 tasks stay owned by `local-student` and disappear from Alice/Bob's view by design. No migration silently transfers ownership. Create new disposable records as each identity.

Inspect `migrations/001_tasks.sql`: UUID primary key, owner, constrained title and consistent completion timestamps. `002_owner_order.sql` adds a compatible owner/order index. `python -m reference.migrate` reads `DATABASE_URL`, applies missing migrations in one transaction, records checksums and refuses changed applied files. Compose runs this command in its `migrate` service. Do not put this command in every app startup; deployment should explicitly control schema changes. In this local lab the database owner also runs the app; a later private deployment should separate migration and restricted application roles.

```bash
source .env
curl -i -H "Authorization: Bearer $LAB_ALICE_TOKEN" -H 'Content-Type: application/json' -d '{"title":"Alice task"}' http://127.0.0.1:8000/tasks
curl -i -H "Authorization: Bearer $LAB_BOB_TOKEN" http://127.0.0.1:8000/tasks
curl -i http://127.0.0.1:8000/tasks
```

Only source the `.env` you generated and control: `source` executes shell content. It loads variables into this terminal; the commands expand tokens without printing them separately. Alice receives `201`. Bob's list excludes Alice's ID. The missing-token request returns `401` with `WWW-Authenticate: Bearer`. Framework `HTTPBearer` parses the credential; the app compares known opaque tokens and selects a server-owned identity. This is local teaching authentication, not a public login system. Keep the service local/private through later labs; public exposure requires an established identity provider and reviewed token validation/authorization.

```bash
docker compose --profile test run --build --rm integration
docker compose --profile test run --build --rm system
python tools/compose_drill.py
python tools/restore_check.py
```

`--profile test` enables the test services. `run --build --rm` builds the test image, executes the selected suite, propagates its exit code, and removes its one-off container. Integration tests use **real PostgreSQL** in database `taskboard_test`, with a newly named schema per case. The fixture rejects other database names and arbitrary hosts, and drops only its own schema. It proves SQL mapping, constraints, rollback, concurrent completion, migration upgrades and failed-migration recovery. System tests call the already-running app over HTTP and prove response bodies, status codes, ownership and state.

`compose_drill.py` operates only Compose project `devopps-taskboard`, creates a disposable task, completes it, restarts the app and database separately, and confirms identical data. It then stops just that database and proves task requests return `503` in under five seconds, readiness returns `503`, and liveness remains `200`. Its `finally` block restarts the database. Request deadlines, connection timeout, SQL statement timeout and lock timeout are all bounded. A deadline does not prove a creation failed to commit; automatic POST retries remain unsafe.

Before `restore_check.py`, pause other task writers so your comparison has a stable dataset. It streams `pg_dump` bytes directly into `pg_restore`, creates a new `taskboard_restore_<random>` database, and compares IDs, owner IDs, titles, completion flags and timestamps. It never overwrites the original database. The new database stays available for inspection. The script's row comparison proves database recovery; serving that restored database and running authenticated HTTP tests is the additional week-42 exercise. A logical dump is not point-in-time recovery and does not include all PostgreSQL global objects.

To inspect the restored destination, copy its **actual generated name** from `reports/restore.json` into `RESTORE_DB` after checking it starts with `taskboard_restore_`. Then run `docker compose exec db psql -U taskboard -d "$RESTORE_DB" -c 'SELECT id, owner_id, title, completed FROM tasks ORDER BY id;'`. Only after inspection, remove that one disposable restore using `docker compose exec db dropdb -U taskboard "$RESTORE_DB"`. Never substitute `taskboard` as the cleanup name.

## GitLab: build one artifact and retain its identity

`ci/gitlab-ci.yml` is an example for a dedicated repository whose root contains this folder's files. Copy it to `.gitlab-ci.yml` only in that repository. It has real unit, integration, image build, and system jobs. GitLab supplies `CI_REGISTRY`, `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD`, `CI_REGISTRY_IMAGE`, and commit identifiers for its registry; no invented account credentials are required. The Postgres service credential exists only inside its disposable test job.

The image build/system jobs run only on the protected default branch; merge requests receive lint/unit/integration checks without privileged image jobs. The `isolated-docker-tls` runner tag is an explicit prerequisite, not a magic hosted service. A runner administrator must provide an **ephemeral isolated runner** configured for Docker-in-Docker, privileged service execution and a `/certs/client` shared certificate volume. The job connects to `docker:2376` with TLS. Do not attach a privileged build runner to an untrusted shared host, and do not make unreviewed forks eligible for protected deployment credentials. If your runner cannot provide this, run the ordinary unit/integration jobs first and document image jobs as pending. The sample requires the registry to be enabled.

Build produces a runtime image once, pushes the commit tag, resolves its registry digest and passes that exact `IMAGE_REF` through a declared dotenv artifact. System testing pulls and starts that digest; its separately built test-runner image is never the deployed app. A successful test produces `tested-digest.txt`. The manual `promote_record` job is available only for a protected default branch and records approval; it deliberately does not claim to deploy to a host that has never been configured. Week 12 must add your private target, environment ownership, rejection of stale jobs, smoke checks and rollback. `resource_group` serializes concurrent jobs; it alone does not reject an older job executed later.

Recovery uses a previous **tested digest**, not a fresh rebuild of an old commit. Set `TASKBOARD_IMAGE` in your controlled `.env` to the recorded `repository@sha256:...`, run `docker compose pull app migrate`, run migrations only after reviewing compatibility, and use `docker compose up -d --no-build app`. Verify `/version`, the selected digest and business smoke behavior. An image rollback cannot restore deleted database columns or data: review expansion/backfill/removal history and select a forward fix or an isolated restore when necessary.

## Cleanup and retained evidence

```bash
docker compose --profile test stop
```

This stops only the named project's containers and preserves the development volume and your evidence. To remove stopped containers/network while keeping task data, run `docker compose --profile test down` without `--volumes`. Do not add `--volumes` casually: it would delete this lab's task database. Your `.env`, code, reports and database may be deliberately retained for the next lesson. `deactivate` leaves the Python virtual environment in this terminal; it does not delete files.

## Verification recorded during authoring

- Python 3.14.3 on Windows: **38 unit and in-process HTTP checks passed**.
- Real loopback Uvicorn stage-3 server: **10 system checks passed; 1 authentication case skipped intentionally** because stage 3 has no credentials.
- Shared stage-7 HTTP adapter with an explicitly injected memory store: **11 real HTTP checks passed**, including two-user isolation. This does not establish PostgreSQL-backed stage-7 behavior. A 2-second load-harness smoke had zero errors; it is not the required five-minute performance assessment.
- The starter validator is deliberately unfinished; its failing tests are a learner checkpoint, not a claimed passing reference.
- The host has no operational Docker daemon or WSL distribution. **PostgreSQL integration, Linux image builds, Compose lifecycle/restore, and GitLab execution are not yet verified here.** They are supplied executable exercises, not fabricated passes. Record their actual outputs on your Docker-capable lab before declaring the corresponding gates passed.
- The installed Starlette version emits a deprecation notice for its `httpx` test-client adapter; current checks pass. This affects only in-process reference tests, not the runtime listener or real HTTP system suite. Review that dependency interface on the next lock update.

## Primary references

- [FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/) — schema validation at the HTTP boundary.
- [FastAPI error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/) — intentional exception responses.
- [FastAPI security reference](https://fastapi.tiangolo.com/reference/security/) — maintained bearer parsing; the token-to-owner mapping is explicitly a teaching addition.
- [Psycopg transaction management](https://www.psycopg.org/psycopg3/docs/basic/transactions.html) — context-managed commit/rollback.
- [PostgreSQL constraints](https://www.postgresql.org/docs/17/ddl-constraints.html) and [SQL dumps](https://www.postgresql.org/docs/17/backup-dump.html) — invariants and logical backup limitations.
- [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) — readiness versus process startup.
- [GitLab Docker builds](https://docs.gitlab.com/ci/docker/using_docker_build/), [artifacts](https://docs.gitlab.com/ci/jobs/job_artifacts/), and [deployment safety](https://docs.gitlab.com/ci/environments/deployment_safety/) — runner prerequisites, explicit artifact flow and stale-deployment controls.
