# 52-week DevOps study plan

Edition 2026-10-20 · Beginner to operational practice · two hours/day · 728 scheduled hours.

Read [Start here](start-here.md) first. Weeks are relative learning units; repeat a gate when evidence is insufficient. Core readings are linked below. Read only the relevant sections in each week's Focus.

Each week: day 1 understand; days 2–3 build; day 4 verify; day 5 inject a controlled failure; day 6 reproduce; day 7 review and catch up. Optional repository exercises replace a related lab, never automatically add to the 14-hour budget.

## Week 1: Own your Linux environment

**Phase:** Foundations · **Execution:** Local

Find a process, its owner, listening socket, logs, configuration, and resource use without guessing.

**Concept:** A service is a process with dependencies, permissions, configuration, and a lifecycle. The shell is an observation tool before it is an automation tool.

**Focus:** Shell navigation and pipes; users and permissions; processes and signals; Git commits, branches and safe reverts.

**Read:** [Ubuntu command line tutorial](https://ubuntu.com/tutorials/command-line-for-beginners) · [Pro Git: basics, branching and tools](https://git-scm.com/book/en/v2)

### Build

1. Create a Linux lab and a Git repository with notes, app, tests and evidence directories. Record OS, available RAM and tool versions.
2. Run a local HTTP server bound to 127.0.0.1; identify its PID, owner and listening port using ps and ss.
3. Create a branch, introduce a harmless wrong configuration, commit it, then recover using git revert.

**Controlled failure:** Start a second server on the same port. Explain the address-in-use error using socket and process evidence; stop only your lab process.

### Prove before advancing

- Locate the correct process and port from a fresh terminal.
- Recover your intentional Git mistake while preserving history.
- Explain standard output, standard error, exit status and file ownership in your own words.

**Deliverable:** evidence/week-01.md with commands, observations, repository history and a 5-minute explanation.

**Mentor question:** What would distinguish a process that never started from one that started but cannot accept traffic?

## Week 2: Follow one request through the network

**Phase:** Foundations · **Execution:** Local

Separate DNS, transport, TLS, HTTP and application failures.

**Concept:** A successful name lookup does not prove a connection works; a connection does not prove the application is correct.

**Focus:** IP, ports, CIDR, routes, DNS records and TTL; TCP; TLS identity; HTTP methods and status codes.

**Read:** [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) · [Ubuntu command line tutorial](https://ubuntu.com/tutorials/command-line-for-beginners)

### Build

1. Draw browser → DNS → connection → TLS → reverse proxy → service → database, marking trust boundaries.
2. Use curl -v and a DNS lookup tool to observe an HTTPS request to a public documentation site.
3. Run the lab server on loopback, then compare connection refused, a wrong path and a deliberate application error.

**Controlled failure:** Use an incorrect hostname or local port in a client configuration without modifying your machine's global DNS. Diagnose the failing layer.

### Prove before advancing

- Predict the difference between timeout, connection refused, TLS verification error and HTTP 500.
- Explain why 0.0.0.0, localhost and a container service name are different.
- Explain /24 addressing and a default route using a small example.

**Deliverable:** An annotated request diagram and four short diagnosis records.

**Mentor question:** If curl works on the server but fails from your laptop, what would you inspect next and why?

## Week 3: Build a small service you understand

**Phase:** Foundations · **Execution:** Local

Create Taskboard, a deliberately small API that will grow with your operational skills.

**Concept:** Keep the application understandable so failures reveal infrastructure and delivery lessons rather than unfamiliar business logic.

**Focus:** HTTP contracts, input validation, configuration through environment variables, structured errors and unit testing.

**Read:** [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) · [pytest fixtures and isolation](https://docs.pytest.org/en/stable/how-to/fixtures.html)

### Build

1. Implement create/list/get/complete task endpoints, initially using in-memory storage. Reject blank titles and unknown task IDs.
2. Keep task validation in a pure function. Write tests for valid, blank, oversized and malformed inputs.
3. Add /livez and /version; log a request ID, method, status and duration without logging secrets.

**Controlled failure:** Change a boundary condition so a blank title is accepted. Confirm a test detects it before fixing it.

### Prove before advancing

- A fresh checkout runs with documented commands and a recorded dependency lock.
- At least one meaningful test fails on an intentional defect and passes after the fix.
- API errors are intentional and do not expose stack traces or secret configuration.

**Deliverable:** Taskboard v0.1 with README, API examples, tests and limitations.

**Mentor question:** Which tests can run without an HTTP server, and why should they?

## Week 4: Gate 1 · operate a Linux service

**Phase:** Foundations · **Execution:** Local VM; use a VM if WSL service behavior differs

Start, stop, diagnose and recover your service on a disposable Linux VM.

**Concept:** Process supervision is a reliability mechanism; repeated restarts are evidence of a problem, not a diagnosis.

**Focus:** Service users, environment files, systemd units, logs, graceful termination and operational documentation.

**Read:** [systemd service documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) · [Pro Git: basics, branching and tools](https://git-scm.com/book/en/v2)

### Build

1. Run Taskboard as an unprivileged service account in a disposable VM with a documented systemd unit.
2. Document start, status, journal, stop and restart commands, including where configuration is stored.
3. Write a small runbook and a clean-machine setup checklist.

**Controlled failure:** Give the lab service a wrong configuration path or an occupied port. Use logs to isolate the cause and recover.

### Prove before advancing

- Rebuild from your notes in 60–90 minutes without copying a working VM.
- Diagnose the injected fault and explain why the evidence supports your fix.
- Show the process does not need root and shuts down cleanly.

**Deliverable:** Gate 1 evidence, service unit and a reproducible Linux-service runbook.

**Mentor question:** What happens to in-memory task data after a restart, and what requirement would justify a database?

## Week 5: Package the service with Docker

**Phase:** Containers and testing · **Execution:** Local

Build and explain an image with a small, explicit runtime surface.

**Concept:** An image is a packaged filesystem and metadata. A container is an isolated process using that image, not a miniature independent kernel.

**Focus:** Dockerfile layers, build context, .dockerignore, non-root users, volumes, networking and signals.

**Read:** [Docker getting started](https://docs.docker.com/get-started/) · [Docker build best practices](https://docs.docker.com/build/building/best-practices/)

### Build

1. Containerize Taskboard, excluding Git history, virtual environments and secret files from the build context.
2. Choose and record a supported base image and its digest. Pin application dependencies and run as an unprivileged user.
3. Inspect image history and compare build cache behavior after a code-only change versus a dependency change.

**Controlled failure:** Bind the app to localhost inside the container and observe why host port publishing is insufficient. Correct the binding.

### Prove before advancing

- The image builds from a clean checkout and runs without source-code mounts.
- You can explain every Dockerfile instruction and where mutable data lives.
- No credential is copied into a layer; the process handles termination.

**Deliverable:** Dockerfile, .dockerignore, image digest and build/run notes.

**Mentor question:** Why can deleting a secret in a later image layer still leave it exposed?

## Week 6: Add PostgreSQL and real integration tests

**Phase:** Containers and testing · **Execution:** Local

Test the boundary between application code and an actual database.

**Concept:** Mocks cannot establish SQL, transaction or schema correctness. Integration tests exercise real boundaries in an isolated environment.

**Focus:** Compose services, database migrations, transactions, persistent volumes, isolated fixtures and readiness.

**Read:** [Docker Compose documentation](https://docs.docker.com/compose/) · [pytest fixtures and isolation](https://docs.pytest.org/en/stable/how-to/fixtures.html) · [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)

### Build

1. Add PostgreSQL-backed task storage with a migration and a persistent local volume.
2. Use Compose to start the app and database; avoid publishing the database port unless needed for a local debugging session.
3. Write integration tests that create a disposable test database or schema and clean up deterministically.

**Controlled failure:** Restart the app and database separately, then use a wrong database hostname. Distinguish persistence from connection configuration.

### Prove before advancing

- A created task survives an app restart.
- A real-database test detects a schema or transaction defect.
- Tests cannot accidentally use the development or future production database.

**Deliverable:** Compose configuration, migration and isolated integration test suite.

**Mentor question:** Why is a container being started different from a database being ready?

## Week 7: Prove whole-system behavior

**Phase:** Containers and testing · **Execution:** Local; never load-test other people's endpoints

Distinguish unit, integration, system, smoke and performance checks by purpose and scope.

**Concept:** The test level describes what boundary is exercised; test purpose describes what risk is checked.

**Focus:** Black-box HTTP tests, authentication versus authorization, task ownership, negative cases, isolation and timeouts.

**Read:** [pytest fixtures and isolation](https://docs.pytest.org/en/stable/how-to/fixtures.html) · [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)

### Build

1. Write a system test against the running Compose stack: create → read → complete → read after app restart.
2. Add a bounded lab-only bearer-token authentication dependency using maintained framework tooling and two synthetic identities. Keep tokens outside Git, enforce task ownership server-side and do not implement a password system. Keep this learning service local or behind a private tunnel.
3. Add missing/invalid-token, cross-user read/update, malformed-input, missing-record and database-unavailable tests with bounded timeouts. Return no other user's task data and verify that rejected updates do not alter it.

**Controlled failure:** Make the service return HTTP 200 with the wrong response body. Show why checking only the status code misses the defect.

### Prove before advancing

- Tests assert user-visible behavior, server-enforced ownership and data consistency.
- Failed tests return non-zero exit codes and useful diagnostics.
- The two synthetic users cannot read or update each other's tasks; the lab identity mechanism is explicitly unsuitable for an unreviewed public deployment.

**Deliverable:** Test matrix, authentication/authorization boundary sketch and denied-access evidence.

**Mentor question:** Can a test have high code coverage and still miss the failure users care about?

## Week 8: Gate 2 · reproducible local release

**Phase:** Containers and testing · **Execution:** Local

Release and recover a complete local service from a clean checkout.

**Concept:** A release is code plus configuration, schema compatibility, evidence and recovery instructions.

**Focus:** Versioning, reproducible commands, immutable artifacts, backups and release notes.

**Read:** [Docker build best practices](https://docs.docker.com/build/building/best-practices/) · [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)

### Build

1. Create explicit commands for unit, integration and system tests; optionally wrap them in Task after understanding the commands.
2. Tag a release and capture its image digest, dependency versions, migration version and test results.
3. Back up the lab database and restore it into a second isolated database.

**Controlled failure:** Ship a deliberately incorrect image tag, observe the failure, then restore the known-good artifact without rebuilding it.

### Prove before advancing

- A clean checkout starts the stack and all three test levels pass.
- Restored data passes a task-count and task-content check.
- Your release notes describe rollback limits when the database schema changes.

**Deliverable:** Taskboard v0.2 release dossier and restore evidence.

**Mentor question:** Why is rebuilding an old commit weaker recovery evidence than redeploying the exact previous image digest?

## Week 9: Build your first GitLab pipeline

**Phase:** GitLab delivery · **Execution:** GitLab quota/runner availability varies; record limits before use

Make GitLab execute the same checks you trust locally.

**Concept:** CI is an executable team agreement about what must be true before a change is accepted.

**Focus:** Runners, jobs, stages, merge requests, exit codes and JUnit reports.

**Read:** [GitLab CI/CD](https://docs.gitlab.com/ci/) · [GitLab CI YAML reference](https://docs.gitlab.com/ci/yaml/)

### Build

1. Create a GitLab project and a minimal .gitlab-ci.yml with lint and unit-test jobs.
2. Run checks on merge requests and use workflow/rules deliberately to avoid duplicate pipelines.
3. Publish test results with finite artifact retention and make a deliberately failing merge request.

**Controlled failure:** Make a test fail and confirm the pipeline blocks your documented release procedure.

### Prove before advancing

- The pipeline executes real commands, not placeholder echo messages.
- A failed command fails the job.
- You can explain where jobs run and what credentials they can see.

**Deliverable:** A passing and a failing pipeline linked from your evidence.

**Mentor question:** Who can modify pipeline code, and what authority does that effectively grant them?

## Week 10: Build once, test and promote

**Phase:** GitLab delivery · **Execution:** Prefer hosted isolated runners within available quota

Deliver the same artifact through test and staging.

**Concept:** Caches speed up work; artifacts are declared outputs. Neither is automatically trustworthy because it came from CI.

**Focus:** needs, artifacts, dependency caches, database services, image registries and digest-based promotion.

**Read:** [GitLab CI YAML reference](https://docs.gitlab.com/ci/yaml/) · [GitLab unit test reports](https://docs.gitlab.com/ci/testing/unit_test_reports/) · [Docker Compose documentation](https://docs.docker.com/compose/)

### Build

1. Add real PostgreSQL integration tests with a separate test database and readiness handling.
2. Build an image on a suitable isolated runner, push to the registry and record its digest.
3. Run a system test against that digest, then promote the same digest to a local or disposable staging environment.

**Controlled failure:** Restore a stale dependency cache or omit an artifact dependency. Identify whether the failure is reproducibility or job ordering.

### Prove before advancing

- Changing a cache does not change the required correctness outcome.
- The digest tested is the digest selected for deployment.
- Failures retain useful sanitized logs and test reports.

**Deliverable:** Pipeline graph, digest trace and test artifacts.

**Mentor question:** What can go wrong when the deploy job silently rebuilds instead of using the tested image?

## Week 11: Design pipeline trust

**Phase:** GitLab delivery · **Execution:** No cloud deployment required

Explain and limit the credentials and execution privileges a pipeline receives.

**Concept:** A pipeline runs code. Masking a variable does not prevent malicious job code from using it.

**Focus:** Protected refs, environment controls, scoped tokens, OIDC identity claims and untrusted merge requests.

**Read:** [GitLab pipeline security](https://docs.gitlab.com/ci/pipeline_security/) · [GitLab OIDC federation to AWS](https://docs.gitlab.com/ci/cloud_services/aws/) · [GitLab workload identity federation to GCP](https://docs.gitlab.com/ci/cloud_services/google_cloud/)

### Build

1. Draw contributor → runner → registry → deploy-role trust boundaries.
2. Separate untrusted test jobs from protected deployment jobs and review runner privileges.
3. Draft narrow OIDC trust conditions for a specific project and protected deployment ref. Implement cloud federation in weeks 20 and 39 after learning cloud IAM.

**Controlled failure:** Use a harmless sentinel variable to verify that an untrusted test path cannot access the deployment secret scope.

### Prove before advancing

- No long-lived cloud key is needed in the intended design.
- Your design denies the wrong project, audience and ref.
- You identify which GitLab controls are available in your tier and document a procedural fallback for paid controls.

**Deliverable:** Pipeline threat model and a negative-access test record.

**Mentor question:** What does the cloud verify about an OIDC token before giving the job a role?

## Week 12: Gate 3 · controlled release and rollback

**Phase:** GitLab delivery · **Execution:** Local staging or explicitly budgeted disposable VM

Release through GitLab with observable checks and an exercised recovery path.

**Concept:** Continuous delivery keeps a change releasable; continuous deployment also automates the production release decision.

**Focus:** Environments, manual deployment decisions, resource_group, smoke checks and rollback evidence.

**Read:** [GitLab CI/CD](https://docs.gitlab.com/ci/) · [GitLab CI YAML reference](https://docs.gitlab.com/ci/yaml/)

### Build

1. Add private staging and a protected release path with explicit environment ownership. Keep the core lab local or tunneled; before any public release, replace the teaching tokens with an established identity provider and maintained token-verification library, validating issuer, audience, expiry and task authorization. Treat that public-auth integration as an extension, not permission to expose the toy mechanism.
2. Serialize deployments to the same environment and reject outdated deployment jobs so an older queued pipeline cannot overwrite a newer approved release; keep pipeline artifacts immutable.
3. Add post-deploy smoke tests and write a rollback runbook that includes schema-compatibility checks.

**Controlled failure:** Deploy a version with a broken business endpoint but a healthy process. Let the smoke test detect it and roll back.

### Prove before advancing

- A failed pre-release check cannot advance through the documented release procedure.
- An older queued deployment cannot overwrite a newer approved release; test this separately from simultaneous-job serialization.
- You can identify and redeploy the last good digest within a measured lab recovery window.

**Deliverable:** Taskboard delivery v1, release recording and rollback report.

**Mentor question:** When is rolling forward safer than rolling back?

## Week 13: Learn cloud identity and spending boundaries

**Phase:** AWS foundations · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Understand accounts, regions, availability zones, identities, roles and billing before deploying.

**Concept:** Cloud APIs can create lasting resources and cost. Identity and ownership are part of the architecture.

**Focus:** Shared responsibility, MFA, role sessions, least privilege, tagging and budgets.

**Read:** [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) · [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) · [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

### Build

1. Read the account setup and IAM guidance. Use a dedicated learning account or isolated sandbox and protect privileged access.
2. Write a proposed monthly ceiling and per-lab inventory; configure budget notifications before paid experiments.
3. Use short-lived role-based access where available and identify your current account and region before each cloud command.

**Controlled failure:** Attempt a harmless read that your deliberately limited lab role should not allow. Explain the denial.

### Prove before advancing

- You can name the identity, account, region and allowed actions of your session.
- Budget notifications are configured and you understand they are not a hard spending cap.
- Your inventory contains owner, purpose, expiry and cleanup for every planned resource.

**Deliverable:** Cloud safety worksheet and IAM permission explanation with secrets removed.

**Mentor question:** What can still cost money after you stop a VM?

## Week 14: Networking and a small EC2 deployment

**Phase:** AWS foundations · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Trace traffic through a VPC, subnet, route table and security group.

**Concept:** Cloud networking combines address space, routing and policy. A subnet name does not make it private.

**Focus:** CIDR, public/private reachability, security groups, instance roles, DNS and access paths.

**Read:** [Amazon VPC user guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) · [Amazon EC2 user guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) · [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

### Build

1. Design a minimal single-region network and explicitly mark ingress and egress.
2. Run Taskboard on one disposable EC2 instance only if the current price fits your lab budget; otherwise rehearse on a VM and mark cloud execution pending. Keep application access private or tunneled while using the teaching authentication mechanism; public access requires an established identity/token-validation model and demonstrated authorization checks.
3. Restrict administration to your chosen controlled access path and keep the database off public ingress.

**Controlled failure:** Change only the lab service port rule, observe the symptom and use a layered diagnosis rather than opening all ports.

### Prove before advancing

- Explain every route and allowed inbound connection.
- The instance uses a scoped role rather than an embedded cloud key.
- Inventory and remove the instance and related billable resources after the lab.

**Deliverable:** Network diagram, sanitized deployment record and cleanup inventory.

**Mentor question:** Why can an instance have an address but still be unreachable?

## Week 15: Storage, databases and recovery

**Phase:** AWS foundations · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Choose among object storage, block storage and managed relational databases.

**Concept:** Durability, availability and recoverability answer different questions.

**Focus:** S3 access controls and versioning; RDS responsibilities; encryption; backups; connection limits.

**Read:** [Amazon S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html) · [Amazon RDS user guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) · [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)

### Build

1. Store a non-sensitive lab object in a private bucket and verify allowed and denied access.
2. Compare self-managed PostgreSQL with RDS: patching, backups, availability, cost and operational responsibility.
3. Rehearse database restore locally; execute a short RDS restore lab only if a fresh cost estimate permits it.

**Controlled failure:** Delete a disposable test record and restore into a separate database instead of overwriting the original.

### Prove before advancing

- Explain why a read replica is not a backup.
- Validate restored rows and application behavior.
- Record which AWS behaviors you executed and which you only designed.

**Deliverable:** Storage decision record and restore report with measured recovery time.

**Mentor question:** What failures survive replication and therefore require an independent recovery copy?

## Week 16: Gate 4 · review an AWS design

**Phase:** AWS foundations · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Defend a simple AWS architecture against reliability, security and cost requirements.

**Concept:** Architecture quality is about meeting requirements with understood tradeoffs, not maximizing the number of services.

**Focus:** Availability zones, load balancing, health checks, blast radius, operating cost and shared responsibility.

**Read:** [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) · [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)

### Build

1. Design a learning-sized deployment and a separate multi-AZ production proposal.
2. Document a single-instance failure, database failure and credential leak response.
3. Estimate both designs using current provider pricing, including load balancers, NAT, logs, storage, backups, IP addresses and egress.

**Controlled failure:** Tabletop an availability-zone failure: identify every dependency that remains a single point of failure.

### Prove before advancing

- Your diagram distinguishes implemented from proposed components.
- Every major design choice has a requirement and a cost consequence.
- Cloud resources are cleaned up and billing is checked again after reporting delay.

**Deliverable:** AWS design review, cost model and a list of unproven assumptions.

**Mentor question:** Would two web replicas help if both depend on one unavailable database?

## Week 17: Make infrastructure changes reviewable

**Phase:** Terraform · **Execution:** Local first; AWS resource only within explicit lab budget

Use Terraform's configuration, plan, state and apply workflow deliberately.

**Concept:** Terraform compares desired configuration, recorded state and provider observations. State is not just a disposable cache.

**Focus:** Providers, resources, data sources, dependencies, outputs, state and replacement.

**Read:** [Terraform tutorials](https://developer.hashicorp.com/terraform/tutorials) · [Terraform state](https://developer.hashicorp.com/terraform/language/state)

### Build

1. Start with a local-provider exercise, then describe one small AWS resource already understood from weeks 13–16.
2. Run formatting and validation; inspect a saved plan and explain creates, updates and replacements.
3. Commit configuration and the provider lock file; keep state, plans and secrets out of public Git.

**Controlled failure:** Change an attribute that forces replacement in a disposable resource. Predict the consequence before applying.

### Prove before advancing

- You can read a plan without treating it as a yes/no prompt.
- A second plan after convergence has no unexpected changes.
- You explain why state can contain sensitive values even when output is marked sensitive.

**Deliverable:** Small Terraform root module and annotated plan review.

**Mentor question:** What evidence would make you stop before applying a plan?

## Week 18: State, modules and environment boundaries

**Phase:** Terraform · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Separate environments and design small modules with stable interfaces.

**Concept:** A reusable module hides repetition, not operational responsibility.

**Focus:** Remote state, locking, versioning, variable validation, outputs and state ownership.

**Read:** [Terraform state](https://developer.hashicorp.com/terraform/language/state) · [Terraform modules](https://developer.hashicorp.com/terraform/language/modules) · [Terraform S3 backend and locking](https://developer.hashicorp.com/terraform/language/backend/s3)

### Build

1. Move the cloud lab to an access-controlled remote backend with encryption, versioning and supported locking.
2. Create one small network or service module with documented inputs and outputs.
3. Separate development and staging state and credentials; document the backend bootstrap and recovery procedure.

**Controlled failure:** Attempt a second operation while the first holds a lab state lock; observe protection without forcibly unlocking an active writer.

### Prove before advancing

- State access is restricted and recoverable.
- Module input validation rejects a bad value.
- You explain why workspaces alone do not create a security boundary.

**Deliverable:** Module README, state design and lock/recovery exercise.

**Mentor question:** Who can read state, and what authority or secrets could that reveal?

## Week 19: Test drift, assumptions and changes

**Phase:** Terraform · **Execution:** Mocked tests local; explicitly gated live tests may cost money

Catch invalid infrastructure designs and distinguish drift from intended change.

**Concept:** Syntax validity does not prove network reachability, access control or recoverability.

**Focus:** Plan assertions, mocked providers, apply tests, drift detection, import and moved resources.

**Read:** [Terraform test framework](https://developer.hashicorp.com/terraform/language/tests) · [Terraform tutorials](https://developer.hashicorp.com/terraform/tutorials)

### Build

1. Add tests for variable constraints and planned properties using terraform test.
2. Keep mocked/plan tests separate from apply tests that create real resources and incur cost.
3. Make one manual lab change, detect the drift and decide whether to restore configuration or adopt the change.

**Controlled failure:** Propose world-open administrative ingress in a lab configuration and make an assertion or policy fail before apply.

### Prove before advancing

- A deliberate unsafe change is rejected by an automated check.
- Live tests clean up and are verified against the provider inventory.
- You can explain a resource move without destroying it.

**Deliverable:** Terraform test suite, drift report and lifecycle notes.

**Mentor question:** Which assertions can a mocked provider never prove?

## Week 20: Gate 5 · deliver infrastructure through GitLab

**Phase:** Terraform · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Plan in a merge request and apply a reviewed change with scoped cloud identity.

**Concept:** Infrastructure delivery needs authorization, serialization and evidence tied to the exact change.

**Focus:** OIDC, narrow role trust, saved plans, protected execution and state isolation.

**Read:** [GitLab OIDC federation to AWS](https://docs.gitlab.com/ci/cloud_services/aws/) · [GitLab CI YAML reference](https://docs.gitlab.com/ci/yaml/) · [Terraform S3 backend and locking](https://developer.hashicorp.com/terraform/language/backend/s3)

### Build

1. Configure GitLab ID-token federation to AWS for your exact project and intended deployment ref.
2. Run format, validate and tests before a protected plan/apply workflow; limit plan artifact access and retention.
3. Recreate the small AWS environment from configuration and produce cleanup evidence.

**Controlled failure:** Try the role from the wrong ref or audience and verify denial; do not print the token.

### Prove before advancing

- The applied change is tied to the reviewed commit and plan.
- Untrusted merge requests cannot obtain deployment authority.
- Concurrent writers are serialized and cloud resources can be reconstructed.

**Deliverable:** Cloud-IaC pipeline with positive and negative identity tests.

**Mentor question:** What happens if configuration or state changes between planning and applying?

## Week 21: Configure machines consistently

**Phase:** Ansible and VM operations · **Execution:** Local VMs

Use Ansible inventories, modules and roles to configure your Linux service.

**Concept:** Terraform owns cloud resources; Ansible configures hosts. Define ownership so two systems do not fight over the same property.

**Focus:** SSH, inventory, facts, modules, privilege escalation, templates and handlers.

**Read:** [Ansible getting started](https://docs.ansible.com/projects/ansible/latest/getting_started/index.html) · [Ansible check and diff modes](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html)

### Build

1. Use two disposable Linux VMs or one VM plus an explicit second-host design.
2. Write a role to create a service user, install prerequisites, render configuration and manage Taskboard's service.
3. Use handlers so a service restarts when its configuration changes, not after every task.

**Controlled failure:** Introduce an incorrect inventory host or service configuration value and diagnose the failing task.

### Prove before advancing

- Host-specific values live in inventory variables rather than duplicated playbooks.
- A second normal run is unchanged unless a documented task intentionally varies.
- You can explain each privileged action.

**Deliverable:** Ansible role, example inventory and ownership decision record.

**Mentor question:** Why prefer a purpose-built package or service module over an unconditional shell command?

## Week 22: Idempotency, secrets and verification

**Phase:** Ansible and VM operations · **Execution:** Local

Demonstrate that configuration is repeatable and secret exposure is controlled.

**Concept:** Check mode predicts changes where supported; it does not substitute for executing and verifying a real configuration.

**Focus:** Check/diff modes, linting, encrypted data, key separation and post-configuration assertions.

**Read:** [Ansible check and diff modes](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html) · [Ansible getting started](https://docs.ansible.com/projects/ansible/latest/getting_started/index.html) · [SOPS primary repository](https://github.com/getsops/sops)

### Build

1. Lint the role and compare check/diff output with an actual run on a disposable host.
2. Keep secret decryption keys outside Git and log output; use encrypted configuration only where its delivery model is understood.
3. Assert that the expected port, user, file permissions and service endpoint are correct after configuration.

**Controlled failure:** Apply a wrong file owner or mode in the lab and ensure a post-configuration assertion catches it.

### Prove before advancing

- Two consecutive runs demonstrate intended idempotency.
- Secrets are absent from repository history, diffs and normal logs.
- Unsupported check-mode behavior is documented rather than mistaken for success.

**Deliverable:** Configuration verification report and secret-access diagram.

**Mentor question:** Who can decrypt this file, and how would you rotate that access?

## Week 23: Harden and patch with evidence

**Phase:** Ansible and VM operations · **Execution:** Local

Improve a host baseline without breaking legitimate service behavior.

**Concept:** A scanner finding is a lead for investigation. Hardening needs threat context, validation and recovery.

**Focus:** Patch management, service permissions, SSH access, firewall policy, audit evidence and exceptions.

**Read:** [Lynis primary repository](https://github.com/CISOfy/lynis) · [Ansible getting started](https://docs.ansible.com/projects/ansible/latest/getting_started/index.html) · [systemd service documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)

### Build

1. Audit the disposable VM with Lynis and classify findings by applicability and risk.
2. Implement three justified changes through Ansible, with before/after evidence.
3. Patch a dependency or package, then run service and system tests and rehearse recovery.

**Controlled failure:** Introduce a restrictive lab permission that blocks the service. Restore only the needed access.

### Prove before advancing

- Every accepted finding has a reason and a verification step.
- Hardening changes preserve required user behavior.
- You retain an access and rollback path during configuration changes.

**Deliverable:** Hardening change record, exception register and verified patch procedure.

**Mentor question:** When can a higher audit score make a real system less operable?

## Week 24: Gate 6 · rebuild the VM platform

**Phase:** Ansible and VM operations · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Provision, configure, deploy, restore and explain one complete environment.

**Concept:** Repeatability is demonstrated by a rebuild, not by how much infrastructure code exists.

**Focus:** Ownership boundaries, bootstrap, external dependencies and handoff.

**Read:** [Terraform tutorials](https://developer.hashicorp.com/terraform/tutorials) · [Ansible getting started](https://docs.ansible.com/projects/ansible/latest/getting_started/index.html) · [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)

### Build

1. Rebuild from Terraform plus Ansible and deploy a GitLab-tested artifact.
2. Restore test data and run the unit, integration and system test evidence appropriate to the release.
3. Have another person follow the runbook, or simulate a fresh-operator review using only the written instructions.

**Controlled failure:** Remove a disposable host and replace it; separately simulate a bad configuration rollout.

### Prove before advancing

- The replacement is created without undocumented console steps.
- Recovery time is measured and remaining manual steps are explicit.
- The system can be cleaned up without deleting unrelated resources.

**Deliverable:** First portfolio project: reproducible VM platform with recovery proof.

**Mentor question:** Which part of the environment cannot yet be reconstructed, and what would close that gap?

## Week 25: Learn reconciliation on a local cluster

**Phase:** Kubernetes · **Execution:** Local; a multi-node kind cluster is not multi-machine availability

Explain what the API server, scheduler, controllers, kubelet and container runtime do.

**Concept:** Kubernetes continuously reconciles declared objects with observed reality. A running Pod is an outcome of several cooperating components.

**Focus:** Cluster architecture, namespaces, manifests, Pods, Deployments and kubectl observation.

**Read:** [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/) · [Kubernetes concepts](https://kubernetes.io/docs/concepts/)

### Build

1. Create a local kind cluster and record compatible tool versions.
2. Deploy the known Taskboard image with a Deployment and inspect objects, events and logs.
3. Delete a disposable Pod and observe replacement through the owning Deployment and ReplicaSet.

**Controlled failure:** Use a nonexistent image tag and diagnose ImagePullBackOff from events.

### Prove before advancing

- You explain why editing a Pod manually is not a durable deployment change.
- You can identify an object's owner and desired replica count.
- Your manifests are versioned and reproducible.

**Deliverable:** Cluster architecture explanation and first Kubernetes manifests.

**Mentor question:** What does Kubernetes know about your application's business correctness?

## Week 26: Traffic, probes and safe rollout

**Phase:** Kubernetes · **Execution:** Local

Route requests to ready application instances and handle startup and shutdown correctly.

**Concept:** Readiness controls traffic eligibility; liveness can trigger restart; startup probes protect slow initialization.

**Focus:** Services, selectors, EndpointSlices, DNS, probes, rollout status and graceful termination.

**Read:** [Kubernetes startup, readiness and liveness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) · [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/) · [Kubernetes workload management](https://kubernetes.io/docs/concepts/workloads/management/)

### Build

1. Expose Taskboard internally through a Service and test service discovery.
2. Add appropriate startup/readiness/liveness checks; do not make liveness depend on a transient database outage.
3. Roll out a new digest while sending a small stream of local requests; record failures and termination behavior.

**Controlled failure:** Use a wrong Service selector, then a failing readiness check. Diagnose the two failures separately.

### Prove before advancing

- Unready instances stop receiving normal Service traffic.
- A slow start is not mistaken for a permanently dead process.
- You can explain and measure a rollout rather than only observing Running status.

**Deliverable:** Probe design, traffic-path diagram and rollout report.

**Mentor question:** How could a poorly designed liveness probe turn a database outage into a restart storm?

## Week 27: Configuration and workload security

**Phase:** Kubernetes · **Execution:** Local

Limit workload permissions and verify network isolation.

**Concept:** Namespaces organize objects; access control and network policy enforce specific boundaries.

**Focus:** ConfigMaps, Secrets, RBAC, service accounts, security contexts, Pod Security and NetworkPolicy.

**Read:** [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/) · [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/) · [SOPS primary repository](https://github.com/getsops/sops)

### Build

1. Run the app without privileged mode, with minimal capabilities and an explicit service account.
2. Add narrowly scoped RBAC and demonstrate an allowed and denied action.
3. Use a NetworkPolicy-capable CNI in the lab; allow app-to-database traffic and deny an unrelated test workload.

**Controlled failure:** Apply a policy missing the required DNS or database egress, then use evidence to add only the necessary rule.

### Prove before advancing

- Network policy enforcement is tested, not inferred from the existence of YAML.
- You explain that base64 encoding is not secret encryption.
- The app cannot perform an unnecessary Kubernetes API action.

**Deliverable:** Workload threat model, RBAC checks and network-policy tests.

**Mentor question:** What can a compromised app do with its mounted service-account token?

## Week 28: Gate 7 · diagnose Kubernetes failures

**Phase:** Kubernetes · **Execution:** Local

Use symptoms and evidence to distinguish scheduling, startup, traffic and application failures.

**Concept:** Events, logs, object state and actual requests answer different questions. Read them in a hypothesis-driven order.

**Focus:** Pending, CrashLoopBackOff, ImagePullBackOff, OOMKilled, selectors and dependency failures.

**Read:** [Kubernetes application troubleshooting](https://kubernetes.io/docs/tasks/debug/debug-application/) · [Kubernetes startup, readiness and liveness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

### Build

1. Create a troubleshooting decision tree with commands and expected observations.
2. Practise image, configuration, readiness, selector and resource-request failures one at a time.
3. Use Headlamp or Freelens only after diagnosing the same symptom with kubectl.

**Controlled failure:** Have a peer choose one fault without naming it, or randomize one of your previously prepared lab faults.

### Prove before advancing

- You preserve evidence before changing the deployment.
- The diagnosis explains the observed failure and the regression check.
- You can repeat the diagnosis without relying on a dashboard or AI explanation.

**Deliverable:** Five incident notes and one independently diagnosed fault.

**Mentor question:** Which observation would falsify your leading hypothesis?

## Week 29: Understand state and operators

**Phase:** Kubernetes operations · **Execution:** Local; operator exercise can be deferred if hardware is constrained

Explain Kubernetes storage and the operational cost of running a database in a cluster.

**Concept:** Scheduling a database is easier than operating its storage, replication, backups, upgrades and recovery.

**Focus:** PersistentVolumes, claims, StorageClasses, StatefulSets, operators and backup boundaries.

**Read:** [Kubernetes persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) · [CloudNativePG primary repository](https://github.com/cloudnative-pg/cloudnative-pg) · [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)

### Build

1. Run a small disposable PostgreSQL workload with a persistent claim and observe restart behavior.
2. Read CloudNativePG's current backup/plugin and recovery guidance and compare it with a managed database.
3. Prepare a restore lab with separate source and target data; install the operator only if local resources permit.

**Controlled failure:** Use an unavailable StorageClass or unsatisfied claim and diagnose why the workload remains pending.

### Prove before advancing

- You distinguish Pod persistence from volume durability and from backups.
- You can explain what the operator owns.
- Your design includes a recovery route when the original cluster is unavailable.

**Deliverable:** Database placement decision and storage failure record.

**Mentor question:** Would deleting and recreating a Pod help if the volume itself is corrupt?

## Week 30: Measure capacity before scaling

**Phase:** Kubernetes operations · **Execution:** Local

Set resource requests and limits from observed behavior and reason about autoscaling.

**Concept:** Adding replicas can move a bottleneck to the database or another dependency.

**Focus:** CPU requests, throttling, memory limits, OOM, metrics availability and HPA behavior.

**Read:** [Kubernetes resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) · [Kubernetes horizontal autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) · [Grafana k6 testing guides](https://grafana.com/docs/k6/latest/)

### Build

1. Measure CPU, memory, latency and error rate under a repeatable local workload.
2. Choose starting requests/limits with a written rationale.
3. Configure an HPA with its required metrics source; observe scale-out and scale-in while tracking database connections.

**Controlled failure:** Set an intentionally small memory limit in the disposable lab and distinguish an OOM termination from a probe failure.

### Prove before advancing

- The load report includes saturation and tail latency, not only average response time.
- You explain why the HPA did or did not react.
- Scaling limits respect downstream capacity and budget.

**Deliverable:** Capacity model with measured assumptions and autoscaling evidence.

**Mentor question:** How can more application replicas make database availability worse?

## Week 31: GitLab CI plus Argo CD

**Phase:** Kubernetes operations · **Execution:** Local

Separate building an artifact from reconciling a cluster to approved configuration.

**Concept:** GitOps uses versioned desired state and a controller to reconcile it; it does not eliminate authorization or recovery design.

**Focus:** Image digests, environment configuration, reconciliation, drift, sync and secret handling.

**Read:** [Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/) · [GitLab CI/CD](https://docs.gitlab.com/ci/) · [podinfo primary repository](https://github.com/stefanprodan/podinfo)

### Build

1. Let GitLab build/test/publish; let Argo CD reconcile a separate environment configuration path or repository.
2. Deploy podinfo first to isolate platform learning, then Taskboard.
3. Use SOPS only with an explicitly understood decryption integration; otherwise keep secrets external to plaintext Git.

**Controlled failure:** Make an intentional manual lab change and observe drift and the configured reconciliation policy.

### Prove before advancing

- The source commit, image digest and deployed revision can be traced.
- No two controllers compete to own the same field.
- A revert restores desired state subject to schema compatibility.

**Deliverable:** GitOps architecture and drift/recovery recording.

**Mentor question:** What prevents a malicious configuration change from being faithfully reconciled?

## Week 32: Gate 8 · release and recover on Kubernetes

**Phase:** Kubernetes operations · **Execution:** Local

Operate your service through a controlled update, failure and recovery.

**Concept:** Availability must be measured during change; a final green dashboard does not reveal an outage during rollout.

**Focus:** Rolling updates, disruption budgets, replica placement, rollout failure and rollback.

**Read:** [Kubernetes workload management](https://kubernetes.io/docs/concepts/workloads/management/) · [Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/) · [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)

### Build

1. Set rollout behavior based on measured startup and shutdown characteristics.
2. Run system tests and a small request stream while deploying a new version.
3. Document what a PodDisruptionBudget covers and what local kind cannot prove about real node or zone loss.

**Controlled failure:** Release an image that never becomes ready, then recover through the source of truth.

### Prove before advancing

- The rollout failure is detected and its impact measured.
- The last working image and configuration are recoverable.
- You explain database compatibility and remaining single points of failure.

**Deliverable:** Second portfolio project: Kubernetes delivery and recovery evidence.

**Mentor question:** What failure would your disruption budget not protect you from?

## Week 33: Measure the user experience

**Phase:** Observability and SRE · **Execution:** Local; choose one metrics stack

Instrument useful metrics and create a small actionable dashboard.

**Concept:** A metric should support a decision or diagnosis; collecting more data is not automatically better observability.

**Focus:** Request rate, errors, duration, saturation, labels, histograms and external probes.

**Read:** [Prometheus overview](https://prometheus.io/docs/introduction/overview/) · [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) · [Gatus primary repository](https://github.com/TwiN/gatus)

### Build

1. Expose request count, error count and duration histogram metrics.
2. Build a Prometheus/Grafana view of request rate, error ratio, latency and resource saturation.
3. Add Gatus or a simple external probe that exercises a meaningful service endpoint.

**Controlled failure:** Cause an endpoint failure while the process remains running and compare process health with user-visible availability.

### Prove before advancing

- Every dashboard panel answers a named question.
- Labels avoid unbounded user IDs, task IDs or raw URLs.
- The external check detects a failure the process check misses.

**Deliverable:** Dashboard definition and a metric design note.

**Mentor question:** Why can a low overall error rate hide a completely broken endpoint?

## Week 34: Connect logs and traces

**Phase:** Observability and SRE · **Execution:** Local; use a lighter backend if hardware is constrained

Follow a slow request across service and database boundaries.

**Concept:** Metrics describe aggregate behavior, logs capture events, and traces connect operations for a request.

**Focus:** Trace context, spans, structured logs, sampling, sensitive data and retention.

**Read:** [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) · [SigNoz primary repository](https://github.com/SigNoz/signoz) · [Sentry primary repository](https://github.com/getsentry/sentry)

### Build

1. Instrument Taskboard with OpenTelemetry and carry a request/trace identifier through logs.
2. Choose one local trace backend; inspect SigNoz as an option rather than adding multiple stacks.
3. Create a controlled slow database call and correlate latency metrics, logs and a trace.

**Controlled failure:** Drop trace context at one boundary and show how it breaks the diagnostic story.

### Prove before advancing

- You identify the slow operation from a trace and confirm it independently.
- Logs omit credentials and unnecessary personal data.
- Retention and sampling decisions have an explicit cost and privacy rationale.

**Deliverable:** One end-to-end trace investigation and telemetry policy.

**Mentor question:** What evidence is lost when a request is not sampled?

## Week 35: Define SLOs and useful alerts

**Phase:** Observability and SRE · **Execution:** Local

Turn service expectations into measurable targets and release decisions.

**Concept:** An SLO is a target for a defined indicator over a window. An error budget makes the tolerance for failure explicit.

**Focus:** SLIs, SLOs, error budgets, burn rate, low-traffic caveats and alert actions.

**Read:** [Google SRE: service level objectives](https://sre.google/sre-book/service-level-objectives/) · [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/)

### Build

1. Define eligible requests, good requests, measurement location and a rolling window.
2. Use a lab availability target such as 99.5% and a separate latency target; label both as chosen exercises.
3. Write an alert with a runbook and evaluate it using synthetic fault data or a controlled outage.

**Controlled failure:** Create a rapid burst of errors and compare detection with a slow sustained degradation.

### Prove before advancing

- You can calculate the remaining request-based error budget.
- An alert identifies a user-impacting symptom and a next action.
- You do not infer a 30-day SLO from a ten-minute successful test.

**Deliverable:** SLO document, budget calculation and alert evaluation.

**Mentor question:** When should reliability evidence delay a feature release?

## Week 36: Gate 9 · run an incident

**Phase:** Observability and SRE · **Execution:** Local

Detect, mitigate, communicate and learn from a service failure.

**Concept:** During an incident, restore useful service while preserving evidence; root-cause analysis can continue after mitigation.

**Focus:** Incident roles, timeline, hypotheses, mitigation, status communication and blameless follow-up.

**Read:** [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) · [awesome-sre primary repository](https://github.com/dastergon/awesome-sre)

### Build

1. Prepare a short incident protocol and a symptom-based runbook.
2. Run a timed game day with one controlled dependency or deployment failure.
3. Write an incident report with impact, timeline, contributing conditions, detection gaps and owned follow-up actions.

**Controlled failure:** Choose a fault the dashboards do not immediately identify; observe whether the runbook narrows it safely.

### Prove before advancing

- Detection and recovery times are measured from explicit events.
- Updates describe known impact and uncertainty without invented certainty.
- At least one prevention or detection improvement is implemented and retested.

**Deliverable:** Incident dossier and improved runbook.

**Mentor question:** What made this error possible or hard to detect beyond the individual who triggered it?

## Week 37: Translate identity, not just names

**Phase:** GCP · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Understand Google Cloud projects, IAM, service accounts and billing.

**Concept:** Similar service categories do not imply identical identity, networking or organizational behavior.

**Focus:** Organization/folder/project hierarchy, IAM bindings, service identities, quotas and budgets.

**Read:** [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/architecture/framework) · [Google Cloud IAM overview](https://cloud.google.com/iam/docs/overview) · [Google Cloud budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets)

### Build

1. Create a comparison of AWS accounts/roles and GCP projects/service accounts with the differences stated.
2. Design an isolated learning project and budget notifications before paid usage.
3. Use a limited identity and inspect permissions on a harmless resource.

**Controlled failure:** Test a deliberately denied read or write and locate the relevant permission boundary.

### Prove before advancing

- You can identify the active project and identity.
- You avoid exported long-lived service-account keys in the planned delivery workflow.
- You explain why budget alerts do not cap spending.

**Deliverable:** GCP identity map and AWS/GCP comparison table.

**Mentor question:** What can go wrong if a command uses the correct account but the wrong project?

## Week 38: Networking, compute and storage on GCP

**Phase:** GCP · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Deploy a small familiar workload while examining cloud differences.

**Concept:** Portability belongs at chosen interfaces; cloud-specific capabilities still require explicit design.

**Focus:** VPC scope, regional subnets, firewall policy, instance identity, storage permissions and logs.

**Read:** [Google Cloud VPC overview](https://cloud.google.com/vpc/docs/overview) · [Compute Engine documentation](https://cloud.google.com/compute/docs) · [Cloud Storage access control](https://cloud.google.com/storage/docs/access-control)

### Build

1. Draw a GCP traffic path and compare its resource scope with AWS.
2. Deploy the same Taskboard image on a short-lived Compute Engine VM if budget permits. Preserve private/tunneled access unless the established public authentication and authorization model has been implemented and verified.
3. Test private object access with a scoped identity and document cleanup.

**Controlled failure:** Use an incorrect service identity or firewall rule in the lab and diagnose without granting broad access.

### Prove before advancing

- The app image remains unchanged while cloud configuration differs.
- Allowed and denied access are both demonstrated.
- The inventory includes persistent disks, addresses and storage after VM removal.

**Deliverable:** GCP deployment record and portability decision.

**Mentor question:** Which parts of the AWS network design cannot be copied mechanically?

## Week 39: Terraform and GitLab federation on GCP

**Phase:** GCP · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Deliver a small GCP workload with short-lived pipeline identity.

**Concept:** Workload identity federation connects an external identity to narrowly authorized cloud actions.

**Focus:** Workload identity pools/providers, attribute conditions, impersonation, remote state and serverless constraints.

**Read:** [GitLab workload identity federation to GCP](https://docs.gitlab.com/ci/cloud_services/google_cloud/) · [Terraform tutorials](https://developer.hashicorp.com/terraform/tutorials) · [Cloud Run documentation](https://cloud.google.com/run/docs)

### Build

1. Create Terraform configuration for the chosen small GCP deployment and isolate its state from AWS.
2. Configure GitLab federation scoped to the intended project/ref and deploy without a downloaded service-account key.
3. Evaluate Cloud Run using podinfo or a stateless Taskboard variant; require authenticated invocation for the lab and document external state, concurrency and scaling constraints. Do not publicly expose Taskboard's teaching authentication mechanism.

**Controlled failure:** Change an audience or attribute condition in the lab and verify that incorrect identity is rejected.

### Prove before advancing

- The deploy job obtains short-lived authority only for the intended scope.
- No persistent application data relies on a container's ephemeral filesystem.
- The exact deployed image digest is traceable to test results.

**Deliverable:** GCP delivery pipeline and federation verification.

**Mentor question:** Why is identity federation still dangerous if the authorized role is too broad?

## Week 40: Gate 10 · compare managed platforms

**Phase:** GCP · **Execution:** Free local core practice; optional provider execution may incur charges and has separate evidence.

Choose between VMs, managed containers and managed Kubernetes for stated needs.

**Concept:** Operational simplicity is an architectural advantage when it meets the requirements.

**Focus:** Managed control planes, workload identity, upgrades, networking, availability and total operating cost.

**Read:** [Google Kubernetes Engine overview](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview) · [Amazon EKS user guide](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html) · [Cloud Run documentation](https://cloud.google.com/run/docs) · [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/architecture/framework)

### Build

1. Compare EC2/Compute Engine, a managed container service, EKS and GKE against Taskboard's requirements.
2. Choose one managed Kubernetes lab, EKS or GKE, for a short execution if budget permits; keep the other a documented comparison.
3. Deploy the known manifests, test identity and traffic, then remove the cluster and dependent resources.

**Controlled failure:** Tabletop loss of a node and an unavailable control plane; separate provider and customer responsibilities.

### Prove before advancing

- You can justify choosing a simpler platform when Kubernetes adds unnecessary work.
- The comparison includes ongoing operations and cost, not only initial deployment.
- Executed and design-only capabilities are clearly labeled.

**Deliverable:** Cloud platform decision and optional managed-cluster evidence.

**Mentor question:** Which responsibilities remain yours even with a managed control plane?

## Week 41: Secure the software supply chain

**Phase:** Security and resilience · **Execution:** Local/CI; verify chosen tool and hosted service terms

Trace source, dependencies, build identity and artifact integrity.

**Concept:** A vulnerability scan is one signal; provenance and authorization answer different trust questions.

**Focus:** SBOMs, image scanning, signatures, provenance, dependency updates and exception expiry.

**Read:** [SLSA supply-chain framework](https://slsa.dev/) · [Sigstore documentation](https://docs.sigstore.dev/) · [GitLab pipeline security](https://docs.gitlab.com/ci/pipeline_security/)

### Build

1. Generate an SBOM and scan the application image using one selected tool.
2. Triage findings by exposure, exploitability, fix availability and operational context; assign time-limited exceptions.
3. Sign or attest the artifact and verify the expected identity and digest before a lab deployment.

**Controlled failure:** Try to deploy an unexpected digest or untrusted signing identity and make the release check reject it.

### Prove before advancing

- The signature is verified against an identity policy, not merely present.
- A critical finding has a documented fix or explicit scoped exception.
- You can trace a running digest back to source and build evidence.

**Deliverable:** Supply-chain evidence bundle and update procedure.

**Mentor question:** What does a valid signature prove, and what does it leave unproven?

## Week 42: Migrate and recover data safely

**Phase:** Security and resilience · **Execution:** Local; backups and retention in cloud are billable

Change schemas compatibly and prove restoration of meaningful data.

**Concept:** Deployment rollback and data rollback are different operations with different risks.

**Focus:** Expand/contract migrations, old/new app compatibility, backup retention, WAL and point-in-time recovery.

**Read:** [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html) · [CloudNativePG primary repository](https://github.com/cloudnative-pg/cloudnative-pg) · [Databasus primary repository](https://github.com/databasus/databasus)

### Build

1. Add an optional field using an expand/contract sequence; test old and new application versions against the expanded schema.
2. Schedule a local backup and restore to a separate destination using PostgreSQL tooling or one audited backup tool.
3. If practising PITR, verify the exact selected tool/version supports the required backup and WAL recovery path.

**Controlled failure:** Delete a disposable record at a known time and recover the intended data without overwriting the source environment.

### Prove before advancing

- A migration test catches incompatible schema changes.
- The restored app passes system tests and content checks.
- Measured data loss and recovery time are compared with your chosen RPO/RTO.

**Deliverable:** Migration compatibility matrix and restore drill report.

**Mentor question:** How would you know a successful-looking backup is actually usable?

## Week 43: Scale with bottlenecks in mind

**Phase:** Security and resilience · **Execution:** Local controlled load

Improve measured performance while controlling overload and consistency.

**Concept:** Queues absorb bursts only while capacity and retention are sufficient; retries can multiply load.

**Focus:** Indexes, connection pools, bounded queues, backpressure, timeouts, retries with jitter and idempotency.

**Read:** [Grafana k6 testing guides](https://grafana.com/docs/k6/latest/) · [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) · [Kubernetes horizontal autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

### Build

1. Use profiling or query evidence to identify one bottleneck and improve it.
2. Add an optional background task with an idempotency key only if it solves a stated requirement.
3. Set bounded timeouts and retry behavior; compare baseline and changed throughput, p95/p99, errors and resource cost.

**Controlled failure:** Slow a dependency or deliver the same background message twice. Observe retry amplification or duplicate work and fix it.

### Prove before advancing

- The improvement is supported by comparable before/after conditions.
- If a background task was added, duplicate delivery cannot silently double-apply the chosen operation; otherwise document this extension as not implemented.
- The service degrades predictably when downstream capacity is exhausted.

**Deliverable:** Performance investigation and overload behavior report.

**Mentor question:** When is rejecting work quickly safer than accepting it into an ever-growing queue?

## Week 44: Gate 11 · recovery game day

**Phase:** Security and resilience · **Execution:** Local default; any cloud reconstruction has a fresh cost estimate

Recover both service and data under explicit constraints.

**Concept:** High availability reduces some interruptions; disaster recovery prepares for loss of the normal operating environment.

**Focus:** RTO, RPO, dependencies, credential recovery, backup access and communication.

**Read:** [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) · [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) · [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/architecture/framework)

### Build

1. Set achievable lab targets, for example RTO 30 minutes and RPO 24 hours for daily logical backups.
2. Simulate losing a disposable environment; rebuild it and restore into a fresh target.
3. Audit whether backups, decryption keys, configuration and runbooks survive the same failure boundary.

**Controlled failure:** Make the normal cluster unavailable while preserving a separate lab backup; restore without depending on the old cluster.

### Prove before advancing

- Measured recovery and data loss meet your stated lab targets or produce a remediation plan.
- Restoration passes meaningful system checks.
- A failed drill is reported accurately rather than marked complete.

**Deliverable:** Disaster-recovery report and revised dependencies map.

**Mentor question:** Which shared dependency could make both your primary system and recovery plan fail?

## Week 45: Kubernetes internals, deliberately

**Phase:** Internals and platform practice · **Execution:** Local VMs; selected reading-only path if hardware cannot support the lab

Understand certificate trust, component communication and control-plane state.

**Concept:** A managed cluster hides implementation work, not the need to understand its failure modes.

**Focus:** PKI, kubeconfigs, API authorization, etcd, control-plane components and node registration.

**Read:** [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) · [Kubernetes concepts](https://kubernetes.io/docs/concepts/)

### Build

1. Read the current Kubernetes The Hard Way prerequisites and choose compatible disposable VMs.
2. Trace component-to-component trust and produce a certificate/identity map.
3. Complete the first bounded set of current upstream steps; annotate what every credential and configuration file permits.

**Controlled failure:** Inspect a deliberately wrong lab endpoint or expired test certificate without changing real cluster credentials.

### Prove before advancing

- You can explain why each component needs its identity.
- You understand the difference between authentication and authorization.
- You record upstream commit/version and mark unfinished steps explicitly.

**Deliverable:** Kubernetes trust map and first internals lab notes.

**Mentor question:** Why is copying an administrator kubeconfig to every machine a poor design?

## Week 46: Upgrades and component failures

**Phase:** Internals and platform practice · **Execution:** Local

Plan a cluster upgrade and diagnose a bounded component failure.

**Concept:** The cluster is itself a system to operate, including version compatibility, certificates, storage and recovery.

**Focus:** Version skew, backup scope, certificate lifecycle, draining and upgrade validation.

**Read:** [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) · [Kubernetes version skew policy](https://kubernetes.io/releases/version-skew-policy/) · [Kubernetes application troubleshooting](https://kubernetes.io/docs/tasks/debug/debug-application/)

### Build

1. Complete the chosen Hard Way scope or document a component-focused alternative.
2. Read current version-skew guidance and plan an upgrade of a disposable cluster.
3. Exercise prechecks, a bounded update, postchecks and an explicit recovery decision; distinguish workload backup from etcd backup.

**Controlled failure:** Stop a lab worker service or misconfigure a component endpoint and trace symptoms back to the component.

### Prove before advancing

- The upgrade plan respects currently supported version skew.
- You identify which failures stop new scheduling versus existing traffic.
- You can explain what restoring etcd does and does not restore.

**Deliverable:** Upgrade runbook and component failure investigation.

**Mentor question:** Which application data is absent from an etcd snapshot?

## Week 47: Make a paved path for another developer

**Phase:** Internals and platform practice · **Execution:** Local

Turn your working conventions into a small usable service template.

**Concept:** Platform engineering reduces repeated cognitive work while retaining clear escape hatches and ownership.

**Focus:** Service templates, documentation, defaults, developer feedback and support boundaries.

**Read:** [GitLab CI/CD](https://docs.gitlab.com/ci/) · [Task primary repository](https://github.com/go-task/task) · [Ansible getting started](https://docs.ansible.com/projects/ansible/latest/getting_started/index.html)

### Build

1. Create a template with health endpoints, tests, CI, configuration conventions and a runbook.
2. Provide understandable commands for development, testing and deployment.
3. Evaluate Semaphore or another audited platform only against a specific usability problem; keep the default workflow small.

**Controlled failure:** Give the template an invalid configuration and improve the resulting error message and documentation.

### Prove before advancing

- A new user can start the example with documented prerequisites.
- Defaults limit privilege and secret exposure.
- The template describes what its maintainers own and what application owners own.

**Deliverable:** Service template v1 and developer onboarding notes.

**Mentor question:** Does this abstraction remove work or merely hide failure modes?

## Week 48: Gate 12 · independent engineering review

**Phase:** Internals and platform practice · **Execution:** Local

Demonstrate transferable judgment beyond a rehearsed tutorial.

**Concept:** Competence includes explaining when not to use a tool and recovering when the tutorial's assumptions fail.

**Focus:** Design critique, practical diagnosis, communication and identifying gaps.

**Read:** [DevOps exercises](https://github.com/bregman-arie/devops-exercises) · [roadmap.sh DevOps](https://roadmap.sh/devops) · [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

### Build

1. Answer a selected set of unseen Linux, cloud, Kubernetes, Terraform and SRE questions without notes, then verify against current docs.
2. Perform two previously unseen local fault investigations.
3. Review a proposed overcomplicated architecture and simplify it with explicit tradeoffs.

**Controlled failure:** Use an unfamiliar combination of two known faults, preserving an escape route.

### Prove before advancing

- Each incorrect explanation becomes a concrete remedial exercise.
- You separate measured facts from hypotheses.
- You can explain the system to both a developer and a non-technical stakeholder.

**Deliverable:** Competency scorecard and capstone gap list.

**Mentor question:** Which skills are demonstrated independently, and which still depend on a guide?

## Week 49: Specify a service worth operating

**Phase:** Final capstone · **Execution:** Planning; paid execution only after estimating the chosen design

Translate a small product need into testable operational requirements.

**Concept:** Production readiness is relative to users, risk, workload and operating constraints.

**Focus:** Requirements, threat model, capacity assumptions, SLO, cost ceiling and ownership.

**Read:** [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) · [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/architecture/framework) · [Google SRE: service level objectives](https://sre.google/sre-book/service-level-objectives/)

### Build

1. Write a Taskboard service brief with users, data sensitivity, expected traffic and failure consequences.
2. Choose one primary deployment platform; retain the second cloud as a tested portability exercise rather than mandatory active-active complexity.
3. Define acceptance tests, recovery targets, monitoring, update policy and architecture decisions before building.

**Controlled failure:** Challenge one assumption: tenfold traffic, loss of a zone, leaked credential or incompatible schema change.

### Prove before advancing

- Every major control traces to a requirement or threat.
- Targets include measurement method and test conditions.
- The design fits a stated operating budget.

**Deliverable:** Capstone service brief, threat model and acceptance contract.

**Mentor question:** What would make this architecture insufficient for a real customer?

## Week 50: Build and deliver the complete system

**Phase:** Final capstone · **Execution:** Local valid; cloud claims require real cloud evidence

Integrate application, infrastructure, delivery, security and observability into a reproducible release.

**Concept:** The final project should demonstrate a coherent operating system of practices, not a collection of tool screenshots.

**Focus:** Infrastructure/configuration ownership, tested artifacts, identity, restore and documentation.

**Read:** [GitLab CI/CD](https://docs.gitlab.com/ci/) · [Terraform tutorials](https://developer.hashicorp.com/terraform/tutorials) · [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)

### Build

1. Rebuild the chosen platform from code and deploy the exact tested image.
2. Run unit, real integration and system tests plus infrastructure and security checks.
3. Attach telemetry, release evidence, backup verification and current cost inventory.

**Controlled failure:** Attempt a release with one deliberately failed acceptance condition and verify the release decision rejects it.

### Prove before advancing

- No critical operational step exists only in your memory.
- Source, artifact, configuration and deployment revisions are traceable.
- The release can be reproduced from a clean environment.

**Deliverable:** Capstone release candidate and evidence index.

**Mentor question:** Which part of the delivery path has the broadest authority, and how is it constrained?

## Week 51: Break it under review

**Phase:** Final capstone · **Execution:** Local default; controlled budgeted cloud session if selected

Demonstrate recovery, diagnosis and communication under realistic lab pressure.

**Concept:** Failure drills test the system and its operating procedures together.

**Focus:** Blind incidents, restore validation, load behavior, rollback and follow-up work.

**Read:** [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) · [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html) · [Grafana k6 testing guides](https://grafana.com/docs/k6/latest/)

### Build

1. Run one deployment failure, one dependency/network failure and one data-recovery scenario.
2. Perform a controlled load test at the declared workload and compare against latency/error targets.
3. Produce one incident report with a prioritized remediation backlog and retest the highest-risk improvement.

**Controlled failure:** Let a reviewer select the fault, or use a randomized prepared scenario and avoid inspecting the fault source before diagnosis.

### Prove before advancing

- Recovery and performance claims have timestamped evidence and stated limits.
- No lost or duplicate user operation is hidden by a green infrastructure dashboard.
- The operator can communicate impact while continuing diagnosis.

**Deliverable:** Final game-day and performance dossier.

**Mentor question:** What failed in your process even if the service was eventually restored?

## Week 52: Gate 13 · hand it to another engineer

**Phase:** Final capstone · **Execution:** No additional infrastructure required

Present a defensible portfolio and a clear map of your next learning needs.

**Concept:** Strong engineering makes systems understandable and maintainable by people other than their original author.

**Focus:** Handoff, architecture explanation, operational readiness, honest claims and continued practice.

**Read:** [roadmap.sh DevOps](https://roadmap.sh/devops) · [DevOps exercises](https://github.com/bregman-arie/devops-exercises)

### Build

1. Have another person rebuild, deploy and recover from your documentation; if unavailable, do a fresh-environment self-review and label it accordingly.
2. Score the capstone using the readiness rubric, resolving critical failures.
3. Write a concise portfolio narrative: problem, constraints, choices, evidence, incidents, tradeoffs and remaining limitations.

**Controlled failure:** Remove your informal assistance from the handoff and identify every point where the documentation is insufficient.

### Prove before advancing

- All mandatory gates have evidence or are explicitly incomplete.
- The portfolio does not claim seniority or production reliability from lab duration alone.
- You have a specific next-quarter plan based on demonstrated weaknesses.

**Deliverable:** Portfolio, handoff package, final scorecard and next-quarter improvement plan.

**Mentor question:** Would a teammate trust you to explain the risk of a change and help recover when it fails?
