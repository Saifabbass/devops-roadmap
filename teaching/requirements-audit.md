# Objective-to-evidence audit

Reviewed 20 October 2026 against the complete goal-objective attachment and the later explicit instruction: **“Expand the lessons and keep the current design.”** The earlier redesign-only restriction does not prohibit this authorized expansion. Latest steering excludes Imagegen. This audit separates authored coverage, executed proof and publication/UI review; it is not a promise that every cloud lab has been run.

## Coverage snapshot

**52 lessons**; **13 capstones**; **120 concepts**; **158 questions**; **529 commandBlocks**; **40 repositorySyntheses**; **40 uniqueRepositories**; **52 mappedWeeks**.

All 52 lesson JSON files are present. All 13 scheduled capstones are present. The original 52-week sequence and outcomes remain supplied by curriculum.json; the renderer uses those canonical titles/outcomes. The repository synthesis contains 40 unique projects, selected as the exact 30 findarepo entries plus the exact ten DevOps Daily learning entries, and maps principles into every week. The renderer embeds those explanations, exercises, reasoned answers and limitations inside lessons and repository catalogs; it does not require readers to follow the source link to understand the core principle.

## Requirement matrix

| Explicit requirement | Current implementation evidence | Verification / remaining boundary |
|---|---|---|
| Preserve current design and expand in place | Existing curriculum, visual framework, mascots and source material retained; teaching renderer added to existing routes. | Root reports original weeks/repositories/learning/templates/sources unchanged against teaching-backup. Current rendered visual QA is separate. |
| Start from zero and explain course operation | In-course lab setup; weeks 1–3 explain terminal/files/processes, HTTP and staged Taskboard construction. Each lesson names prerequisites and working paths. | A first-time learner review remains valuable; no claim of universal zero-friction onboarding. WSL/VM setup must match the chosen supported route. |
| Actual commands and explanation in every lesson | Every lesson has ordered command blocks, purposes, explanations, expected observations and troubleshooting. Full configurations or included lab files are supplied. | Syntax checks exist by author range; provider/OS semantics remain live acceptance gates. This is more than field-count validation but not execution of the entire year. |
| Explain the knowledge, not a link collection | Concepts have mechanics, concrete examples and engineering decisions. Forty repository patterns are presented within week pages. | Source links support attribution and deeper reference. Review of primary docs does not mean every upstream project was installed or its test suite rerun. |
| Deliberately break, diagnose and recover | Every lesson has a scoped fault, diagnostic observations, hints, recovery and a verification command. | Local app/helper faults have executed evidence; infrastructure faults are authored procedures, explicitly unexecuted here. |
| Answers as dropdowns | Native details/summary disclosures render question answers, diagnostic hints/recovery and reference approaches. | Renderer inspection confirms behavior; keyboard/touch/rendered QA belongs to final UI checks. |
| Practice after every level | Capstones at 4/8/12/16/20/24/28/32/36/40/44/48/52 combine level skills, require evidence and give rubrics. Normal weeks have independent exercises. | Capstones have not all been performed. A rubric is a requirement, not a reported pass. |
| All 30 findarepo projects | Exact identity match to live category table; repository-synthesis.json includes specific principles, placements, exercises, avoided shortcuts and sources. | Live selection checked on audit date; source file inspections from stored research retained. Ranking/stars are not used as quality evidence. |
| All ten learning repositories | Exact identity match to live DevOps Daily table; ten additional unique syntheses with source/commit evidence. | Total 40 unique, not duplicate mentions counted toward coverage. |
| REA roadmap investigation | research/roadmap-analysis.md, roadmap-rea-evidence.json and roadmap-rea-interaction.json capture source inventory and live node interaction. | Existing evidence was adequate; inspection transferred into the staged path. No claim that a roadmap itself proves competence. |
| AWS | Weeks 13–16: SSO/least privilege/cost, VPC/EC2/tunnel, private versioned S3 and isolated restore, architecture/cost review. | Real AWS creation and denial checks were not run here. Budget alerts explicitly do not cap spend. |
| Terraform | Weeks 17–20: plans/state/modules, separate identities and backend keys, real S3 lock procedure, mock tests/drift/moved address, GitLab delivery. | Syntax/HCL checked; provider actions and locking are unexecuted. |
| Live plan in an MR, scoped apply | Week 20 has protected same-project iac-review, GitLab protected-resource settings, separate state-read/lock-only planning role and an MR plan artifact. Main push identity creates a fresh plan for review/manual apply. | Untrusted MRs receive offline checks only. Protected-main-only planning is explicitly a narrower fallback, not satisfaction of the live-MR outcome. GitLab project/runner/IAM execution is pending learner evidence. |
| Ansible | Weeks 21–24: inventory/roles/handlers, secret delivery, independent assertions, hardening/patches, exact-image platform rebuild and data restoration. | Linux/SSH/Ansible operations are unexecuted here. Memory-stage host lessons are explicitly separated from database-backed rebuild evidence. |
| Kubernetes | Weeks 25–32: reconciliation, Services/probes, enforcing CNI policy/RBAC, diagnosis, persistent state, HPA/load, GitOps and persistent-release recovery. | Real cluster execution is not claimed. NetworkPolicy requires an enforcing plugin; replica count is not durability or zone resilience. |
| GitLab CI/CD | Weeks 9–12 plus 20/39: runner trust, distinct tests, one built artifact, digest promotion, private target, stale-job rejection, scoped federation. | Included pipeline and deployment helpers support real execution; hosted/runner jobs were not run here. MR/offline versus protected-authority boundaries are explicit. |
| Docker | Weeks 5–8 teach image/runtime/filesystem/network boundaries and a complete private Compose stack. Later delivery preserves artifact identity. | Windows authoring host lacks operational Docker; no Linux build/Compose/PostgreSQL pass is fabricated. |
| GCP | Weeks 37–40: project/IAM/billing, private Compute Engine/IAP/object permissions, GitLab WIF/Cloud Run, optional GKE Autopilot and named-mode EKS comparison. | Full provider procedures exist, while design-only alternatives have narrower claims. Paid managed-cluster execution is optional as in the original outcome. |
| Unit, integration and system testing | Supplied staged app has pure/unit, in-process contract, real PostgreSQL integration and real HTTP system suites; CI and later gates preserve their distinctions. | 38 unit/contract checks and real memory HTTP checks are recorded; PostgreSQL and Docker execution are explicitly pending. MemoryStore authentication checks do not prove SQL owner isolation. |
| Security, scalability and production judgment | Least privilege/denials, runtime identity, signed artifacts, metadata/private networks, schema compatibility, controlled load, SLOs, measured recovery and choice of simpler platforms are taught at point of use. | No “bulletproof,” seniority or production-readiness claim follows from completing a lab year. Some extensions such as queues/PITR are explicitly optional/design-only. |
| References at lesson ends using badge style | lesson-view.js appends primary-source references after core teaching and maps them through devOppsResourceBadge. Repository sources are deduplicated into the same end section. | Root checked 181 unique authored URLs: 174 HTTP success/redirect, seven Ansible rate-limit responses, no 404. Availability is not factual correctness. |
| Remove montage link and fix overlaps | Existing design change scope retained; renderer and badge changes fit existing course. | Current viewport/mascot-eye/text-overlap proof belongs to final browser QA. Earlier research/final-ui-validation.json predates the new teaching pass and is not reused as fresh proof. |
| No Imagegen | Current authoring used code/text and existing visual assets only. | Historical Imagegen wording is superseded by latest steering. |
| Public usability and honest maintenance | Core teaching is bundled locally; private values are generated/entered by learner, not shipped. Source dates/versions and execution limitations are explicit. | Package exclusions, final artifact payload identity, navigation/copy/disclosures, responsive layout and publication remain root integration checks. No public deployment is claimed by this audit. |

