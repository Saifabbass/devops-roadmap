# Private Taskboard deployment lab

This Linux helper implements week 12's single-host private staging exercise. Read the lesson before running it. It selects an already tested registry digest; it does not create a cloud account, VM, runner, database backup, identity provider or public endpoint.

## Prerequisites and preparation

Use a dedicated disposable Ubuntu 24.04 staging VM with Python 3, Docker Engine and Compose v2. The VM's project-locked **Protected shell executor** runner uses tag `private-staging-shell`; disable untagged jobs. Only reviewed protected-default-branch jobs may run here. Docker-group membership controls the host daemon and is unsuitable for an untrusted merge-request runner.

Follow week 12 to create `/opt/devopps-staging`, owned by `gitlab-runner` with mode 0700, and generate its private `.env` with Taskboard's `tools/init_lab.py`. Do not overwrite an existing target to repeat setup. The source Compose file must retain the bundled app/migrate/db layout: stage 07, app published only at `127.0.0.1:8000`, internal backend network, database without host publication and volume `devopps-staging_taskboard-data`.

Copy `deploy_private.py` to `tools/deploy_private.py` in the dedicated application repository. Add the complete week-12 manual jobs to the week-10 pipeline. The deploy job downloads `tested-digest.txt` from its successful system job. It must use the same pipeline's source Compose file. Keep the runner restriction, GitLab outdated-deployment setting and `resource_group: private-staging`.

## Invocation inside the configured CI job

Run from the checked-out application root:

```sh
python3 tools/deploy_private.py deploy --image-file tested-digest.txt --compose compose.yaml
```

GitLab supplies the real `CI_PIPELINE_ID`, `CI_COMMIT_SHA`, `CI_REGISTRY_IMAGE`, `CI_REGISTRY`, `CI_REGISTRY_USER` and `CI_REGISTRY_PASSWORD`. After reviewing current/previous schema compatibility, supply `SCHEMA_COMPATIBLE=yes` for that specific manual job. This acknowledgment is not an automated compatibility proof. Do not print credentials or make the acknowledgment an unconditional permanent variable.

The helper resolves Compose privately, verifies app and migration image references, removes build directives from the temporary runtime model, pulls the exact project digest, waits for the database and runs migrations explicitly. It then starts the app without building, compares its actual container image ID with the pulled artifact, and checks readiness, authentication, owner isolation, task completion, idempotence and commit metadata through real loopback HTTP. Synthetic smoke tasks remain as evidence.

Expanded Compose contains credentials. It is kept only in the private temporary directory alongside a temporary Docker credential configuration and removed on normal exit. Never print or archive it. Abrupt host failure can leave private temporary directories; inspect them locally after stopping any active deployment.

## State and recovery

The canonical ledger is `/opt/devopps-staging/state.json`. It records the approval watermark, current known-good release, previous release, current attempt and selected recovery release. Related fields are replaced together under a Linux file lock. A newer approval prevents older queued jobs from deploying even when the newer release fails. A same-pipeline retry cannot change its approved digest.

From the same or a newer protected pipeline, after schema review:

```sh
python3 tools/deploy_private.py rollback
```

After a failed or interrupted deploy, rollback selects the recorded good release. After a completed deploy it selects the previous release. A failed/interrupted rollback retries its recorded destination, and repeated successful rollback is idempotent. The saved Compose text accompanies its image; configuration-only releases also preserve the previous configuration. Recovery does not run migrations, restore a dump, delete data, or create a guessed release when no recorded good artifact exists.

Inspect only the sanitized portion of the private ledger:

```sh
sudo -u gitlab-runner python3 -c "import json; from pathlib import Path; s=json.loads(Path('/opt/devopps-staging/state.json').read_text()); print(json.dumps({k:s[k] for k in ('attempt','watermark')},indent=2))"
```

Individual sanitized results are also written under `reports/PIPELINE_ID-deploy.json` or `reports/PIPELINE_ID-rollback.json`. A passed report includes the selected digest, actual runtime image ID, business result and timing. Report-write failure can make the CI job fail even after the atomic ledger recorded successful runtime verification; inspect both before repeating an operation.

Legacy separate `good.json`/`watermark.json` records cause refusal rather than silently resetting stale-job protection. This course version does not supply an automatic legacy migration. Do not erase state files to bypass a refusal.

## Tests and limits

From the extracted course root:

```sh
python -m unittest discover -s labs/delivery/tests -v
python -O -m unittest discover -s labs/delivery/tests -v
```

The deterministic tests replace Docker subprocesses and HTTP calls. On Windows only the import of `fcntl` uses a scoped stub. They exercise stale/substitution rejection, private configuration, runtime-image mismatch, configuration-only releases, interrupted deploys, failed recovery retries and the atomic ledger. They do **not** prove Linux locking, real Compose rendering, database migrations, live GitLab jobs or deployment on a VM. Run the actual week-12 exercise to establish those boundaries.

This is a single-host educational controller. Image rollback cannot reverse an incompatible schema change; human review, protected-runner administration, storage recovery and application testing remain separate responsibilities. Runtime service configuration is constrained to the bundled lab layout. It is not a general Compose policy engine or a distributed deployment service.

Stop only this project's containers and pause/stop its dedicated runner using the lesson cleanup. Preserve the database volume, private ledger and reviewed evidence until an explicit retention decision.
