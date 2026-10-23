# Use the resources to build competence

Your schedule is 52 weeks at two hours a day. The weekly curriculum defines the work, the failure to investigate and the evidence required to finish. These repositories supply explanations, examples and challenges inside that schedule. They are not ten additional courses.

Weeks 1–4 validate your existing programming, Git and Linux knowledge through service operations. Fill the weaknesses they expose. Keep developing Taskboard so each new tool solves a problem you understand.

## Your weekly resource routine

Start with the current week's outcome and “prove” conditions. Read its linked official documentation, then select at most one companion exercise below. Before following instructions, predict the result. Afterward, reproduce the idea in Taskboard and introduce the week's controlled fault.

Use each two-hour session roughly as follows:

- **15 minutes:** recall the previous lesson without notes and state today's question.
- **25 minutes:** read the relevant documentation or selected lesson.
- **65 minutes:** build, test or investigate your own system.
- **15 minutes:** record observations, remaining questions and the next action.

Across seven sessions, reserve time for verification, one failure investigation and a weekly review. These replace ordinary building sessions; they do not require extra hours. During review, answer 5–10 questions with solutions hidden, revisit one older topic and check the week's evidence. If you cannot explain a result, repeat a smaller experiment before advancing.

A useful note contains your prediction, the observed result, why they differed and a repeatable check.

## Use roadmap.sh as your coverage map

