# How the roadmaps and ten learning repositories become your curriculum

Reviewed 20 October 2026. Designed for 14 hours per week, a CS graduate familiar with Linux, programming and Git, starting cloud and DevOps from zero. This research supports the handbook; it is not a claim that every linked tutorial was executed or that any example has passed a production security audit.

## What was actually inspected

- The [DevOps Daily selection article](https://devops-daily.com/posts/top-github-devops-learning-repos-2026), all ten linked repositories' README files, full GitHub file inventories for the nine companion repositories, and selected exercises, tests and deployment files listed in `learning-repos.json`. Roadmap source inventory was scoped to its DevOps content directory.
- The current [developer-roadmap source](https://github.com/nilbuild/developer-roadmap), including all 140 filenames, content hashes and URLs under `roadmaps/devops/content`; eleven selected topic files were read in full.
- The actual [roadmap.sh DevOps interface](https://roadmap.sh/devops), using the requested REA skill and tools. A temporary headless browser loaded the page; a second successful scenario clicked the GitLab CI node and waited for its resource panel. Both browser processes were cleaned up by REA. No account was created and no progress, subscription or AI-chat action was submitted.
- The live page's embedded graph was parsed as JSON data without executing the embedded source. It contains 171 graph nodes, including 139 topics/subtopics, and 60 explicit edges. The rendered SVG has 173 node groups: the two additional groups are legend items. The GitHub inventory has one content file not represented by a live topic: `contabo`. Counts describe the captured representations, not an assertion that all graph edges are learning prerequisites.

This investigation used repository tools for source analysis and REA for browser behavior analysis. Native decompilation would add no evidence about this public content repository.

The source commit inspected for developer-roadmap was [`46aa6a6b533feda20a8f36172188ddb4d7e82ed4`](https://github.com/nilbuild/developer-roadmap/tree/46aa6a6b533feda20a8f36172188ddb4d7e82ed4). The live page graph reported its own update time of 29 July 2026. A newer repository commit does not establish that the website deployed it. File inventory and live graph are therefore retained separately.

## The central decision

Use roadmap.sh as a coverage map. Use the handbook as the order of work and the definition of competence. The live legend identifies alternatives and says ordering is not strict. Tool names beside one another do not mean you must learn every tool.

The GitLab CI node opens a concise definition, links and learning-status controls. Its source has the same four resource destinations as the observed panel. That is useful orientation; it does not specify a runner trust boundary, identity federation, deployment rollback test or measurable graduation task. Checking “Done” cannot demonstrate any of those capabilities. [Inspected topic source](https://github.com/nilbuild/developer-roadmap/blob/46aa6a6b533feda20a8f36172188ddb4d7e82ed4/roadmaps/devops/content/gitlab-ci@2KjSLLVTvl2G2KValw7S7.md)

Your path deliberately chooses Python/Bash, Linux, Git/GitLab, Docker, AWS first, Terraform, Ansible, Kubernetes, a single GitOps controller, Prometheus/Grafana/OpenTelemetry and then GCP. Reading alternatives is useful when writing a design decision; implementing all alternatives consumes time needed for debugging and recovery.

## Translating the actual topic map into the year

| Roadmap branch | Decision for your path | Evidence of competence |
|---|---|---|
| Programming, OS, terminal, Git and hosting | Weeks 1–4 teach terminal, Linux, Git, networking and small-service foundations, then verify them through service operations. Learners with prior experience can demonstrate the outcomes before extending the exercises. | Diagnose a failed process, permissions fault, port conflict and bad DNS; produce a useful merge request. |
| Networking, protocols, proxies and web servers | Weeks 1–4 first; revisit with VPCs and Kubernetes. Use one reverse proxy. | Trace DNS → TCP → TLS → HTTP → app → database and locate an injected failure. |
| Containers | Weeks 5–8, Docker and Compose. Treat LXC and Swarm as awareness topics. | Reproducible non-root image, persistent data, bounded resources, clean shutdown, tests and measured image size. |
| CI/CD and artifacts | Weeks 9–12, GitLab CI and its registry. GitHub Actions/Jenkins examples are translated, not added as second platforms. | Failed tests block a release; promote the same immutable image; prove rollback and preserve test reports. |
| Cloud providers | Weeks 13–16 establish AWS; weeks 37–40 translate to GCP. Avoid learning two clouds simultaneously from zero. | Explain IAM, network, compute, storage, billing and failure domains; reproduce a small deployment in each cloud. |
| Provisioning | Weeks 17–20 use Terraform. Learn other IaC approaches only as comparison. | Review a plan, protect remote state, detect drift, import safely and recover from an interrupted change. |
| Configuration management | Weeks 21–24 use Ansible on VMs. | A second run is idempotent, configuration is tested, SSH identity is verified and a rolling change can be reversed. |
| Orchestration | Weeks 25–32, local Kubernetes before short-lived managed clusters. | Diagnose scheduling, DNS, probes, resource and storage failures; prove disruption and rollout behavior. |
| GitOps | Weeks 31–32 introduce one controller after Kubernetes fundamentals. | Git records desired state; drift is reconciled; rollback is explicit; CI builds and tests artifacts. |
| Monitoring, logs and observability | Add basic logs early; deepen in weeks 33–36. | A user-centered SLI and SLO, useful alert, trace and runbook guide recovery from an unknown failure. |
| Secrets | Begin in week 1; deepen with GitLab identity, cloud IAM and Kubernetes. | No credentials in Git/images/logs; access and rotation tested; different environments have different permissions. |
| Cloud design patterns | Apply a few patterns repeatedly, especially bounded retries, timeouts, idempotency, queues and backup/restore. | Demonstrate their behavior when a dependency is slow, unavailable or duplicated work is delivered. |
| Service mesh | Optional late comparison only, after ordinary service routing, TLS, policy and observability are understood. | An architectural decision explains whether its operational cost is justified for this application. |
| Serverless and alternative hosts | One bounded comparison with a managed container/serverless service; no separate mastery track. | Choose a simpler hosting model when Kubernetes is unnecessary, with a documented cost and operations tradeoff. |
| Email protocols, BSD variants, alternate languages and alternate CI/cloud vendors | Lookup knowledge unless a real requirement appears. | Recognize their purpose and know where authoritative documentation lives. |

The complete factual topic inventory is in `roadmap-devops-topic-inventory.json`. `roadmap-live-graph.json` retains labels and display relationships. Neither copies the full lesson text.

## What the map does not make sufficiently explicit

The main DevOps graph has no dedicated topic nodes named unit testing, integration testing, system testing, incident command, backup restoration, cost controls or database migrations. This is a statement about the inspected graph, not a claim that the entire roadmap.sh website lacks related content. Observability, availability, secrets and cloud patterns do exist; they need much more practice than their individual nodes imply.

The curriculum therefore adds these continuous threads:

1. **Testing from the first service.** Unit tests exercise business rules with dependencies isolated. Integration tests use real boundaries such as PostgreSQL and queues. System tests exercise the deployed service through its public contract. Infrastructure checks validate rendered manifests, policy, plans and actual behavior. A test suite must demonstrate that it catches an intentional defect.
2. **Data safety.** Practice schema evolution, backwards-compatible deployments, backup restoration to an isolated environment, integrity checks, and measured recovery time and data loss. A backup file's existence is not a restore test.
3. **Delivery safety.** Separate untrusted merge-request jobs from privileged deployment jobs; promote immutable artifacts; expire review environments; rehearse rollback and forward repair.
4. **Security throughout.** Threat-model trust boundaries, use least privilege and short-lived identity, scan dependencies and images, verify artifact provenance, restrict network paths and rotate a deliberately invalidated credential.
5. **Operations and teamwork.** Write usable runbooks, incident timelines, decisions with alternatives, handover notes and postmortems with verifiable follow-up work. Have another person operate the service from the documentation when possible.
6. **Capacity, performance and cost.** Define a workload and latency objective before load testing. Report percentiles, error rate and saturation. Estimate and record cost; clean up every billable lab. No tutorial's “free tier” statement is a guarantee for your account.

## The ten repositories: exact jobs to give them

### 1. The-DevOps-Daily/devops-daily — guided exercises and explanations

Use one exercise matching the current week, then apply its idea to your own service. The inspected tree contains exercises, guides, quizzes, checklists and flashcards; its codebase also has tests and Docker configuration. Relevant exercises include Docker multi-stage builds, Terraform AWS VPCs, Ansible automation, HPA, GitOps and observability. [Repository](https://github.com/The-DevOps-Daily/devops-daily)

Concrete adaptations from inspected examples:

- The [VPC exercise](https://github.com/The-DevOps-Daily/devops-daily/blob/4cd12767d34f51510bfd08b05536c10dbcc6958a/content/exercises/terraform-aws-vpc.json) creates NAT gateways per availability zone and uses automatic apply approval. Estimate that architecture first; make the default lab smaller; review the saved plan before applying; record and verify cleanup.
- The [Ansible exercise](https://github.com/The-DevOps-Daily/devops-daily/blob/4cd12767d34f51510bfd08b05536c10dbcc6958a/content/exercises/ansible-web-server-automation.json) disables SSH host-key checking and uses a `latest` package variable. Replace those shortcuts with trusted host-key enrollment and a tested update/version policy.
- Treat its suggested exercise times as reading/building estimates, not proof that the outcome meets your acceptance gate.

### 2. nilbuild/developer-roadmap — coverage and navigation

Use the selected branches in the table above. Consult dedicated AWS, Docker, Kubernetes, Linux and Terraform maps only for the current capability. Keep a personal label per topic: “can explain,” “built,” “broke and repaired,” or “operated with evidence.” The last two are the important ones. Source and interface inspection are described above. [Repository](https://github.com/nilbuild/developer-roadmap)

### 3. bregman-arie/devops-exercises — retrieval and diagnostic challenges

Use 5–10 questions after a week's lab, with answers hidden. For any incorrect answer, create a small experiment and save its output. The inspected AWS section spans IAM, networking, recovery, costs and production scenarios; Terraform includes state, modules, import and production; GCP has projects, IAM and compute; CI/CD mixes platform-neutral questions with Jenkins examples. [AWS](https://github.com/bregman-arie/devops-exercises/tree/master/topics/aws) · [Terraform](https://github.com/bregman-arie/devops-exercises/tree/master/topics/terraform) · [GCP](https://github.com/bregman-arie/devops-exercises/tree/master/topics/gcp) · [CI/CD](https://github.com/bregman-arie/devops-exercises/tree/master/topics/cicd)

The README itself says learning DevOps is not learning every topic in the repository. It is an assessment bank, not a prerequisite-ordered textbook. Do not reward recalled wording when you cannot demonstrate the behavior.

### 4. kubernetes-the-hard-way — a late internals laboratory

Place it in weeks 45–46 after normal Kubernetes use. The inspected version uses four Debian 12 machines: jumpbox, one control-plane server and two workers. It teaches CA/certificates, kubeconfigs, encryption, etcd, control plane, workers and routing, ending with smoke tests. Its README explicitly identifies the result as unsuitable for production. [README](https://github.com/kelseyhightower/kubernetes-the-hard-way) · [Prerequisites](https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/52eb26dad1a3e9e8083a899bc854421eb4842a73/docs/01-prerequisites.md) · [Smoke test](https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/52eb26dad1a3e9e8083a899bc854421eb4842a73/docs/12-smoke-test.md)

Evidence: draw the trust and request paths, explain each component and its credentials, diagnose one controlled break, perform the smoke tests, and clean up. Recheck version support before starting; the observed tutorial version is not a recommendation to deploy that version publicly.

### 5. 90DaysOfDevOps — selected explanations, extended with your own lab

The [2022 index](https://github.com/MichaelCade/90DaysOfDevOps/blob/main/2022.md) uses Azure in its cloud segment and Jenkins/GitHub Actions in its CI segment. Keep container days 42–47, IaC days 56–62, Ansible days 63–69, and selected monitoring/data-protection chapters. Use [2023](https://github.com/MichaelCade/90DaysOfDevOps/blob/main/2023.md) for secure coding, supply chain, secrets, database recovery and operations discussions.

Each selected chapter should yield one changed artifact or tested hypothesis. The “90 days” framing is not your completion schedule, and the 2022/2023 examples need current documentation alongside them. AWS and GitLab replace the providers and CI tools outside your focus.

### 6. milanm/DevOps-Roadmap — a second opinion on scope

Use at the start and quarterly reviews, about 30 minutes each. Its main README has twelve subject sections, including software engineering practices, plus security references. Compare your evidence against those sections and create a missing-capability issue when warranted. [Repository](https://github.com/milanm/DevOps-Roadmap)

Its ordering differs from your dependency-based path, and its resources include both free and commercial material. It is a cross-check, not a second course to finish.

### 7. awesome-kubernetes — a constrained research index

Use when a lab creates a specific question: local cluster choice, managed Kubernetes, storage or policy. The inspected source has dedicated directories for installers, managed Kubernetes, official resources, learning materials and projects. [Repository](https://github.com/ramitsurana/awesome-kubernetes) · [Managed Kubernetes index](https://github.com/ramitsurana/awesome-kubernetes/blob/master/docs/managed-kubernetes/managed-kubernetes.md)

Choose at most two candidates, then verify their current official documentation and maintenance. The list contains older historical articles and platform names alongside current entries; inclusion is not a quality or compatibility guarantee. Produce a short decision with requirements, operating cost and rejected alternative.

### 8. awesome-sre — the human and operational layer

Weeks 33–36 and 41–44: follow its reliability, alerting, on-call, postmortem, capacity and performance sections. Prefer the primary Google SRE books and operators' own incident material. [Repository](https://github.com/dastergon/awesome-sre)

Produce an SLO document, alert/runbook pair, incident rehearsal and postmortem. A useful postmortem explains contributing conditions and improves defenses; it does not merely identify a person or a single “root cause.” Reading on-call stories does not equal on-call experience; record what your simulation actually tested.

### 9. podinfo — a reference workload and testing specimen

Use in weeks 25–36 to isolate platform learning from bugs in your own application, then compare its deployment practices with your service. Its inspected source includes handler tests, kind/Helm testing, chart probes, graceful termination, fault controls, metrics and tracing. [Repository](https://github.com/stefanprodan/podinfo) · [Unit-test workflow](https://github.com/stefanprodan/podinfo/blob/3e0ff8ae123b710bc91de1315cba0f996a8896c2/.github/workflows/test.yml) · [Cluster-test workflow](https://github.com/stefanprodan/podinfo/blob/3e0ff8ae123b710bc91de1315cba0f996a8896c2/.github/workflows/e2e.yml)

Translate its test stages into GitLab. Demonstrate readiness changes, injected latency, a failed rollout and recovery. Keep this workload private and use dummy values: it intentionally exposes environment/configuration inspection and failure endpoints. It does not replace your business logic, migrations or stateful recovery tests.

### 10. awesome-devops — tool comparison, with a strict time budget

Use the categories to locate candidates only when a requirement exists. Its source covers registries, CI/CD, monitoring, secrets, security, chaos and platforms; the chaos section includes network fault tools. [Repository](https://github.com/wmariuss/awesome-devops)

Spend at most 30 minutes making a shortlist, then use official project documentation. Deliver a decision, not more bookmarks. Do not introduce an extra platform merely because the list contains it.

## What changes in the source article's advice

The article is useful discovery, but popularity does not establish security, accuracy, suitability or teaching quality. Its suggestion to start the hard-way Kubernetes tutorial if you already have a plan is too early for someone new to cloud and DevOps. You will first learn containers, delivery, identity, networking and ordinary Kubernetes troubleshooting.

You also will not finish all ten repositories cover to cover. Each has a defined role above; your actual unit of progress is a working, tested, recoverable capability. The deliberate sequence is explain → predict → build → test → break → diagnose → recover → document → revisit.

## Evidence and update policy

- `learning-repos.json`: all ten decisions, inspected paths, source identities, time placement, exercises and limits.
- `learning-source-inventory.json` and `learning-source-identities.json`: companion repository path inventories and verified commit identities. One repository changed during inspection; its original inspected revision is retained explicitly.
- `roadmap-devops-topic-inventory.json`: complete 140-file public content inventory.
- `roadmap-live-node-inventory.json`: all 173 observed SVG groups.
- `roadmap-live-graph.json`: 171 serialized graph nodes and 60 edges, reduced to metadata.
- `roadmap-rea-evidence.json` and `roadmap-rea-interaction.json`: REA evidence IDs, selected actions, captured artifact hashes, coverage and cleanup.

Review sources at the start of each new technical phase and monthly for tools actively used. Pin the versions you actually test, consult deprecation notices, and update a lab only after reproducing its checks. No complete dependency audit, cloud deployment, arbitrary external-link crawl or full upstream test run was performed in this research. That boundary is intentional and recorded, so the handbook can distinguish verified observations from learning exercises still to be executed.
