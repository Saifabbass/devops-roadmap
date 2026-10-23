# Start here

This is your working reference for a year of deliberate DevOps practice. It starts with terminal, Linux and Git foundations for a beginner and plans around **two hours a day**. You do not need prior cloud experience. The plan contains 52 weeks, 13 assessment gates and about **728 scheduled hours**. Weeks are relative: begin whenever you are ready. They are learning units, not deadlines.

The intended outcome is a teammate who can build, test, deploy, diagnose, recover and explain a small service with sound engineering judgment. No course can confer twenty years of operational experience or guarantee a bulletproof system. This course makes the qualities you asked for observable: correctness, security, recovery, performance, scalability and maintainability.

Use this as your home base. The official documentation remains part of the reference because commands, provider behavior, supported versions and prices change. You should not need to invent your own sequence or wander through resource lists.

## Your first action

Open [Set up your learning lab](lab-setup.md), then **Week 1** in the study plan. Follow the explanations and command blocks in order, compare each expected result, and complete its independent practice. You do not need a cloud account, a Kubernetes cluster or a paid course to begin.

The first four weeks teach foundations through small operational tasks. If you already know a topic, prove the weekly outcomes in a fresh environment and use the remaining time to improve your evidence, explain a failure, or help another learner. Familiarity alone does not waive the gate.

## How to use the fieldbook

1. **Study plan:** choose the current week. Read the in-course concepts and explained commands, then build, diagnose the controlled fault, and complete independent practice. Each fourth week has a level capstone with acceptance checks and a rubric.
2. **Handbook:** use the explanations when a tool's behavior is unclear. Start with request flow and testing boundaries.
3. **Repository library:** read the principles and exercises synthesized inside the course. All 30 requested projects have an assessment; installing every project is not required.
4. **Roadmap and learning sources:** use the in-course synthesis of the ten learning repositories and the roadmap coverage analysis as companions to this sequence. External sources are optional depth after the core explanation.
5. **Templates:** record evidence, decisions, incidents, runbooks and service readiness.

Progress is stored in this browser when local storage is available. It is not synchronized to roadmap.sh or GitLab. Export a progress backup weekly and keep the JSON with your learning notes. Browser storage can be cleared, and moving the HTML file or using another browser may create a different storage context. Import your export to restore it. If storage is unavailable, you can still read everything and export the current session's progress.

All 52 guided lessons, handbook text and catalog entries are available offline. Download the lab files before going offline; installing dependencies and performing cloud exercises require connectivity. External documentation links need internet access. Markdown and JSON source files are included beside the HTML so your work is not trapped in a particular viewer.

## Your two-hour routine

Use a normal session as **15 minutes retrieval, 25 minutes focused reading, 65 minutes practice, 15 minutes evidence and cleanup**. The operations chapter gives a slightly different split for incident drills; choose the split that fits the exercise.

| Day | Purpose | What you should leave behind |
|---|---|---|
| 1 | Understand the current concept and observe a small example | A prediction, a diagram or a short explanation |
| 2 | Build the smallest useful implementation | A working increment and a test |
| 3 | Extend and automate it | A repeatable command or configuration |
| 4 | Verify boundaries and negative cases | Evidence that incorrect behavior is rejected |
| 5 | Inject the week's controlled failure | Diagnosis, fix and regression evidence |
| 6 | Rebuild or repeat without the tutorial | Proof that you can reproduce the result |
| 7 | Review, clean up and catch up | Evidence note, recall practice and next objective |

Day 7 is deliberately flexible. Do not compensate for a missed session by rushing an unsafe cloud change. Every fourth week concentrates on assessment and recovery; use it to repair gaps. If a gate needs an additional week, extend the calendar and keep the prerequisite order. Drop optional tool exercises first. A 52-week target is useful; falsely marking skills complete is not.

Read the lesson first. Open the primary references at its end when you need the underlying specification, a version-specific change or deeper treatment. The core teaching, commands, expected results, diagnosis, hints and answers are already in the lesson.

## One application, increasing responsibility

Use the [Taskboard project specification](project-spec.md) for exact endpoints, response formats, ownership rules and the test matrix. It defines what you will build; the weekly plan defines when and how to prove it.

The main project is **Taskboard**, a small API for creating, reading and completing tasks. Start with a simple Python service, then add PostgreSQL and isolated tests. Later stages package it, deliver it through GitLab, operate it on VMs and Kubernetes, and add observability and recovery.

| Stage | What changes | What you must understand |
|---|---|---|
| Weeks 1–4 | Linux process and small API | Process lifecycle, network path, configuration, errors |
| Weeks 5–8 | Image, database, test boundaries | Packaging, persistence, validation, identity scope, restore |
| Weeks 9–12 | GitLab delivery | Trusted jobs, artifacts, release controls, rollback |
| Weeks 13–20 | AWS and Terraform | Identity, networks, state, plans, cost, reproducibility |
| Weeks 21–24 | Ansible VM platform | Configuration ownership, idempotency, hardening, rebuild |
| Weeks 25–32 | Kubernetes and GitOps | Reconciliation, routing, probes, policy, capacity, drift |
| Weeks 33–36 | Observability and incidents | Signals, SLOs, alert actions, evidence, communication |
| Weeks 37–40 | GCP and platform comparison | Transferable concepts and cloud-specific behavior |
| Weeks 41–48 | Security, data, scale, internals | Trust, recovery, overload, upgrades, developer experience |
| Weeks 49–52 | Independent capstone | Defensible requirements, measured behavior, handoff |

