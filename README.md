# Dev Oops!

Open the [public course](https://devoops.tech/), its [Pages address](https://devoops.pages.dev/), or [index.html](index.html) locally. Start with **Set up your learning lab**, then Week 1. This directory is the current editable source. The course starts with terminal fundamentals and builds toward operating a tested, recoverable service.

- 52 guided lessons with concepts, explained commands, expected results and troubleshooting.
- Controlled failure drills, expandable hints and answers, independent practice, and 13 level capstones.
- AWS, GCP, Kubernetes, Terraform, Ansible, GitLab CI/CD, Docker and unit/integration/system testing.
- Original in-course synthesis of all 30 findarepo projects and ten DevOps Daily learning repositories.
- Downloadable Taskboard starter/reference, tests, database migrations, container/CI examples and delivery helpers.
- Local browser progress, evidence notes, JSON export/import and printing.
- Eleven explicit free local routes for cloud-dependent lessons, with separate provider execution evidence.

Content edition: 2026-10-20; publication and content review: 2026-10-21. Weeks are relative learning units, with two hours a day as a planning guide. Repeat difficult work before advancing. The required route uses local practice without cloud charges. Optional provider exercises require an explicitly chosen account, budget and cleanup plan; the website never executes those lab commands.

## Offline use and lab downloads

The lesson text, handbook, repository synthesis and artwork work offline. External references and lab dependency installation require internet access. Extract the full course archive before opening it. The smaller [lab download](downloads/dev-opps-labs.zip) is also available from the setup guide.

Export progress weekly. Progress stays in this browser and origin; moving to a hosted site does not transfer it automatically. Import an exported backup to restore it.

## Public hosting and progress

The course is public on **Cloudflare Pages**. The Cloudflare zone and Pages association for [devoops.tech](https://devoops.tech/) are active, with certificates marked Issued. The complete 71-file public deployment includes the progress worker and enabled main-domain configuration. A direct check against Cloudflare's serving IP returned HTTPS 200 with valid TLS. The authoring machine's system DNS still does not resolve the domain; the [Pages address](https://devoops.pages.dev/) remains available for lessons and local progress.

Reading, lab downloads, local progress and JSON backups work without signing up. The deployed optional progress service has a Neon Free database with a restricted runtime role, verified Clerk Hobby production DNS/signing-key access, and its database connection in a Cloudflare encrypted secret. The live anonymous API returns JSON 401 with private/no-store caching; the Clerk UI and JavaScript bundles return 200 after redirects. The Pages fallback correctly offers a main-site link and export/import guidance without loading authentication. **Real signed-in save/load, cross-account isolation and deletion remain unverified**, because the authoring machine's system DNS has not resolved the main domain. See [Progress sync setup](deploy/PROGRESS-SYNC.md) for the implementation and configuration boundary.

The portable static edition still works without a server-side progress service. Its `index.html` belongs at the host's root, with the included assets and content directories alongside it. Hash routes need no rewrite rules. Use the reviewed public output or deployment archive; do not upload the entire editable source, dependency caches, learner evidence, `.env` files, credentials or database dumps.

See [Deployment record](DEPLOYMENT.md) for publication status and [Learning intent review](teaching/product-intent-review.md) for the content corrections, executed checks and remaining gaps. Free service allowances are finite; no course access depends on buying hosted compute or enabling optional services.

Resend and R2 are intentionally inactive. Domain renewal is separate from free hosting: the recorded quote is **US$29.99/year**, the current domain expiry is **20 October 2027**, and auto-renew is **off**.

## Edit and rebuild

The source edition includes Markdown, JSON and the current design modules. With Python 3.12 or newer:

```text
python tools/build_fieldbook.py
python tools/validate_fieldbook.py
python tools/validate_teaching.py
python tools/package_course.py
```

The builder uses only Python's standard library. It preserves the current design and embeds the authored lessons and repository teaching into the offline viewer. Lab dependencies are separate from the course builder.

## Validation and provenance

See [Validation](VALIDATION.md), [Taskboard validation](teaching/validation-taskboard.md) and [Learning intent review](teaching/product-intent-review.md) for the exact checks and limits. Local Python and HTTP evidence does not establish that cloud, cluster or GitLab exercises have run. Source reviews are suitability assessments, not upstream security certifications. See the research directory for repository and roadmap evidence.