## Level-by-level teaching evidence

| Level / weeks | Measurable integration project | Important distinction |
|---|---|---|
| 1 / 1–4 | Hand off a private Linux Taskboard service and diagnose startup failure. | Process/socket/HTTP observations are different proofs; memory is ephemeral. |
| 2 / 5–8 | Release and recover the private database-backed application. | Unit, real DB integration, real HTTP, immutable image and meaningful restore remain separate. |
| 3 / 9–12 | Release through GitLab, reject stale jobs and recover a failed deployment. | Serialization alone does not prevent old intent from deploying late. |
| 4 / 13–16 | Review AWS identity/network/storage, costs and recovery evidence. | Architecture targets are not measured availability claims. |
| 5 / 17–20 | Create/retire/recreate bounded infrastructure through reviewed GitLab plans. | Real live-MR planning uses a trusted source branch and separate planning authority. |
| 6 / 21–24 | Replace the VM, redeploy the same tested image and restore a known task. | Host reconstruction, image identity and data recovery all need proof. |
| 7 / 25–28 | Diagnose a blind Kubernetes symptom and restore declared behavior. | Healthy controllers are insufficient without a useful request. |
| 8 / 29–32 | Promote and recover a persistent Kubernetes release under observation. | Git revert cannot undo incompatible data/schema changes. |
| 9 / 33–36 | Operate an incident and prove a prevention check catches its recurrence. | A short window does not establish a monthly SLO. |
| 10 / 37–40 | Choose a managed platform and optionally execute a private GKE lab. | Mode-specific provider/customer duties and architecture-only claims stay explicit. |
| 11 / 41–44 | Recover service and meaningful data outside the normal environment. | Backup/credentials/runbook must survive the tested failure boundary. |
| 12 / 45–48 | Component diagnosis, template onboarding and independent review. | Hard Way scope is deliberately partial and records unfinished work. |
| 13 / 49–52 | Produce a defensible release dossier and hand it to a fresh operator. | Mechanical evidence checks do not establish authenticity or customer readiness alone. |

