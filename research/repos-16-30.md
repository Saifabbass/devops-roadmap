# DevOps repository audit: entries 16-30

Reviewed 2026-10-20. These entries follow the supplied Find a Repo snapshot order. This is a learning-fit and documentation inspection, not a code security audit, performance benchmark or production certification. Primary READMEs were read for every repository; additional files and official documentation are linked per entry. No repository code or installer was executed. Failed optional document fetches are explicitly identified below. Default-branch documents can change and sometimes describe unreleased behavior: pin a supported release and reopen its matching docs before a lab.

Recommendations assume a CS graduate comfortable with programming, Git and Linux, new to cloud/DevOps, with 14 hours per week. The aim is reusable engineering judgment, not 30 installations. Core labs belong inside existing lessons; focused labs are bounded exercises; optional tools replace a comparable extension; reference and deferred entries still yield a design artifact. Suggested exercises and acceptance evidence are original curriculum recommendations, not claims that the repository supplies a complete course.

| # | Repository | Decision | Placement |
|---|---|---|---|
| 16 | [bytebase/bytebase](https://github.com/bytebase/bytebase) | Focused lab | Week 42, after application migrations, GitLab CI and database backup basics |
| 17 | [kubernetes-sigs/headlamp](https://github.com/kubernetes-sigs/headlamp) | Focused lab | Week 28, after kubectl, Pods, Deployments, Services and RBAC |
| 18 | [cloudnative-pg/cloudnative-pg](https://github.com/cloudnative-pg/cloudnative-pg) | Focused lab | Weeks 41-44, after Kubernetes storage, PostgreSQL, failure domains and managed database concepts |
| 19 | [CISOfy/lynis](https://github.com/CISOfy/lynis) | Core lab | Week 4 baseline; weeks 21-24 automate selected fixes; week 41 reassess |
| 20 | [jenkinsci/jenkins](https://github.com/jenkinsci/jenkins) | Reference | Week 12, after a working GitLab CI pipeline |
| 21 | [woodpecker-ci/woodpecker](https://github.com/woodpecker-ci/woodpecker) | Reference | Week 12, in the CI architecture comparison |
| 22 | [go-task/task](https://github.com/go-task/task) | Core lab | Week 5 onward; reuse the same interface in GitLab CI in weeks 9-12 |
| 23 | [theonedev/onedev](https://github.com/theonedev/onedev) | Reference | Week 12 or week 45, as a platform comparison |
| 24 | [apache/apisix](https://github.com/apache/apisix) | Focused lab | Weeks 31-32 or 43, after HTTP, reverse proxies and Kubernetes Services |
| 25 | [psviderski/uncloud](https://github.com/psviderski/uncloud) | Defer | Week 45 design reading; hands-on exploration after the core capstone or in year two |
| 26 | [semaphoreui/semaphore](https://github.com/semaphoreui/semaphore) | Optional | Week 24, after Ansible CLI, inventories, roles and idempotence |
| 27 | [bunkerity/bunkerweb](https://github.com/bunkerity/bunkerweb) | Optional | Week 41, after HTTP/TLS, application authorization and baseline security tests |
| 28 | [OneUptime/oneuptime](https://github.com/OneUptime/oneuptime) | Reference | Weeks 33-36, after basic metrics, logs, traces and SLOs |
| 29 | [k8sgpt-ai/k8sgpt](https://github.com/k8sgpt-ai/k8sgpt) | Optional | Week 32 or 44, after manual troubleshooting competence |
| 30 | [freelensapp/freelens](https://github.com/freelensapp/freelens) | Optional | Week 28, only as an alternative to Headlamp |

## 16. bytebase/bytebase

**Focused lab — Week 42, after application migrations, GitLab CI and database backup basics.** Database change and access governance.

**Observed evidence.** The README describes SQL review, GitLab integration, change workflows, RBAC and policy APIs. LICENSE separates enterprise paths and enablement code from the MIT-licensed remainder.

**Learning exercise.** Design an expand/contract database change for the capstone. In a disposable PostgreSQL environment, prove that old and new app versions work during the expansion stage, rehearse the data migration and a forward fix, and record who can approve versus execute a change. Inspect Bytebase's workflow; install it only if the required controls are available in the chosen edition.

**Completion artifact.** A migration runbook, compatibility test results and a review/execute permission matrix.

**Operational caution and scope.** A migration rollback button is not proof that data can be recovered. Verify edition entitlements before depending on approval/access features. Avoid importing real database credentials into a learning installation.

**Timebox.** 2 hours of the database-change lesson; optional installation can replace another extension.

**Inspected:** [Primary source 1](https://github.com/bytebase/bytebase); [Primary source 2](https://raw.githubusercontent.com/bytebase/bytebase/main/LICENSE).

## 17. kubernetes-sigs/headlamp

**Focused lab — Week 28, after kubectl, Pods, Deployments, Services and RBAC.** A Kubernetes web or desktop interface for resources, logs and operations.

**Observed evidence.** The README documents desktop and in-cluster modes, multi-cluster access, logs/exec, and actions governed by Kubernetes RBAC. SECURITY.md links Kubernetes disclosure and security announcements.

**Learning exercise.** Use a namespace-scoped read-only identity in a disposable cluster. Trace Deployment to ReplicaSet to Pod and Service to endpoints in the UI, then reproduce every finding with kubectl. Confirm that the identity cannot edit workloads or read Secrets.

**Completion artifact.** A resource relationship sketch, matching CLI observations and denied-action evidence.

**Operational caution and scope.** A GUI inherits the power of its credentials. Do not give it cluster-admin merely to remove permission errors; do not publicly expose an administrative dashboard. Choose this or Freelens for the first year, not both.

**Timebox.** One 2-hour session.

**Inspected:** [Primary source 1](https://github.com/kubernetes-sigs/headlamp); [Primary source 2](https://raw.githubusercontent.com/kubernetes-sigs/headlamp/main/SECURITY.md).

## 18. cloudnative-pg/cloudnative-pg

**Focused lab — Weeks 41-44, after Kubernetes storage, PostgreSQL, failure domains and managed database concepts.** Operate PostgreSQL clusters through a Kubernetes operator.

**Observed evidence.** README explains reconciliation, primary election and rolling updates. The backup documentation describes base backups plus WAL, restore measurement, separate secret protection, and the transition from native Barman integration to CNPG-I plugins beginning in 1.26.

**Learning exercise.** In a disposable cluster, follow a release-matched quickstart, write timestamped records, observe primary/standby roles, and simulate a primary Pod failure. Separately back up and restore to a new cluster, verify rows and measure recovery time and data loss. Compare ownership with AWS RDS and Cloud SQL before selecting a database architecture.

**Completion artifact.** Separate failover and restore reports with measured RTO/RPO, checksums or row assertions, and an operator-versus-managed-service decision.

**Operational caution and scope.** Failover and backups solve different problems. A local multi-Pod cluster does not demonstrate availability-zone resilience. Do not copy deprecated backup fields from an old tutorial; match operator, plugin and PostgreSQL documentation to pinned releases.

**Timebox.** 4-6 hours within the recovery block; optional operator implementation after the core managed-database recovery exercise.

**Inspected:** [Primary source 1](https://github.com/cloudnative-pg/cloudnative-pg); [Primary source 2](https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/README.md); [Primary source 3](https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/docs/src/backup.md).

## 19. CISOfy/lynis

**Core lab — Week 4 baseline; weeks 21-24 automate selected fixes; week 41 reassess.** Audit Unix-like host configuration and identify hardening opportunities.

**Observed evidence.** README describes host auditing and hardening guidance. The official usage guide documents audit system, profiles, warnings and suggestions.

**Learning exercise.** Audit a disposable Linux VM, select three findings whose threat and operational effect you can explain, implement the chosen changes through Ansible, rerun the audit and application smoke tests, and document any intentionally accepted finding.

**Completion artifact.** Before/after findings, three explained fixes, an idempotent Ansible run and regression evidence.

**Operational caution and scope.** The hardening index is not a security guarantee or compliance certificate. Prioritize threat relevance and service functionality over a perfect score. A container or WSL result does not stand in for a complete cloud VM audit.

**Timebox.** 2 hours baseline plus 2 hours during Ansible, with later reassessment inside the security lesson.

**Inspected:** [Primary source 1](https://github.com/CISOfy/lynis); [Primary source 2](https://raw.githubusercontent.com/CISOfy/lynis/master/README.md); [Primary source 3](https://cisofy.com/documentation/lynis/).

## 20. jenkinsci/jenkins

**Reference — Week 12, after a working GitLab CI pipeline.** Extensible automation server widely used for build, test and deployment workflows.

**Observed evidence.** The primary README covers build/test/deploy automation and weekly versus LTS release lines. Jenkins security documentation says to isolate the controller and avoid executing builds on the built-in node.

**Learning exercise.** Map a small Jenkins pipeline's stages, agent, credentials and artifacts onto the equivalent GitLab jobs, runner and variables. Write a short migration note identifying plugin dependencies and the trust boundary between orchestration and executing untrusted code.

**Completion artifact.** A one-page Jenkins-to-GitLab concept map and a runner isolation checklist.

**Operational caution and scope.** Do not spend the main course administering a second CI platform. Installing plugins creates maintenance and security work; a tutorial's plugin list is not an architectural requirement.

**Timebox.** 60 minutes; no server installation required.

**Inspected:** [Primary source 1](https://raw.githubusercontent.com/jenkinsci/jenkins/master/README.md); [Primary source 2](https://www.jenkins.io/doc/book/security/).

## 21. woodpecker-ci/woodpecker

**Reference — Week 12, in the CI architecture comparison.** A lightweight, extensible CI/CD server and agent system.

**Observed evidence.** README identifies the server/agent architecture and plugin ecosystem. docker-compose.example.yaml mounts /var/run/docker.sock in the agent and contains example server registration and admin settings.

**Learning exercise.** Read the server/agent Compose example and draw which component receives source, runs code and can access credentials. Compare this to GitLab Runner. Explain what mounting the Docker socket grants and propose isolation for untrusted merge requests.

**Completion artifact.** A CI trust-boundary diagram and three isolation controls transferable to GitLab.

**Operational caution and scope.** The example is not a hardened deployment recipe. Docker socket access is a host-control trust decision; copying sample openness or administrator settings is inappropriate for shared runners.

**Timebox.** 45 minutes; no installation required.

**Inspected:** [Primary source 1](https://github.com/woodpecker-ci/woodpecker); [Primary source 2](https://raw.githubusercontent.com/woodpecker-ci/woodpecker/main/docker-compose.example.yaml).

## 22. go-task/task

**Core lab — Week 5 onward; reuse the same interface in GitLab CI in weeks 9-12.** Define repeatable developer and automation commands in a Taskfile.

**Observed evidence.** README identifies Task as a cross-platform build tool. Its guide covers dependencies, preconditions, output checks, platform shells, cleanup and remote Taskfile trust.

**Learning exercise.** Create named commands for format, lint, unit, integration, system smoke, build and local teardown. Keep actual logic in understandable scripts or test tools. Have GitLab call the same commands. Prove that a deliberately failing test returns failure to the pipeline and that cleanup stays within the lab.

**Completion artifact.** A documented Taskfile that works from a clean checkout and propagates failing exit codes.

**Operational caution and scope.** Task is an orchestration convenience, not a replacement for shell knowledge or GitLab CI. Untrusted Taskfiles execute commands. A cache or up-to-date shortcut must not silently bypass required validation.

**Timebox.** 2 hours initial setup, then maintained as part of normal lab work. An existing clear Makefile is an acceptable equivalent.

**Inspected:** [Primary source 1](https://github.com/go-task/task); [Primary source 2](https://taskfile.dev/docs/guide/).

## 23. theonedev/onedev

**Reference — Week 12 or week 45, as a platform comparison.** Integrated code hosting, review, issues, package registries and CI/CD.

**Observed evidence.** README describes conditional code-protection rules, CI executors, debugging, registries and issue/build linkage. The root license.txt inspected is MIT.

**Learning exercise.** Follow the documented lifecycle from issue to commit, protected review, successful test, package and deployment. Map each artifact to your GitLab workflow, and identify what must be backed up if the integrated platform is self-hosted.

**Completion artifact.** A traceability table for a single capstone release and a platform backup inventory.

**Operational caution and scope.** The first-year learning value is lifecycle traceability. Operating another full development platform would duplicate GitLab study and add unrelated administration. Root licensing does not establish entitlements for every external plugin or hosted feature.

**Timebox.** 45 minutes; no installation required.

**Inspected:** [Primary source 1](https://github.com/theonedev/onedev); [Primary source 2](https://github.com/theonedev/onedev/blob/main/license.txt).

## 24. apache/apisix

**Focused lab — Weeks 31-32 or 43, after HTTP, reverse proxies and Kubernetes Services.** An API gateway for routing, traffic policy, authentication and observability.

**Observed evidence.** README describes dynamic routing, canary traffic, authentication and observability. The Admin API reference instructs operators to configure a secure admin key and review the admin IP allowlist.

**Learning exercise.** Put two capstone versions behind a disposable gateway, route a small percentage of requests to the new version, enforce authentication and a rate limit, then test unauthorized, throttled, healthy and unavailable-upstream responses. Record latency before and after the gateway and rehearse rollback.

**Completion artifact.** Versioned route policy, automated HTTP assertions, a small latency comparison and rollback evidence.

**Operational caution and scope.** A gateway adds another component to operate. Keep the management API private. Do not copy a remote shell quickstart into a production host; inspect and pin artifacts. Choose one gateway implementation for the exercise.

**Timebox.** 2-4 hours, replacing a gateway extension rather than adding another required platform.

**Inspected:** [Primary source 1](https://github.com/apache/apisix); [Primary source 2](https://raw.githubusercontent.com/apache/apisix/master/README.md); [Primary source 3](https://apisix.apache.org/docs/apisix/admin-api/).

## 25. psviderski/uncloud

**Defer — Week 45 design reading; hands-on exploration after the core capstone or in year two.** Deploy containers across Docker hosts with a simpler operational interface.

**Observed evidence.** README shows multi-host container deployment and machine bootstrap. misc/design.md discusses mesh networking, shared state, coordination and imperative versus declarative orchestration as design choices.

**Learning exercise.** Read the design document and compare a single VM, managed container service, Uncloud and Kubernetes for a small service. Discuss networking, placement, state convergence, a host failure and the operational work each option transfers to the engineer.

**Completion artifact.** An architecture decision record explaining when Kubernetes is unnecessary and what requirements would change that decision.

**Operational caution and scope.** Treat the design document as design history and proposals, not proof that all described behavior is shipped. Verify current release behavior before relying on rescheduling or partition semantics. It does not replace learning Kubernetes for the stated career target.

**Timebox.** 60 minutes of reading; no required installation.

**Inspected:** [Primary source 1](https://github.com/psviderski/uncloud); [Primary source 2](https://github.com/psviderski/uncloud/blob/main/misc/design.md).

## 26. semaphoreui/semaphore

**Optional — Week 24, after Ansible CLI, inventories, roles and idempotence.** A UI and API for controlled execution of Ansible and other automation.

**Observed evidence.** README documents projects, templates, schedules, inventories and variable groups. The security policy states scope and a private vulnerability-reporting process; its fetched supported-version table may lag releases.

**Learning exercise.** Wrap the already-tested Ansible hardening playbook in a task template for a disposable inventory. Separate an operator's execution permissions from configuration changes, run the job twice, and compare the logs with the CLI workflow.

**Completion artifact.** A repeatable task template, restricted lab identity and a second run with no unintended changes.

**Operational caution and scope.** This is Semaphore UI, not the separate Semaphore CI product. Never reuse the README's example changeme password or unpinned latest image. A UI with execution credentials is a sensitive control surface; it does not replace playbook versioning or review.

**Timebox.** One optional 2-hour session; GitLab remains the primary CI/CD system.

**Inspected:** [Primary source 1](https://github.com/semaphoreui/semaphore); [Primary source 2](https://raw.githubusercontent.com/semaphoreui/semaphore/develop/SECURITY.md).

## 27. bunkerity/bunkerweb

**Optional — Week 41, after HTTP/TLS, application authorization and baseline security tests.** A web application firewall and reverse-proxy security layer.

**Observed evidence.** README describes ModSecurity with OWASP Core Rule Set, TLS and request controls; it explicitly recommends security tuning and false-positive management, and distinguishes AGPL community code from PRO features.

**Learning exercise.** Protect only your disposable capstone service. Create a small regression suite with legitimate requests and controlled malicious-looking inputs, observe false positives, make one narrow rule exception, and prove legitimate traffic works without disabling the entire rule set.

**Completion artifact.** A request/expected-result matrix, a justified narrow exception, relevant logs and a configuration rollback.

**Operational caution and scope.** A WAF does not repair broken authorization, vulnerable code or exposed credentials. Test only owned lab endpoints, retain application tests, and evaluate edition/licensing requirements before adoption. The linked security-tuning page could not be retrieved in this audit.

**Timebox.** One optional 2-hour session; do not add a second permanent ingress stack.

**Inspected:** [Primary source 1](https://github.com/bunkerity/bunkerweb).

## 28. OneUptime/oneuptime

**Reference — Weeks 33-36, after basic metrics, logs, traces and SLOs.** An integrated monitoring, incident response and observability platform.

**Observed evidence.** README lists monitoring, status pages, on-call, incidents, metrics/logs/traces and self-hosting. Its sizing document warns that Helm defaults are for trial installation and recommends 16 GB memory, 8 cores and 400 GB disk for the Compose deployment.

**Learning exercise.** Design a capstone incident flow: synthetic failure, actionable alert, acknowledgment, status update, recovery and postmortem. Read the sizing page and estimate how retention and telemetry rate affect storage. Implement the same flow in the lighter observability tools already used by the course.

**Completion artifact.** A timed incident exercise, draft status update, postmortem and telemetry-retention estimate.

**Operational caution and scope.** A full self-hosted deployment should not be mandatory on an unknown laptop or cloud budget. Demonstrated features and automated-fix marketing are not evidence of diagnosis accuracy. Check current sizing and paid/external notification costs before a later trial.

**Timebox.** 60 minutes of study within the SRE block; installation deferred unless capacity is confirmed.

**Inspected:** [Primary source 1](https://github.com/OneUptime/oneuptime); [Primary source 2](https://github.com/OneUptime/oneuptime/blob/master/packages/App/FeatureSet/Docs/Content/en/installation/sizing.md).

## 29. k8sgpt-ai/k8sgpt

**Optional — Week 32 or 44, after manual troubleshooting competence.** Kubernetes analyzers with optional language-model explanations.

**Observed evidence.** README documents analyzer scans, namespace/resource filters, JSON output, optional --explain providers and --anonymize.

**Learning exercise.** Create three known failures in a disposable namespace: bad image, incorrect Service selector and failed readiness probe. Write your diagnosis from events/logs first. Compare analyzer output and optional AI explanation, validate every claim against cluster evidence and record an incorrect or incomplete suggestion.

**Completion artifact.** A diagnosis comparison with ground truth, evidence, time taken and corrections.

**Operational caution and scope.** An AI explanation is a hypothesis. External providers may receive cluster-derived information; anonymization is not proof that all sensitive content is removed. Use synthetic lab data, narrow read permissions and no automatic remediation.

**Timebox.** One optional 2-hour session, after completing the same troubleshooting cases without it.

**Inspected:** [Primary source 1](https://github.com/k8sgpt-ai/k8sgpt).

## 30. freelensapp/freelens

**Optional — Week 28, only as an alternative to Headlamp.** A standalone Kubernetes management UI for Windows, macOS and Linux.

**Observed evidence.** README identifies its desktop platforms, kubeconfig use, bundled tools and OpenLens ancestry. Its directory listing exposes development/test configuration, but those tests were not inspected or run.

**Learning exercise.** If a desktop UI suits you better, use a limited lab kubeconfig to inspect workloads, events and logs. Diagnose a deliberate bad image, then reproduce the diagnosis with kubectl. Verify the current context before each operation.

**Completion artifact.** A UI-to-kubectl diagnosis and a written context/credential handling habit.

**Operational caution and scope.** Choose one dashboard, preserve CLI competence and protect kubeconfig credentials. Do not install unnecessary extensions or give broad permissions to simplify navigation. The linked security file was not retrievable in this audit, so no claim about its content is made.

**Timebox.** Use instead of Headlamp's 2-hour session; no additional course time.

**Inspected:** [Primary source 1](https://github.com/freelensapp/freelens).