# Independent execution and deployment audit

Scope: lessons 01, 02 and 04-12; deployment helper and README; final fixes to assigned lesson 03 and 41-52. Current design and original curriculum sequence are unchanged.

## Executed checks

- 14 deterministic deployment tests passed on Windows/Python 3.14.3, then all 14 passed with Python optimization enabled. The tests include multiple negative cases per test. All Docker subprocesses and HTTP calls are replaced. The Windows-only fcntl import stub does not claim Linux locking was tested.
- Full controller flows cover successful deployment, config-only releases, failed deployment, failed rollback, recovery retry, interrupted deployment, stale deployment/rollback rejection, same-pipeline digest substitution rejection, wrong running-image rejection, private Compose layout checks and refusal to discard legacy state.
- 234 Bash command blocks passed Git Bash `bash -n`; 28 embedded Python programs passed AST parsing; 6 embedded YAML documents parsed with PyYAML. Counts cover all owned lessons 01-12 and 41-52 after the principal audit changes. The small final guard/test-selection corrections were parsed again individually.
- Executed week 11's actual prompt/heredoc block using synthetic input in a temporary folder. The default subject includes `:ref:` and ref_protected is the documented string value.
- Executed week 8 cleanup with the forbidden source database name and week 42's SQL fault with an invalid UUID. Both exited nonzero before a stubbed Docker command could be reached. No actual database or deletion command was executed.
- UTF-8 JSON scan confirms no remaining known mojibake markers in assigned 03/41-52; preserved already-correct Unicode and repaired joined learner prose without changing code identifiers.

## Corrections

Command guards now stop on reserved-path collisions, failed edits/install prerequisites, failed release checks, invalid disposable database names and invalid UUIDs. Setup describes the actual VM/source directory, Docker group session refresh and resumed dedicated runner. Week 11 no longer calls input() while stdin is occupied by its Python here-document. Its default OIDC subject and protected-ref type match the current official GitLab payload documentation.

The helper uses a single atomic state.json ledger, records the recovery destination through interrupted/failed rollback, rejects stale or substituted artifacts, checks the resolved private Compose layout and verifies the actual running image ID against the pulled tested digest. Operational checks remain enabled under Python -O. Configuration-only releases retain their previous configuration. The README explains prerequisites, job inputs, ledger/recovery behavior and limits.

Week 42 now supplies an old/new reader compatibility experiment: the next query genuinely requires operator_note while preserving public API 1.0, rejects old schema readiness, then both images run the same HTTP suite against the expanded isolated database. It also includes a scoped user timer and exact-name three-snapshot retention example. These operations remain unexecuted on this host.

Week 50 builds/selects and records one clean-source candidate before testing, verifies the running image ID, builds the separate test runner explicitly, gathers system evidence without replacing app, and binds that exact candidate to the dossier. Failed suite exits are retained even while copying their JUnit reports.

## Not executed

No operational Docker daemon, Linux/WSL environment, PostgreSQL, systemd user manager or live GitLab deployment was available. Compose canonical-model validation is tested using explicit fixtures, not claimed as real Compose rendering. Real database, migration, container, systemd scheduling, VM, registry, cloud and provider exercises require learner execution. No paid cloud resources were created. Do not infer production readiness from local guard tests or syntax checks.

Current primary references checked during audit: GitLab ID-token payload documentation, Docker Compose config/run documentation and systemd.timer documentation. Relevant links are included in the lesson reference sections.
