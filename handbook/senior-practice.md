# Learn the judgment behind the commands

The target is an engineer who can explain, test and operate a service responsibly. Experienced engineers do not know every command from memory. They make assumptions visible, reduce uncertainty with evidence, limit the consequences of a mistake and leave a recoverable system for the next person.

This course starts with small local experiments and grows those habits across delivery, infrastructure, security, reliability and recovery. Completing it can produce a strong portfolio and practical skills. Twenty years of incidents, teamwork and production responsibility cannot be awarded by a website.

## Ask these questions before every change

1. **Requirement:** What user problem does this solve? Write one observable outcome and one thing outside scope.
2. **Simplest working design:** Can the existing platform meet it? Explain the operating work each new component adds.
3. **Failure boundary:** Which user requests or stored data could this change affect? Identify the owner, permissions, environment and irreversible part.
4. **Evidence:** What observation would prove success? What negative case would expose a misleading green result?
5. **Recovery:** Can the previous application read the changed data? Specify when to roll back, when to roll forward, and how to restore.
6. **Operation:** Who gets the alert, what do they do first, and where is the runbook? Record the known limit and next review date.

For example, two replicas of an in-memory API do not make task data durable. Before increasing replicas, trace a task through the process, database, volume and backup. Test the failure boundary you actually promise to survive. A process restart, a disk loss and a regional outage need different evidence.

## Use a decision record before choosing a tool

Write five short paragraphs: the requirement; two plausible options; the choice and its cost; the failure/recovery plan; and the observation that would make you reconsider. For a small internal service, a VM with a supervised process may be easier to operate than Kubernetes. Kubernetes becomes justified by concrete scheduling, rollout or platform requirements, with capacity and maintenance ownership included.

## Score evidence at each four-week capstone

Score each row **0: absent**, **1: completed with the guide**, or **2: explained and repeated independently**. This is a learning rubric, not a professional certification.

| Capability | Evidence for a score of 2 |
|---|---|
| Understanding | Predict the result and explain the mechanism before running a command. |
| Construction | Rebuild from a fresh checkout with documented prerequisites. |
| Diagnosis | Test competing hypotheses and identify the failing boundary without opening the answer. |
| Security | Demonstrate a denied action and explain whose authority is being exercised. |
| Recovery | Restore useful behavior and meaningful data; measure time and loss where relevant. |
| Judgment | Explain a simpler alternative, a tradeoff and an accepted limitation. |
| Handoff | Another learner can follow the runbook; otherwise label it a fresh-environment self-review. |

A missing security or recovery check stays missing even if the total score is high. Repeat the weakest experiment before moving on. For cloud weeks, score the free local assessment and record real-provider execution separately. A local pass never establishes AWS IAM, GCP IAM or managed-cluster behavior.

## Practice transfer instead of memorization

After a successful lab, change one bounded condition: a new port, a smaller memory limit, a missing configuration key, a different identity or a delayed dependency. Predict the symptom, write two hypotheses, then choose the smallest observation that separates them. Keep the successful and failed results. At the next capstone, repeat one older exercise without the original command block.

Before the final handoff, include a release record, a denied-access test, one measured load run, an isolated restore, two incident reports, a cost/resource inventory and an explicit list of unverified environments. Review the evidence with another person when possible. Treat disagreement as a prompt to run a discriminating experiment.

## References used for this practice

- [Google SRE: effective troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) — hypotheses, observations and diagnosis.
- [Google SRE: postmortem culture](https://sre.google/sre-book/postmortem-culture/) — learning from incidents and following through on prevention.
- [AWS Well-Architected: general design principles](https://docs.aws.amazon.com/wellarchitected/latest/framework/general-design-principles.html) — testing, measured decisions and reversible evolution.

These references support the practice; the questions and rubric above are original course teaching.
