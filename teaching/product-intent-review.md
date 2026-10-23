# Dev Oops! learning intent review

Reviewed 21 October 2026 against the previous authored objective and the current request for a public, beginner-friendly, zero-cloud-bill learning route.

## Assessment

The expanded course substantially matches the requested teaching format: 52 guided lessons, 13 level capstones, original synthesis of all 30 requested project repositories and ten learning repositories, staged application code, meaningful test boundaries, command explanations, expected results, controlled failures, expandable hints/answers and references after the teaching. It is more than a list of commands or external links.

It does not establish that a learner has twenty years of operating experience, that every command has been executed on its advertised platform, or that a resulting service is bulletproof. Its strongest defensible outcome is progressively demonstrated engineering capability, with explicit environment and evidence boundaries. The added senior-practice handbook makes judgment, diagnosis, recovery, tradeoffs and handoff recurring assessment criteria.

## Concrete corrections in this review

| Finding | Correction |
|---|---|
| The old zero-budget route deferred provider gates without a guided alternative in every affected lesson. | Added 11 explicit Free local practice routes: weeks 13–16, 18, 20, 24 and 37–40. Each has prerequisites, explained commands, expected results, acceptance criteria, cleanup and limits. The free-learning handbook distinguishes local completion from optional real-provider proof. |
| Week 29 introduced a StatefulSet while retaining week 27's PostgreSQL Deployment. Both matched the same Service selector, allowing requests to reach different databases. | Retire only the disposable network-probe Deployment, waiting for foreground deletion, before creating the persistent database. See week-29.json, first build step. |
| Week 29's migration Job had no identity selected by the existing database NetworkPolicy. It could not reach PostgreSQL on the enforcing cluster. | Give migration Pods a distinct label and narrowly scoped database/DNS policies. Keep the HTTP Service's application selector distinct, and remove the temporary policies at cleanup. |
| Week 31 awaited a private-image rollout before creating its image-pull Secret. | Create the read-only registry Secret and its manifest reference before promoting and synchronizing the image. |
| The operations handbook assumed prior Linux/Git/programming familiarity despite the beginner route. | Point beginners to the foundations and retain the operational rubric as a later assessment. |
| Week 9 assumed a runner before installation was introduced in week 10. | Add an explicit local runner bridge: basic Docker-executor registration first, with privileged mode off, then the separate protected image runner in week 10. No purchased minutes are required. |

The current source contains 545 command blocks, including 15 new local-route blocks. This count is coverage information, not proof of educational effectiveness.

## Checks actually executed

- Current application source: **38 unit and HTTP-adapter checks passed** using the existing authoring Python environment.
- Actual local Uvicorn listener: **10 HTTP system checks passed**; the one authentication case was intentionally skipped because this run uses stage 03, which has no authentication. The adapter suite separately exercises synthetic-user isolation; neither run establishes PostgreSQL ownership behavior.
- All 15 added local-route Bash blocks and the changed Kubernetes build blocks passed Bash parsing. Embedded Python compiled. The trust-condition exercise ran: its intended case was allowed and all five changed conditions were denied. It explicitly uses fabricated dictionaries, not authenticated tokens.
- Full lesson coverage, embedded payload and command syntax are recorded separately in validation-structure.json after the site rebuild.

The tests emitted the existing Starlette/httpx adapter deprecation notice. A local pytest cache-write warning did not affect the HTTP assertions. No cloud resources, provider accounts, paid services or learner machines were created or modified during this content audit.

## Remaining limits and next validation priorities

1. **Run the Linux stack end to end.** Real PostgreSQL integration, container builds, Compose backup/restore and the new two-project recovery procedure remain unexecuted on this Windows authoring host. Execute them on the documented Ubuntu/Docker route before claiming those labs are verified.
2. **Run the cross-week Kubernetes sequence.** The week 29 and 31 corrections follow the actual selectors, policies and deployment order, checked against primary Kubernetes documentation. They still need execution on the specified kind/Cilium cluster; syntax checks do not prove networking or lifecycle behavior.
3. **Pilot with a beginner.** Setup, copying files into WSL, starting a local VM, initial GitLab runner registration and long cloud explanations are the highest-friction transitions. The free local alternatives preserve useful mechanisms but do not replace provider-specific operational experience.
4. **Assess independent transfer.** Local progress remains a learner evidence record. A nonempty note cannot validate its truth. The senior-practice rubric asks for a fresh rebuild, competing-hypothesis diagnosis, denied-action evidence, measured recovery and another operator's handoff wherever possible.
5. **Maintain the reference.** Pins and primary links are dated snapshots. Review tool support, dependency advisories, provider behavior and free-service limits at the documented monthly maintenance interval. Do not silently promise permanent zero-cost hosted quotas or indefinite compatibility.

## Primary sources for the corrected mechanics

- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/) — a Service selects the matching Pods; a Deployment and StatefulSet are not separate routing boundaries by themselves.
- [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/) — Pod selection, ingress/egress isolation and additive allowed traffic.

Publication, public-domain configuration and visual checks belong to the separate site delivery review. This document reports content and lab validation only.