## Material issues found during this pass

Resolved in owned weeks: nonexistent AWS installer fallback; runtime restore verification requiring a test-only dependency; cost worksheet interactive input via consumed stdin; IPv4 CIDR validation; an implicit state-isolation check; direct protected-main bootstrap; missing primary live-MR plan; missing running-image digest observation; Vault input/password path clarity.

Cross-range findings are now resolved in the authored content:

1. Week 42 builds a distinct next reader that requires the new internal column, observes its rejection on the old schema, tests old and new readers on the expanded schema, and adds a scoped user-systemd backup timer with three-snapshot retention and cleanup. The public API contract remains unchanged. These Docker/database/timer procedures are explicitly unexecuted here.
2. Week 50 now records a clean source revision, builds one runtime candidate, records its immutable local image ID, selects it before HTTP testing, preserves test reports and verifies the deployed container against that same ID. It no longer re-resolves a mutable tag after testing.
3. All weeks 41–52 were read as UTF-8 after their author's correction; no replacement-character or identified mojibake markers remain. Final structural validation is recorded by the rebuilt viewer checks in validation-structure.json.
4. Week 39 protected-main bootstrap now uses a feature branch and reviewed merge. Week 40 includes the optional managed-cluster path and the labeled architecture-only alternative. All 52 files are present.

The exact-UUID deletion guard in week 15 now explicitly stops the shell before interpolation on invalid input; the same stop guard is now implemented in week 42 and its invalid-input path was executed without reaching SQL or Docker. There are no other unresolved material content-coverage gaps identified in this pass. This does not replace live execution or a fresh learner pilot.

## Executed versus authored

See teaching/validation-taskboard.md for actual Python/memory HTTP/helper runs, teaching/validation-13-24.md and validation-13-24.json for the AWS/Terraform/Ansible syntax scope, validation-25-40.json for that range, validation-structure.json for final payload/coverage checks, and validation-source-links.json for URL availability. Current source coverage is complete, and the material content findings above have been corrected. The final integrated artifact/UI/package checks remain separate completion gates.

No cloud account, paid resource, GitLab project or learner host was changed during this audit. Provider, Linux container, real PostgreSQL, Kubernetes and Ansible exercises remain authored procedures rather than claimed execution passes. The course requires learners to retain actual evidence for those gates.
