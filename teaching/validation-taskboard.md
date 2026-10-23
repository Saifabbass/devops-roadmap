# Taskboard and assigned lesson validation — 2026-10-20

Scope: labs/taskboard plus teaching/lessons/week-03.json and week-41.json through week-52.json. User explicitly approved expanding lessons while preserving the current design.

## Executed evidence

- Python 3.14.3 isolated environment on D:. `pip check`: no broken requirements.
- `python -m pytest tests/unit tests/contract -q`: 38 passed. The installed Starlette/httpx in-process adapter emits one deprecation notice; it does not affect the real listener.
- `python tools/run_local_system.py`: real loopback stage03 HTTP, 10 passed/1 intentional authentication skip.
- Shared stage07 HTTP adapter using an explicitly injected MemoryStore and real loopback Uvicorn: 11 system tests passed, including two-user ownership and rejected mutations. This is not a PostgreSQL stage07 claim.
- Bounded load helper smoke against that private memory listener: 20 tasks, 2 clients, 1 second warmup/2 seconds measurement; 2151 measured requests, zero errors. This validates the helper only, not the formal 60/300-second workload or a production performance claim.
- `doctor.py --stage 03` passed; a separate invalid stage07 environment file failed with actionable messages without token values.
- `init_release.py` produced an explicitly incomplete record; `release_gate.py` returned nonzero and BLOCK messages as required.
- Exact requested lint: Ruff 0.11.13, target py312, E9/F63/F7/F82 over reference/starter/tools passed.
- Compose and GitLab YAML parsed with PyYAML; every script/before_script/after_script entry is a string. Corrected literal-newline shell escape defects before final parse.
- 126 Bash lesson command snippets parsed with Git Bash `bash -n`; 12 embedded Python blocks compiled; 2 embedded YAML blocks parsed. No syntax errors remained. This is syntax validation, not infrastructure execution.
- Required content structure checked for all13 assigned lessons: concepts, steps, command explanations, checkpoints, bounded failure/hints/recovery, at least3 questions, independent exercise, cleanup, references and repository connections. Capstones present for44/48/52.

## Explicitly not executed here

No operational Docker daemon or WSL distribution was available on the authoring host. Real PostgreSQL integration (constraints, rollback, concurrency, migration upgrades), Linux container build, Compose lifecycle/restore, GitLab pipeline, Kubernetes/VM/provider exercises are supplied but unexecuted. Their corresponding learner gates must not be marked passed from Python/memory tests. No paid cloud resources were created.

The PostgreSQL test fixture refuses arbitrary hosts/database names and drops only its random schema inside taskboard_test. Restore checks always create a separate destination and compare all stored task fields. The supplied CI retains lint/unit/integration gates, restricts privileged image jobs to the protected default branch, builds runtime once, tests its digest and records promotion; a target-specific deployment job remains the earlier delivery lesson's responsibility.

## Source verification

Official FastAPI/Pydantic/Psycopg, PostgreSQL17, Docker Compose and GitLab docs were consulted for boundaries and commands. Actual runtime/test versions were resolved from PyPI and locked. Public Docker registry manifests verified the Python3.14/Postgres17/Docker28 digests in shipped files and kind1.35.0/1.35.1 digests in lesson46. Hard Way prerequisite/jumpbox source was inspected: four Debian12 machines; its sampled binary list includes older/prerelease components. Lessons state the exact completed/unfinished scope and do not present that list as a current production recommendation.

## Publication exclusions

Do not package labs/taskboard/.venv, .tmp, reports, .pytest_cache, __pycache__, .env, private keys or database dumps. .tmp contains authoring scripts and syntax-check scratch files; final lesson JSON files contain the final corrections and must not be overwritten by rerunning those authoring scripts.

## Known evidence boundaries

The source-only template is not a data backup. Archive SHA256, local imageID and OCI registry digest are distinguished. The release gate checks evidence completeness/checksums/JUnit outcomes, not report authenticity or full threat coverage. Short closed-loop performance samples do not establish long-window availability. Local component replacement does not prove an in-place production cluster upgrade; the lessons label that distinction.