Use **podinfo** briefly when you need a known application to test a new platform. Return to Taskboard to prove that you understand application and infrastructure interactions. Keep podinfo's debug/failure endpoints private and free of real secrets.

Do not start with microservices, service mesh, multiple CI systems or active-active multi-cloud. Add a component only after naming the requirement it solves, its failure modes and its ongoing cost. Those are design decisions you should be able to defend.

## Lab environment and budget

The required learning route is **local and free of cloud charges**. Use [Learn without a cloud bill](free-learning.md) and the Free local practice panel in cloud-dependent lessons. Paid provider execution is a separate optional extension. No account, subscription or resource has been created for you.

On Windows, use WSL2 with a supported Ubuntu release or a disposable Linux VM. Use the in-course [lab setup guide](lab-setup.md), which includes installation and first-tool checks, with official sources at its end. If WSL is already configured, inspect it before changing anything. Keep Linux project files in the Linux filesystem where practical. Use a VM for exercises that need a full isolated host or where WSL networking/service behavior would obscure the lesson.

Begin with a shell, Git and Python. Add Docker at week 5, cloud CLIs at the relevant cloud stage, Terraform at week 17, Ansible at week 21 and local Kubernetes at week 25. The relevant lesson introduces installation commands and prerequisites; record exact versions and verify the current official release instructions before installation. Do not install the 30 audited projects together.

Hardware needs vary. On a constrained computer, run only the stack needed for the current lesson. Stop observability systems before running multiple Kubernetes nodes or database operators. A single-node local cluster is adequate for many workload lessons; it does not demonstrate physical node or zone resilience. If an exercise cannot run, record it as designed or deferred, not completed.

Before a cloud lab, write down the account/project, region, identity, planned resources, current price estimate, maximum duration and cleanup steps. Configure billing notifications. AWS and GCP budget notifications do **not** reliably act as a hard spending cap. Include disks, snapshots, NAT gateways, load balancers, external IPs, logs and egress. Re-check the provider inventory after teardown and billing after its reporting delay. [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html), [Google Cloud budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets).

Use free local emulation to test specific interfaces, not to claim cloud competence. Real IAM, quotas, managed networking and provider behavior require live evidence. You can complete the local engineering path and its local acceptance checks while recording provider implementation separately as unattempted. Do not create EKS or GKE resources for the free learning track.

Read [Learn the judgment behind the commands](senior-practice.md) for the recurring decision questions and independent-practice rubric.

## Evidence is the completion rule

The portal has four states:

| State | Meaning |
|---|---|
| Not started | No meaningful work yet |
| Learning | You are reading or experimenting with guidance |
| Built | The exercise works, but independent verification is unfinished |
| Proved | You completed the listed checks, diagnosed the failure and linked evidence |

Use the evidence note for a repository commit, test report, incident note or concise measurement. A green checkbox alone is not evidence. Revisit the previous week's concepts after seven days and the previous month's after about four weeks. Explain from memory, then verify against documentation.

Every gate asks you to explain a tradeoff, rebuild a component, diagnose a failure and leave another engineer useful instructions. These habits make your knowledge valuable to a team.

## Learning with an AI tutor

Ask for questions, hints and reviews before full solutions. Try the exercise yourself, preserve the error, and state your current hypothesis. Use this reusable prompt:

```text
I am following Week [number] of the DevOps Engineering Fieldbook.
My objective is [outcome]. My environment and versions are [details].
Expected behavior: [expectation].
Observed behavior and sanitized evidence: [evidence].
My current hypothesis is [hypothesis].
Ask me one discriminating question or suggest one small diagnostic check.
Do not give me the complete solution yet.
After I fix it, challenge my explanation and ask for a regression test.
```

For an assessment, request an unfamiliar fault within a disposable environment and ask the tutor not to reveal the cause. You must understand and review any proposed command before running it. Use synthetic data and keep credentials out of conversations and evidence files.

## What was researched and what was not tested

This edition reviewed all 30 repositories listed on findarepo's 2026-10-18 DevOps snapshot and all ten repositories in the supplied DevOps Daily article. Reviews used primary repository READMEs and selected documentation, configuration, tests, security and licensing files. This is a suitability review, not a security certification or exhaustive code audit.

The roadmap investigation combined repository source inventory with REA observation of the live page and GitLab CI topic panel. The detailed report distinguishes source commit identity from live website observations. The roadmap is used as a coverage map, not treated as a strict prerequisite graph.

The supplied original Taskboard starter/reference has local unit, adapter and HTTP test evidence. PostgreSQL, Docker/Compose, GitLab, Kubernetes and provider exercises have not been executed by the course author in this environment. Upstream repository reviews are source inspections, not execution or security certifications. Read the included validation reports for the exact scope; a syntax check is not a completed cloud lab.

Refresh versions and source links at each four-week gate. Read the matching release documentation before applying old snippets. Use the monthly maintenance procedure in **Assessment and operations** so this reference stays useful throughout the year.
