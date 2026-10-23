# Proving that you can operate a service

This handbook turns study into evidence a teammate can review. Your goal is to build a service, explain its behavior, detect a failure, recover safely and leave another engineer able to operate it. A successful deployment proves only that one attempt worked. Competence becomes visible when the same process works from a clean checkout and when you can explain what happens outside the happy path.

Use this alongside the weekly plan. Plan around two hours a day. Weeks 1–4 teach the programming, Linux and Git foundations used here; beginners should complete those lessons before attempting these operational assessments. The exercises and scoring below are curriculum choices, not an industry certification. A strong result demonstrates readiness for supervised production work; it does not replace experience with real users, organizational constraints or unfamiliar incidents.

## A two-hour practice session

Spend the first 10 minutes stating a measurable objective and recalling yesterday's concepts without notes. Use 20 minutes for the relevant official documentation, 65 minutes to implement or investigate, 15 minutes to check a failure path, and 10 minutes to record evidence and clean up.

When stuck, write three things: observed behavior, expected behavior and your next discriminating check. A discriminating check separates plausible causes: reaching a Pod directly but not through its Service makes application code less likely and routing more likely. Change one thing at a time. After 25 minutes without new evidence, narrow the experiment or consult a focused reference. Random configuration changes produce accidental fixes that you cannot maintain.

Use AI to explain evidence or challenge a hypothesis after making your own attempt. Keep an independent record of what you thought before asking. Never treat a plausible explanation as a confirmed cause.

## Evidence that survives the session

Each meaningful lab produces one short record using `templates/evidence.md`: objective, exact source version, environment, commands or automation entry point, observed results, a negative case, interpretation and cleanup. Include the commit and image digest where relevant. Link test reports and small sanitized log excerpts instead of dumping secrets or entire logs.

Separate three statements: “the documentation says,” “I observed,” and “I infer.” For example, “I observed a replacement Pod” does not establish availability-zone resilience. A recovery measurement needs start/end timestamps and a defined finish condition. A screenshot can help explain a result, but executable assertions and raw measurements make stronger evidence.

Keep small reports in version control. Store large artifacts with a documented retention period. Record failures honestly; a clear investigation of an unresolved problem is more useful than a green badge obtained by weakening the test.

## Testing the service at three boundaries

**Unit tests** exercise a small piece of application behavior without a real database or network: validation, calculation, retry classification and error conversion. Include boundaries and invalid inputs. They should be quick enough to run whenever code changes.

**Integration tests** exercise actual interfaces between components. Start a disposable database, apply migrations, call the repository/API layer and verify real persistence, uniqueness, transaction handling and unavailable-dependency behavior. A mocked database client is useful for a unit test, but cannot demonstrate SQL compatibility.

**System tests** exercise the deployed service through its public boundary. Create a record, retrieve it, attempt unauthorized access, and verify persistence after a controlled restart. Run them against a disposable environment built from the candidate artifact. Keep the suite small and representative; many slow UI tests do not compensate for missing lower-level checks.

Security, load and resilience checks ask additional questions across these boundaries. Make a deliberate defect fail the correct test and block promotion. Build the release artifact once, record its identity, and promote that artifact. Keep a release note linking source, pipeline, tests, configuration and deployment.

## Targets with explicit limits

