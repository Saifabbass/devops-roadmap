# Learn without a cloud bill

Every lesson is open to read. The core practice uses your existing computer, Ubuntu, local containers and local Kubernetes. No paid cloud account or subscription is required. Internet access, available disk space and the computer you already use are still prerequisites; the course does not provide remote compute.

The cloud lessons now begin with **Free local practice**. Complete its commands and acceptance checks, then record **Scope: local practice** in your evidence. The separate optional provider lab shows how those concepts map to AWS or GCP. Opening an account or following provider creation commands is not necessary for the free track. Provider budgets are alerts, not a hard spending cap.

## Choose the right route

| Weeks | Free core practice | Additional provider evidence, only if chosen |
|---|---|---|
| 1–8 | Ubuntu, Python, Docker, real local PostgreSQL and recovery | None needed. |
| 9–12 | GitLab Free project and a runner on your own disposable Linux VM | Hosted runner usage depends on the provider's current allowance. |
| 13–16 | Identity denials, private request flow, local backup/restore, architecture/cost review | AWS SSO/IAM, VPC/EC2, S3 and actual billing behavior. |
| 17–20 | Real Terraform local state, separate roots, drift, tests and offline delivery checks | S3 backend isolation/locking and GitLab-to-AWS federation. |
| 21–24 | Ansible against your local disposable Ubuntu VM; isolated local rebuild/restore | Recreating an AWS VM and proving cloud access boundaries. |
| 25–36 | kind Kubernetes, network policy, GitOps, observability and incident practice | Physical node, zone and managed-service resilience are separate claims. |
| 37–40 | Identity tests, private containers, trust-condition review and local Kubernetes rollout | Google IAM/IAP/WIF/Cloud Run/GKE behavior. |
| 41–52 | Supply chain, compatible migrations, performance, disaster recovery and independent handoff | Only provider-specific promises you explicitly choose to verify. |

The local alternatives teach the transferable mechanism. They are not cloud emulators or a shortcut to claiming production cloud experience. You can finish the free learning track while leaving every real-provider execution record unattempted.

## GitLab without buying compute

Use a free project and a runner you own on a disposable local Ubuntu VM. Week 10 gives the runner installation and registration commands. To prepare the ordinary runner for week 9, follow only its installation/register portion first; select the **Docker executor**, use a standard Python image, enable untagged jobs, and leave **privileged mode off**. Return to week 9 for the first lint/unit pipeline. Week 10's separate protected image runner uses its documented tag and isolation settings. Do not merge the two runner trust boundaries.

Your VM must have Docker from week 5 and outbound access to GitLab and the image registry. Check the free account's current storage/registry limits before publishing artifacts; retain small reports and expire old artifacts. If account or hosted quota setup is unavailable, continue running the identical lint/test/build commands locally and label hosted pipeline execution pending. Buying minutes or adding a payment card is not a course requirement.

## Use local VMs for Ansible

Weeks 21–23 already accept a local disposable Ubuntu VM. Keep console access, install the SSH server using the supplied prerequisite commands, confirm the host-key fingerprint from the VM console, and use the VM's actual private address in your inventory. Use the distribution's existing networking; do not expose SSH on your router. A loopback/local connection does not demonstrate remote SSH behavior.

## How to record completion honestly

Keep the existing evidence states, but write the scope on the first line: **local**, **provider**, or **design review**. Include the environment, exact command, result, negative check and limitation. For weeks with a Free local practice panel, its acceptance list is the local completion gate. The optional provider capstone's acceptance list remains the separate provider gate.

For example: “Local week 18 passed: distinct dev/stage Terraform roots and outputs, reviewed plans, state files identified. AWS S3 permissions and distributed locking unattempted.” This is a stronger record than a vague “Terraform complete.”

## Keep the course itself free

Reading needs no account. Progress can stay in your browser and be exported as JSON. Saving across devices, if offered, is optional; it must not gate the lessons. No paid API, remote terminal, automated cloud provisioning or email service is needed to teach this course.

Continue with [Set up your learning lab](lab-setup.md) and [Learn the judgment behind the commands](senior-practice.md).