The [DevOps roadmap](https://roadmap.sh/devops) helps you see the field and find explanations. Its live legend identifies alternatives and explicitly treats ordering as flexible. You do not need every language, cloud, CI platform or monitoring product displayed.

The investigation inventoried 140 [DevOps content files](https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/devops/content) and used REA to inspect the live interface and GitLab CI resource panel. The captured graph had 139 topics/subtopics. Its display relationships are not verified prerequisites.

Apply this priority scheme:

| Priority | Your choices |
|---|---|
| Core | Linux, networking, Python/Bash, Git/GitLab, Docker, AWS, Terraform, Ansible, Kubernetes, testing, identity, recovery and observability |
| One implementation first | One reverse proxy, one GitOps controller, one image registry and one metrics/logging/tracing stack |
| Transfer after fundamentals | GCP in weeks 37–40; compare equivalent capabilities and important differences |
| Defer unless justified | Additional clouds, languages, CI engines, orchestration platforms and service meshes |

Mark a topic “can explain,” “built,” “broke and repaired,” or “operated with evidence.” Revisit the map at gates and in weeks 48 and 52. Its completion controls are convenient reminders, but your evidence determines competence.

The main graph does not give unit, integration and system testing, data restoration, cost controls or incident practice the explicit treatment your goals require. The curriculum adds these throughout. Security begins with the first service; it is not postponed until week 41.

## The ten repositories and their jobs

### DevOps Daily: one guided exercise for the current capability

Use [The-DevOps-Daily/devops-daily](https://github.com/The-DevOps-Daily/devops-daily) when you need a concrete introduction before adapting an idea to Taskboard.

The inspected exercise files support Docker multi-stage builds in weeks 5–8, AWS VPCs with Terraform in weeks 17–20, and Ansible server automation in weeks 21–24. Their prerequisites matter: the VPC exercise assumes an AWS account and basic tooling; the Ansible exercise assumes SSH and introductory Ansible knowledge. Read the matched exercise after those foundations.

Measure your own image, explain your routes and prove your configuration converges. Select later Kubernetes and observability exercises only for the current week's task. [Exercise directory](https://github.com/The-DevOps-Daily/devops-daily/tree/main/content/exercises)

### developer-roadmap: orientation and gap checking

Use [nilbuild/developer-roadmap](https://github.com/nilbuild/developer-roadmap) with the priority scheme above. Consult its dedicated AWS, Docker, Linux, Kubernetes or Terraform maps for a specific question, then return to the scheduled lab.

The GitLab CI node provides an introduction and links. Weeks 9–12 turn that orientation into runner trust analysis, meaningful tests, immutable artifacts and rollback evidence.

### devops-exercises: test understanding after building

Use [bregman-arie/devops-exercises](https://github.com/bregman-arie/devops-exercises) during weekly review and formal gates. Select AWS questions for weeks 13–16, Terraform for 17–20, Kubernetes for 25–32, and GCP for 37–40.

The inspected [AWS](https://github.com/bregman-arie/devops-exercises/tree/master/topics/aws), [Terraform](https://github.com/bregman-arie/devops-exercises/tree/master/topics/terraform), [GCP](https://github.com/bregman-arie/devops-exercises/tree/master/topics/gcp) and [CI/CD](https://github.com/bregman-arie/devops-exercises/tree/master/topics/cicd) sections contain questions and practical tasks. Answer before revealing solutions. Turn a mistake into an experiment, rather than memorizing the supplied wording. Save unfamiliar questions for week 48 to test transfer beyond rehearsed examples.

### Kubernetes The Hard Way: understand the machinery late

Use [kubernetes-the-hard-way](https://github.com/kelseyhightower/kubernetes-the-hard-way) in weeks 45–46, after you can deploy and diagnose ordinary workloads.

Its inspected sequence covers machines, certificate authority, kubeconfigs, encryption, etcd, controllers, workers, networking and smoke tests. The observed prerequisites require four Debian 12 machines; the resulting teaching cluster has one control-plane server and two workers. Its README explicitly excludes production readiness.

Your output is a component and trust map, explained configuration, a diagnosed failure and cleanup evidence. If hardware limits prevent execution, complete the curriculum's documented component-focused alternative and label it honestly. Recheck upstream requirements and supported versions before beginning.

### 90DaysOfDevOps: selected explanations, not another calendar

Use the [2022 index](https://github.com/MichaelCade/90DaysOfDevOps/blob/main/2022.md) selectively: days 42–47 support Docker, 56–62 support Terraform concepts, and 63–69 support Ansible. Selected monitoring and data-protection sections support later operations work.

The [2023 index](https://github.com/MichaelCade/90DaysOfDevOps/blob/main/2023.md) adds secure coding, scanning, signing, secrets, database recovery and day-two operations. Pair these with weeks 33–36 and 41–44.

The original cloud sequence uses Azure and its CI sequence uses Jenkins/GitHub Actions. Keep their general ideas while implementing AWS/GCP and GitLab. The indexes were inspected; every individual chapter was not executed or validated. Compare dated examples with current official documentation.

### Milan's DevOps Roadmap: a quarterly second opinion

Review [milanm/DevOps-Roadmap](https://github.com/milanm/DevOps-Roadmap) briefly in weeks 1, 13, 26, 39 and 52. Its twelve subject sections include software engineering practices, with additional security resources.

Identify a missing capability and create a remedial task. Keep the curriculum's sequence and limit this review to 30 minutes.

### awesome-kubernetes: answer one design question

Use [awesome-kubernetes](https://github.com/ramitsurana/awesome-kubernetes) during weeks 25–32, the managed-platform comparison in week 40, or the platform template in week 47.

The inspected structure separates installers, managed Kubernetes, official resources, projects and learning material. Shortlist at most two candidates for an actual requirement, then verify their current official documentation. Record why the chosen option fits and what it costs to operate. Historical links and product names remain; inclusion does not establish current suitability.

### awesome-sre: turn reading into operating practice

Use [awesome-sre](https://github.com/dastergon/awesome-sre) in weeks 33–36 and 41–44. Its reliability, alerting, on-call, postmortem, capacity and performance sections complement the curriculum's primary SRE readings.

Pair each reading with an artifact: an SLO, actionable alert, runbook, incident timeline or recovery experiment. During the capstone, use these to critique what actually happened. Describe lab incidents as simulations; do not present reading or rehearsals as production on-call experience.

### podinfo: separate platform behavior from application bugs

Use [podinfo](https://github.com/stefanprodan/podinfo) in weeks 25–36 when you need an understood workload while learning Kubernetes, GitOps and observability.

Its inspected files include HTTP health tests, a unit-test workflow, kind/Helm cluster tests and deployment probes. Translate relevant stages into GitLab. Test readiness, latency, failed releases and recovery, then repeat important checks on Taskboard. Podinfo cannot prove your business rules, schema migrations or database recovery.

Keep it private with dummy configuration: its intentional debugging and failure endpoints include environment/configuration inspection and process failure controls.

### awesome-devops: compare tools only when necessary

Use [awesome-devops](https://github.com/wmariuss/awesome-devops) for bounded comparisons around weeks 12, 24, 36, 44 and 47. Its categories include CI/CD, registries, observability, secrets, security and fault-testing tools.

Set a 30-minute discovery limit. Write the requirement before browsing, shortlist two options, and continue in primary documentation. Finish with a decision or experiment, not a larger bookmark collection.

## Correct examples before adopting them

Inspection found concrete shortcuts in the DevOps Daily examples. The Ansible exercise disables SSH host-key checking and specifies a `latest` package variable: replace those with trusted host-key enrollment and a tested update policy. The VPC exercise creates NAT gateways per availability zone and uses automatic apply approval: estimate the design, review the saved plan and verify cleanup.

Record corrections and their reasons. A tutorial's production-ready label does not replace your acceptance checks.

The detailed research records source revisions, inspected paths and limitations. These reviews did not execute upstream test suites or create cloud deployments. Your weekly evidence closes that gap gradually. The final standard is whether you can explain a change, test its risks, diagnose failures and help another engineer operate the result.