An SLI is a measured aspect of user service; an SLO is its target over a stated window. Define eligible requests and successful outcomes before measurement. For this lab, a successful read means the correct response within the timeout, not merely any HTTP response. Report unexpected errors separately from intentional authentication or rate-limit rejections. Percentiles help expose slow requests hidden by an average. [Google SRE: service level objectives](https://sre.google/sre-book/service-level-objectives/)

Use these **sample lab targets**, then adjust them before a run if your hardware requires it:

| Question | Initial target and measurement |
|---|---|
| Can another person start it? | Clean local checkout to passing smoke test within 30 minutes using the documented prerequisites. |
| Does it behave under modest load? | After 2 minutes of warm-up, sustain 20 requests/second for 10 minutes on the recorded machine; at least 99% of eligible requests succeed and p95 latency is below 300 ms. Record actual throughput and dropped load-generator work. |
| Can an alert detect an outage? | A deliberately stopped lab API produces a visible actionable alert within 2 minutes, measured from injection to notification receipt. |
| Can you reverse a bad release? | Restore the previous compatible application artifact and pass the smoke test within 10 minutes. Database compatibility must be checked separately. |
| Can you recover data? | Restore a 100 MB synthetic dataset into a new environment within 30 minutes, with no more than 5 minutes of committed writes missing when using a backup/WAL strategy designed for that target. |

These are engineering exercises, not production promises or statistically proven annual availability. A ten-minute run says little about a year's rare failures. Always record hardware, data volume, dependency placement, test duration and exclusions. Stop a load run when resource limits or the defined error threshold are crossed.

**RTO**, recovery time objective, is the maximum acceptable recovery duration for the scenario. **RPO**, recovery point objective, expresses the acceptable data-loss window. Define the outage start and recovered-service checks; measure lost writes using timestamped records. Replication can improve availability but can also replicate an unwanted deletion. A backup is useful only when you can restore and validate it. [AWS Well-Architected: recovery objectives](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_objective_defined_recovery.html)

If you only have a daily logical dump, do not claim a five-minute RPO. State the achievable limit and the next improvement. For CloudNativePG, use release-matched backup/plugin guidance and preserve required credentials separately; a restored database without access material may still leave the service unavailable. [CloudNativePG backup documentation](https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/backup.md)

## Twelve controlled failure drills

Run these only in your disposable local VM, Compose project or explicitly selected `lab-drills` Kubernetes namespace, with synthetic data. Save the last working configuration, scope the change and write the reversal before injecting it. Do not fill the host disk, attack public services, alter real credentials, disable account security or load-test a paid endpoint. One drill should usually fit one session.

For every drill, capture the symptom, initial hypothesis, evidence that supports or rejects it, smallest safe fix and regression check.

| Drill and injection | Symptom and hypothesis | Evidence to collect | Fix and regression |
|---|---|---|---|
| 1. Wrong image reference: set a nonexistent tag in a lab Deployment. | New release never becomes ready; suspect registry/image selection. | Pod events, exact image reference and deployment conditions. | Restore the pinned known image; verify all intended replicas ready and the API returns the expected version. |
| 2. Wrong Service selector: change one label in the lab manifest. | Service requests fail while the Pod runs; suspect no matching backends. | Compare labels, EndpointSlices and a direct Pod request. | Correct the selector in source; add a system request through the Service boundary. |
| 3. Bad readiness path: point readiness to a missing endpoint. | Healthy-looking process receives no Service traffic; suspect health configuration. | Probe events, endpoint membership and direct health response. | Correct readiness; demonstrate temporary unready state removes traffic and recovery restores it. |
| 4. Startup too slow: introduce a bounded startup delay. | Repeated restarts before startup completes; suspect liveness timing. | Restart count, timestamps and previous-container logs. | Configure appropriate startup protection; repeat slow startup and prove genuine deadlock still fails liveness. |
| 5. Wrong database hostname: change only the lab application's connection host. | API reports dependency failure; suspect DNS or configuration. | Resolve the configured name inside the app's network, compare the intended name and inspect sanitized errors. | Correct configuration; check persistence and an informative failed-dependency response. |
| 6. Missing configuration key: remove one required nonsecret variable. | Startup fails or requests return errors; suspect incomplete configuration. | Validation message and effective configuration names, never credential values. | Restore the key and add startup validation; test missing-key behavior in CI. |
| 7. Dependency unavailable: stop the disposable database. | Requests slow or fail; suspect connection retries or exhaustion. | Request duration, pool usage, error rate and bounded retry behavior. | Restart dependency; verify recovery without an app restart and no duplicate writes from retries. |
| 8. Memory limit too small: lower a single lab container's limit. | Container terminates under a fixed small workload; suspect out-of-memory termination. | Termination reason, limit, workload size and peak usage when available. | Choose a measured limit or reduce allocation; rerun the identical workload within a resource ceiling. |
| 9. Unwritable data path: point a lab writer at a deliberately read-only mount. | Writes fail while reads work; suspect filesystem permissions. | Mount mode, effective user and permission error. | Provide a narrowly writable data mount; test writing as the intended nonroot user. |
| 10. Incompatible schema change: remove a field only in a disposable database copy. | Old and new application versions disagree; suspect migration compatibility. | Integration failures for both versions and migration history. | Rehearse expand/migrate/contract and a forward fix; prove mixed-version compatibility before contraction. |
| 11. Lost lab data: delete synthetic records only after making a verified backup. | Counts or checksums differ; suspect logical data loss. | Last known good timestamp, backup identity and expected record set. | Restore into a new database; validate rows, permissions and API behavior; record actual RTO/RPO. |
| 12. False-green pipeline: deliberately ignore a failing test command in a branch. | Pipeline appears healthy despite a known defect; suspect swallowed exit status. | Test report, command exit code and promotion dependencies. | Restore failure propagation and required gates; prove the same defect blocks deployment. |

Readiness controls whether a Pod receives Service traffic; liveness failure can restart its container; startup probes protect slow initialization. Choosing the wrong probe can turn a dependency problem into a restart loop. [Kubernetes probe documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

## Capstone assessment

Score each dimension from 0 to 3. **0:** missing, unsafe or unsupported assertion. **1:** works with step-by-step help on the happy path. **2:** repeatable implementation plus a demonstrated negative case. **3:** independently operate it, explain tradeoffs and handle an unfamiliar variation. Use evidence, not confidence, to assign the score.

| Dimension | Minimum evidence for 2 | Additional evidence for 3 |
|---|---|---|
| Reproducibility | Clean checkout, pinned dependencies/artifacts, versioned infrastructure and teardown. | Another person completes setup; you resolve one environment difference without undocumented manual repair. |
| Testing | Unit, real-dependency integration and deployed system checks; defect blocks promotion. | Explain coverage gaps, diagnose a flaky test and add a meaningful missing case. |
| Security | Least privilege, secret handling, isolated execution, restricted network exposure and threat model. | Demonstrate denied actions and credential rotation; explain accepted risks and controls. |
| Reliability | Compatible rollback and validated restore with measured recovery results. | Recover from a new bounded failure while preserving data correctness. |
| Observability | User-facing indicators, correlated logs and a tested actionable alert. | Diagnose an incident using evidence across components and remove an unhelpful alert. |
| Performance | Reproducible load baseline with throughput, errors and latency distribution. | Identify one bottleneck and validate improvement without shifting failure elsewhere. |
| Cost | Inventory, estimate, resource owner/expiry, cleanup evidence and actual-cost check. | Explain the largest cost drivers and a measured cost/reliability tradeoff. |
| Communication | Architecture diagram, decision records, runbook, release notes and postmortem. | Another person uses the documents successfully and you explain tradeoffs clearly in review. |

The year-end pass is **at least 20/24, every dimension at least 2, and no stop condition below**. This is a deliberately demanding curriculum gate. Revisit the weakest dimension instead of adding a new tool.

Stop the assessment if real secrets are committed; unintended public administrative access exists; a failed required test can promote a release; cleanup targets are ambiguous; destructive changes lack recovery evidence; privileged untrusted CI jobs can reach sensitive environments; or claims materially exceed measured evidence. Fix and reassess. Self-managed runners execute repository-controlled code, so runner isolation and trust levels deserve explicit review. [GitLab runner security](https://docs.gitlab.com/runner/security/)

## Independent handoff and portfolio

For the final assessment, ask a peer to use a clean environment and only the repository documentation. They should start the service, make one small change, follow the pipeline, interpret an alert and perform a documented rollback. You may answer clarifying questions, but record every missing instruction. If no peer is available, wait a week, use a clean environment and hide your personal notes; label that as self-assessment.

Then have the reviewer choose one known drill without revealing which configuration changed. Explain your investigation aloud. Time matters less than controlled reasoning, accurate communication and data protection. A failed attempt is followed by a corrected runbook and a repeat; it is not erased from the record.

Publish a compact portfolio: architecture and tradeoffs; infrastructure/configuration code; pipeline and test reports; one performance comparison; one restore report; two incident reports; cost/cleanup evidence; and a five-minute walkthrough. Include limitations such as “local single-node test” or “GCP adaptation demonstrated, cross-cloud failover not implemented.” Remove secrets and private identifiers.

An incident report should describe impact, timeline, contributing conditions, recovery and owned follow-ups. Avoid blaming a person for acting under incomplete information; improve the system and its checks. [Google SRE: postmortem culture](https://sre.google/sre-book/postmortem-culture/)

## Keep this reference useful for a year

Reserve one two-hour session each month for maintenance. Review the tools actually in use, their supported versions, release notes, security advisories and the official pages linked from the current module. Record the review date and the exact version you tested. Verify pricing and quotas before a cloud lab; do not assume last month's free allowance still applies.

Update one dependency group at a time in a branch, run the relevant checks and retain a rollback path. A newer version is not automatically urgent; a relevant security fix or approaching support end may be. Mark broken links and changed commands in the evidence log. Prefer a release-specific guide to a development-branch example.

Quarterly, rerun clean setup, a failed-deployment recovery and a data restore. Check that CI reports and backups are still readable and that unused cloud resources are gone. Keep a short “known limitations” list with owners and next review dates. Reliable engineering comes from keeping claims, evidence and operational reality aligned.
