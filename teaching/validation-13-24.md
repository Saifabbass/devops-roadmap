# Weeks 13–24 validation — 20 October 2026

The user explicitly authorized “Expand the lessons and keep the current design.” These twelve final JSON files preserve their original curriculum week, phase, title and outcome. There are substantive capstones in weeks 16, 20 and 24.

## Performed

- Required teaching fields and all command objects inspected; 124 command blocks include explanation, expected observation and troubleshooting.
- Git Bash 5.2.37 parsed 122 Bash blocks with `bash -n`.
- Python parsed 11 embedded Python blocks; PyYAML 6.0.3 parsed 12 YAML/configuration blocks; python-hcl2 8.1.4 parsed 11 HCL/backend/test blocks.
- The final syntax report is `teaching/validation-13-24.json`. No provider, VM or container commands were executed by these checks.
- Current primary documentation checked for AWS CLI/SSO, S3 version/lock behavior, GitLab protected MR resources and ID-token claims, Terraform releases/backend/mocks, Ansible check/diff/Vault/modules, Docker Ubuntu installation and PostgreSQL restore mechanics.
- Reviewed actual included Taskboard README, runtime/test entry points and Compose topology. Replaced a test-client check that required an absent runtime-only dependency with a separate real HTTP restore listener.
- Corrected AWS CLI setup prerequisites, an interactive Python stdin conflict in the cost worksheet, IPv4 /32 validation, exact state-denial commands, protected feature-branch bootstrap, MR/main role separation, and runtime digest inspection.

## Important teaching boundaries

Week 20's primary path executes a live plan inside a protected same-project `iac-review` merge request. The plan role reads only its state/managed bucket with writes restricted to the lock object. Apply authority trusts protected main push pipelines. Untrusted MRs run offline checks only. A post-merge plan is a fresh independent review and is explicitly not a substitute for the MR requirement. GitLab protected-resource prerequisites and tier/version considerations are written into the lesson.

Weeks 21–23 deliberately operate the memory-stage service to isolate host configuration and hardening. Week 24 deploys the tested authenticated stage-07 image with PostgreSQL, replaces the VM, restores a separate database and checks the known task through HTTP. It does not confuse memory process recovery with data recovery.

## Not performed

This Windows authoring host has no operational Linux VM/WSL or Docker daemon. No real AWS IAM/SSO/S3/EC2, Terraform provider execution, GitLab job, Ansible SSH run, package upgrade, Docker/Compose operation or PostgreSQL restore from these lessons was executed here. Syntax validation does not establish provider authorization, package compatibility, convergence or recovery success. Those remain explicit learner acceptance gates; no paid resources were created.

## Publication and maintenance

Final `lessons/week-NN.json` files are canonical. Some `author_NN.py` scripts predate final review corrections; do not regenerate lessons from them. Exclude authoring scripts, `validation-lib`, `validation-tmp`, caches and private execution evidence from the public course bundle. The validation libraries live only on D: and contain no learner credentials.
