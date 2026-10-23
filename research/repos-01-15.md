# DevOps repository audit: entries 1-15

Reviewed on 2026-10-20. The numbering follows the assigned FindARepo snapshot order; it is not a quality ranking. Week mappings assume 14 hours per week and the agreed AWS-first, GCP-second curriculum. Recommendations are learning-design judgments, not upstream promises.

Inspection scope: primary repository landing pages and README sections were reviewed for every entry, with the additional files and official documentation linked under each entry. No repository code, installer, test suite or deployment was executed. This is a suitability and documentation review, not a security audit, benchmark or complete code review. Branch URLs move; pin a reviewed release when starting each lab and check current advisories. Website retrieval may use cached copies. A test workflow being present is not evidence that it passed.

Use Core lab entries in the main project, Focused lab entries for a bounded exercise, Reference entries for decisions, Optional entries only after milestones are met, and Defer entries only if the specialization becomes relevant. The goal is to learn transferable engineering decisions without operating all 30 tools.

## 1. kestra-io/kestra

**Optional — Weeks 45-48, after GitLab CI, cloud identity and incident handling.** Coordinate scheduled and event-driven workflows with declarative configuration. Use it to study durable operational automation: retries, timeouts, idempotency and partial failure. A second workflow platform is unnecessary until the GitLab delivery pipeline and basic scheduled jobs are understood. The README describes YAML workflows and retry/error-handling primitives. The sampled Compose file uses PostgreSQL, persistent storage and a health dependency; its comments explicitly identify root access to the Docker socket as a development configuration. [Primary repository](https://github.com/kestra-io/kestra).

**Learning deliverable:** Build a disposable backup-validation workflow with an explicit timeout, bounded retries and a failure notification to a local test receiver. Trigger the same input twice and prove it cannot overwrite a good backup or create duplicate side effects. Produce a workflow diagram and failure timeline.

**Operational caution:** Do not copy the quick start into production: it uses mutable image tags, sample database credentials and Docker socket access. Enterprise features and community features differ. Workflow success is not proof that the business result is correct.

**Inspected sources:**

- [github.com/kestra-io/kestra](https://github.com/kestra-io/kestra)
- [raw.githubusercontent.com/kestra-io/kestra/develop/docker-compose.yml](https://raw.githubusercontent.com/kestra-io/kestra/develop/docker-compose.yml)

## 2. databasus/databasus

**Focused lab — Weeks 23-24 first restore exercise; weeks 41-44 recovery comparison.** Schedule database backups and validate restores. The useful lesson is recoverability, not operating a backup dashboard. Start with a manual PostgreSQL dump and restore, then compare what automation adds and what it cannot prove. The README documents logical and physical backups, WAL/PITR support, retention settings and restore verification. It also warns that the application's encryption key must be backed up to recover encrypted backups. [Primary repository](https://github.com/databasus/databasus).

**Learning deliverable:** Seed a disposable database with known records, back it up, deliberately remove only the lab database, restore into a separate clean instance, and run application-level assertions. Record measured recovery time, missing transactions, retention behavior and encryption-key recovery steps.

**Operational caution:** A successful restore job or row count does not prove application consistency. Protect backup credentials and encryption keys separately; keep tests isolated from real data. CI/security assurances in the README were read, not independently reproduced.

**Inspected sources:**

- [github.com/databasus/databasus](https://github.com/databasus/databasus)
- [raw.githubusercontent.com/databasus/databasus/main/README.md](https://raw.githubusercontent.com/databasus/databasus/main/README.md)

## 3. floci-io/floci

**Focused lab — Weeks 7-8 test isolation; repeat against real AWS in weeks 13-16.** Emulate AWS interfaces locally for development and automated integration tests. Use one narrowly scoped storage or queue integration to learn endpoint injection and reproducible fixtures. The local emulator keeps the rapid feedback loop inexpensive; real-cloud checks establish the compatibility boundary. The README includes AWS SDK endpoint configuration and Python, Java and Node Testcontainers examples. It says default credentials can be arbitrary non-empty values unless stricter checks are enabled, and some service modes start real Docker containers. [Primary repository](https://github.com/floci-io/floci).

**Learning deliverable:** Write upload/download and missing-object tests against isolated S3 emulation. Inject the endpoint through configuration, use fake local credentials and clean up fixtures. Later run the same contract suite against a temporary AWS bucket, including an explicit access-denied case, and document differences.

**Operational caution:** Passing emulator tests does not validate real IAM, regional behavior, quotas, networking, billing or managed-service availability. Do not claim complete AWS parity from the supported-service list. Avoid mounting the Docker socket unless the chosen test requires it.

**Inspected sources:**

- [github.com/floci-io/floci](https://github.com/floci-io/floci)
- [raw.githubusercontent.com/floci-io/floci/main/README.md](https://raw.githubusercontent.com/floci-io/floci/main/README.md)

## 4. rorkai/App-Store-Connect-CLI

**Defer — Weeks 45-48 reading exercise; implementation only for a mobile platform role.** Automate Apple application release workflows through a command-line interface. This is a specialization, not a missing prerequisite for AWS/GCP DevOps. Extract reusable release-engineering ideas without buying Apple tooling or building an unrelated application. The README documents structured output, authentication diagnostics and release automation. The CI guide includes GitLab components, fresh macOS-runner signing steps and an AWS workload-identity example for object storage. [Primary repository](https://github.com/rorkai/App-Store-Connect-CLI).

**Learning deliverable:** Read the release workflow and draft a generic GitLab release-job checklist: validate inputs, pin dependencies, use machine-readable output, protect signing material, require a release approval and clean temporary credentials. Apply those principles to the existing container release.

**Operational caution:** Real mobile signing and release work has platform/account prerequisites and can publish externally. The inspected CI snippets use floating refs; pin reviewed versions in your own examples. The README documents default usage telemetry.

**Inspected sources:**

- [github.com/rorkai/App-Store-Connect-CLI](https://github.com/rorkai/App-Store-Connect-CLI)
- [raw.githubusercontent.com/rorkai/App-Store-Connect-CLI/main/README.md](https://raw.githubusercontent.com/rorkai/App-Store-Connect-CLI/main/README.md)
- [raw.githubusercontent.com/rorkai/App-Store-Connect-CLI/main/docs/CI_CD.md](https://raw.githubusercontent.com/rorkai/App-Store-Connect-CLI/main/docs/CI_CD.md)

## 5. go-gitea/gitea

**Reference — Weeks 45-48 platform comparison.** Self-host Git collaboration, code review, packages and automation. Use its operational documentation to understand the responsibilities hidden by hosted source control. Keep GitLab as the primary delivery platform; use a disposable Gitea instance only if time remains. The README describes an integrated development service with GitHub-Actions-compatible CI. The backup documentation explains that database, files and repositories can become inconsistent and instructs stopping the instance for its documented consistent backup procedure. [Primary repository](https://github.com/go-gitea/gitea).

**Learning deliverable:** Write a source-control service recovery plan covering repositories, database, attachments, configuration and credentials. Optionally restore a throwaway instance and prove a clone, commit history and issue attachment survive. Compare the maintenance burden with the GitLab service used in the course.

**Operational caution:** A Git repository mirror is not a complete platform backup. Gitea Actions syntax and runner behavior do not teach GitLab CI directly. Avoid expanding this comparison into a second permanent CI platform.

**Inspected sources:**

- [github.com/go-gitea/gitea](https://github.com/go-gitea/gitea)
- [docs.gitea.com/administration/backup-and-restore/](https://docs.gitea.com/administration/backup-and-restore/)

## 6. netdata/netdata

**Focused lab — Weeks 3-4 applied Linux diagnosis; revisit weeks 33-36.** Observe host, container and service resource behavior. Its immediate feedback helps connect processes and kernel counters to application latency. Use it for a short diagnosis lab, then retain only the observability stack selected for the capstone. The README describes collection, storage and alerting in the Agent and lists host/container monitoring. The security/privacy documentation distinguishes observability data from metadata sent to Cloud and documents anonymous usage statistics. [Primary repository](https://github.com/netdata/netdata).

**Learning deliverable:** Create controlled CPU pressure and a slow-disk scenario inside a disposable VM. Correlate latency with CPU, memory, disk and network charts and verify the diagnosis with Linux tools. Write a two-page incident note containing the failed hypothesis as well as the final cause.

**Operational caution:** A dashboard does not supply an SLO or prove causality. Measure collector overhead in the lab rather than accepting marketing performance claims. Review dashboard exposure, host access and telemetry settings; Agent, UI and Cloud have different licensing and service boundaries.

**Inspected sources:**

- [github.com/netdata/netdata](https://github.com/netdata/netdata)
- [learn.netdata.cloud/docs/security-and-privacy-design](https://learn.netdata.cloud/docs/security-and-privacy-design)

## 7. Dokploy/dokploy

**Optional — Weeks 45-48, after manual VM/container delivery and Kubernetes.** Operate a self-hosted application deployment platform. Study the developer experience a platform team should provide: repeatable deployment, logs, backups and rollback. Compare those conveniences with the infrastructure and operational responsibilities underneath. The README describes Docker Compose, Docker Swarm multi-node operation, Traefik routing and backups. The inspected license file applies Apache 2.0 outside a proprietary-directory carve-out. [Primary repository](https://github.com/Dokploy/dokploy).

**Learning deliverable:** Trace the deployment of the capstone app on paper: source, image build, registry, secrets, routing, storage, health checks and recovery. Produce an architecture decision record comparing your GitLab/Terraform/Ansible path with Dokploy; optionally repeat on a disposable VM.

**Operational caution:** Swarm-based operation is not Kubernetes practice. One-click deployment does not establish backup correctness, least privilege or high availability. The installer is powerful host-changing code; inspect and pin a release before any future lab execution.

**Inspected sources:**

- [github.com/Dokploy/dokploy](https://github.com/Dokploy/dokploy)
- [raw.githubusercontent.com/Dokploy/dokploy/canary/LICENSE.MD](https://raw.githubusercontent.com/Dokploy/dokploy/canary/LICENSE.MD)

## 8. getsentry/sentry

**Optional — Weeks 33-36, after basic logs, metrics and tracing.** Connect application errors and performance problems to code changes. Use one instrumented service to learn release attribution and safe error reporting. Running a full Sentry platform is a separate operating challenge and is not required to learn the concept. The README links language SDKs for error debugging. The self-hosted repository describes its package as intended for low-volume deployments and proofs of concept. The current main-repository license identifies FSL-1.1-Apache-2.0. [Primary repository](https://github.com/getsentry/sentry).

**Learning deliverable:** Introduce a controlled exception in staging, attach release/environment metadata, diagnose it from the recorded event, ship a fix and verify the regression test. Demonstrate that a fake password and access token are removed before telemetry leaves the process.

**Operational caution:** Do not treat the whole repository as permissively licensed open source. Error events can carry sensitive application data. The self-hosted documentation site was unavailable during this inspection; no resource sizing or deployment reliability was verified.

**Inspected sources:**

- [github.com/getsentry/sentry](https://github.com/getsentry/sentry)
- [raw.githubusercontent.com/getsentry/sentry/master/LICENSE.md](https://raw.githubusercontent.com/getsentry/sentry/master/LICENSE.md)
- [raw.githubusercontent.com/getsentry/self-hosted/master/README.md](https://raw.githubusercontent.com/getsentry/self-hosted/master/README.md)

## 9. nektos/act

**Reference — Weeks 9-12, brief CI portability comparison.** Run supported GitHub Actions workflows locally using containers. Learn the distinction between a local job rehearsal and a provider's control plane. Your target is GitLab, so the main exercise belongs in GitLab's own pipeline validation and real runner execution. The README says act reads .github/workflows and runs through Docker. Its limitations page says job permissions, environment scoping, concurrency and several timeout behaviors are ignored, and OIDC URLs are not provided. [Primary repository](https://github.com/nektos/act).

**Learning deliverable:** Read one simple upstream GitHub workflow and translate its lint/test/build intent into GitLab jobs. Write a parity table for jobs, artifacts, caches, identity, approvals and concurrency. Optionally use act only on a reviewed workflow with fake credentials.

**Operational caution:** act is not a GitLab CI emulator. A successful local run cannot validate hosted authorization, environment approvals or deployment concurrency. Workflows execute code with the access you grant the runner; inspect them before running.

**Inspected sources:**

- [github.com/nektos/act](https://github.com/nektos/act)
- [nektosact.com/not_supported.html](https://nektosact.com/not_supported.html)

## 10. argoproj/argo-cd

**Core lab — Weeks 29-32, after Kubernetes workloads, networking, storage and RBAC.** Reconcile Kubernetes application state from version-controlled desired configuration. This is a strong fit once you can deploy and troubleshoot the app manually. GitLab remains responsible for validation and building the artifact; Argo CD teaches continuous reconciliation and controlled promotion. The README defines Argo CD as Kubernetes GitOps delivery. The auto-sync documentation distinguishes sync, self-healing and pruning; pruning is disabled by default, and direct rollback is unavailable while automated sync is enabled. [Primary repository](https://github.com/argoproj/argo-cd).

**Learning deliverable:** Have GitLab publish an immutable image and propose its digest in an environment repository. Review and merge, observe reconciliation, introduce a harmless replica-count drift, compare self-heal off/on, and revert a bad release through Git. Save timeline evidence and a rollback runbook.

**Operational caution:** Pruning can delete resources and self-heal can overwrite emergency manual edits. Start in an isolated namespace with restrictive access. A Git revert of application manifests does not reverse an incompatible database migration.

**Inspected sources:**

- [github.com/argoproj/argo-cd](https://github.com/argoproj/argo-cd)
- [argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)

## 11. pranshuparmar/witr

**Focused lab — Weeks 1-4 diagnostic validation; repeat during incident drills.** Trace processes, ports and containers back to their launch chain. Use it as a cross-check after solving the same mystery with native tools. The lasting skill is reasoning about processes, service managers, parent-child relationships and namespaces. The README documents process/port/container tracing, JSON output and a TUI. Its platform matrix and permissions section describe visibility differences and elevated access requirements; the TUI also includes process actions. [Primary repository](https://github.com/pranshuparmar/witr).

**Learning deliverable:** Create a harmless service that keeps restarting and a second service with a port conflict. Identify the owner and launch chain using ps, ss, lsof and systemctl, then compare witr's report. Deliver a runbook that fixes the service definition instead of repeatedly killing a child process.

**Operational caution:** Treat diagnostic output as sensitive because environment and process details may contain secrets. Use inspection operations only during the first exercise; TUI process actions are not read-only. Windows and WSL visibility differ from a Linux server.

**Inspected sources:**

- [github.com/pranshuparmar/witr](https://github.com/pranshuparmar/witr)
- [raw.githubusercontent.com/pranshuparmar/witr/main/README.md](https://raw.githubusercontent.com/pranshuparmar/witr/main/README.md)

## 12. getsops/sops

**Core lab — Weeks 11-12 local age lab; weeks 17-20 AWS KMS; weeks 37-40 GCP KMS.** Keep structured configuration encrypted while managing who can decrypt it. It connects Git hygiene, identity and cloud key management without requiring a large secrets platform. Learn the difference between encrypting a file, authorizing decryption and rotating the underlying application secret. The README lists structured formats and AWS KMS, GCP KMS, age and other key backends. The official docs expose usage and security-model sections; the repository includes examples and functional-test directories. [Primary repository](https://github.com/getsops/sops).

**Learning deliverable:** Encrypt fake configuration with age and prove an unauthorized key cannot decrypt it. Later use a tightly scoped cloud identity with KMS, test a denied identity, rotate a recipient, and recover using an approved backup identity. Verify plaintext never appears in CI logs or retained artifacts.

**Operational caution:** Encryption at rest does not protect plaintext after decryption. Removing a recipient cannot erase old Git history or revoke a secret already seen; rotate the actual secret when access is lost. Do not assume Argo CD automatically decrypts SOPS files without a reviewed integration.

**Inspected sources:**

- [github.com/getsops/sops](https://github.com/getsops/sops)
- [getsops.io/docs/](https://getsops.io/docs/)
- [getsops.io/docs/usage/](https://getsops.io/docs/usage/)
- [getsops.io/docs/security/](https://getsops.io/docs/security/)

## 13. SigNoz/signoz

**Focused lab — Weeks 33-36 observability; choose one backend for the capstone.** Explore application telemetry through OpenTelemetry logs, metrics and traces. Make the transferable skill OpenTelemetry instrumentation and diagnosis. Use SigNoz as one possible backend rather than maintaining several overlapping observability products for a one-person course. The README describes an OpenTelemetry-based platform with logs, metrics, traces and alerts, with community and enterprise offerings. The license applies MIT terms outside specified enterprise directories and third-party components. [Primary repository](https://github.com/SigNoz/signoz).

**Learning deliverable:** Instrument an HTTP request and a database call, propagate a trace identifier, inject a slow query and locate the latency in a trace. Correlate the trace with a structured log and an error-rate metric, then set a justified sampling and retention policy.

**Operational caution:** Telemetry volume, retention and cardinality consume real storage and compute. Do not assume enterprise access controls exist in the community edition. Redact sensitive attributes before export and keep the ingestion endpoint private.

**Inspected sources:**

- [github.com/SigNoz/signoz](https://github.com/SigNoz/signoz)
- [raw.githubusercontent.com/SigNoz/signoz/main/LICENSE](https://raw.githubusercontent.com/SigNoz/signoz/main/LICENSE)

## 14. TwiN/gatus

**Core lab — Weeks 7-8 basic checks; weeks 33-36 external monitoring.** Run synthetic endpoint checks and report service status. It makes the distinction between a running process and a working user journey concrete. Begin with one simple HTTP contract; later place checks outside the application's failure domain. The README provides HTTP/TCP/DNS checks, conditions, alerts, authentication and deployment examples. The sampled GitHub test workflow builds the binary and runs Go tests with the race detector; ICMP testing requires elevation in that workflow. [Primary repository](https://github.com/TwiN/gatus).

**Learning deliverable:** Check status code, expected response content and a justified latency threshold. Break DNS, return a misleading HTTP 200 and stop the app in separate drills. Prove each failure is detected, recovery clears it, and notification thresholds avoid repeated noise.

**Operational caution:** Synthetic checks complement rather than replace unit, integration and whole-system tests. A monitor inside the same failed cluster may vanish with the app. Keep credentials out of public check output, and do not make alpha workflow suites a core dependency.

**Inspected sources:**

- [github.com/TwiN/gatus](https://github.com/TwiN/gatus)
- [raw.githubusercontent.com/TwiN/gatus/master/README.md](https://raw.githubusercontent.com/TwiN/gatus/master/README.md)
- [raw.githubusercontent.com/TwiN/gatus/master/.github/workflows/test.yml](https://raw.githubusercontent.com/TwiN/gatus/master/.github/workflows/test.yml)

## 15. awesome-foss/awesome-sysadmin

**Reference — Weeks 1-52, only when answering a specific operational need.** Discover categorized system-administration tools and their upstream projects. Treat it as a directory for comparing options, not a syllabus or installation queue. It is useful when you can state the problem, constraints and acceptance criteria before opening a category. The README groups projects into categories including configuration management, CI/CD, backup and monitoring; entries provide upstream links and license/language labels. It includes Ansible, GitLab CI and Argo CD in the inspected sections. [Primary repository](https://github.com/awesome-foss/awesome-sysadmin).

**Learning deliverable:** Choose a genuine requirement, such as configuration management or external monitoring. Compare three candidates on maintenance, licensing, access control, backup/recovery, resource costs and integration effort. Write a one-page decision record that explains why you rejected two.

**Operational caution:** Directory inclusion is not a security audit or proof that a project is still maintained. Follow the upstream documentation and verify the current license/version before adopting a tool. Limit browsing so it does not replace building and debugging.

**Inspected sources:**

- [github.com/awesome-foss/awesome-sysadmin](https://github.com/awesome-foss/awesome-sysadmin)

