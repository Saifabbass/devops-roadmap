# Dev Oops! deployment record

Recorded 21 October 2026. This record contains public addresses and status only; deployment credentials belong in the provider's protected configuration.

| Item | Recorded status |
|---|---|
| Public course | Complete **71-file** public upload deployed successfully, including the worker and enabled main-domain progress configuration. [devoops.pages.dev](https://devoops.pages.dev/) remains available. |
| Custom domain | Cloudflare Pages shows [devoops.tech](https://devoops.tech/) **Active, SSL enabled**; Clerk certificates marked **Issued**. HTTPS returned 200 with valid TLS against its Cloudflare serving IP, and the delivered HTML SHA-256 exactly matched the published build. The authoring machine's system DNS still does not resolve the domain; this check does not establish propagation through every resolver. |
| Current editable source | This workspace's **site/** directory. Older root-level material and the previous D: edition are historical. |
| Access | Lessons and lab downloads are public; reading needs no account. |
| Local progress | Browser check passed: week-one state and note survived reload, exported JSON matched them, and importing the clean backup restored the original empty record. No sign-in required. |
| Progress database | Neon **Free** project **Dev Oops Progress**, Frankfurt, created; schema applied. Restricted **progress_app** runtime role verified. |
| Database permissions | Runtime role has table access and lacks superuser, createdb, createrole, replication, bypassrls, neon_superuser and schema-create privileges. Application authorization still controls which learner row each request may access. |
| Server configuration | Database connection stored in Cloudflare's encrypted **DATABASE_URL** secret; other required configuration saved. No secret value is recorded here. |
| Sign-in infrastructure | Clerk **Hobby** production frontend, accounts and email DNS verified. Its public JWKS returned HTTPS 200; the Clerk UI and ClerkJS public bundles returned 200 after redirects. This proves resource availability, not an end-to-end learner session. |
| Anonymous API | Deployed **/api/progress** returns **401 JSON**, with **private/no-store** caching, when requested anonymously over real TLS using the confirmed Cloudflare IP. |
| Main-domain restriction | Verified on the Pages fallback: safe main-site link and progress export/import explanation, with **no authentication bundles loaded**. Lessons and local progress remain available there. |
| Optional cloud progress | Worker and client **deployed**, canonical-domain configuration **enabled**. Live signed-in save/load/delete, account isolation and stale-revision checks remain **unverified** while local system DNS cannot resolve the main domain. No live saved learner record was created during validation. See [setup notes](deploy/PROGRESS-SYNC.md). |
| Resend and R2 | Intentionally inactive. No separate application-email feature is needed; R2 would introduce unnecessary subscription/overage exposure. |
| Domain renewal | Quoted **US$29.99/year**, separate from hosting. Current expiry **2027-10-20**; auto-renew **off**. This deployment does not promise zero-cost domain renewal. |

## Review and checks

The [learning intent review](teaching/product-intent-review.md) found that the expanded course substantially meets the previous request for in-course explanations, commands, controlled failures, answers, capstones and repository synthesis. This revision adds eleven explicit free local routes and a recurring judgment rubric, and fixes cross-week Kubernetes database selection, migration networking and private-image deployment ordering.

Current content has 52 lessons, 13 capstones and 545 command blocks. The full teaching validator passed with no errors: 542 Bash syntax checks and 40 embedded Python compilation checks. The local application had 38 unit/adapter checks and 10 real HTTP checks pass, with one intentionally skipped stage-03 authentication case. The final embedded lesson payload matched all source lessons.

These checks do not establish real PostgreSQL/container execution, Kubernetes networking, GitLab delivery or AWS/GCP behavior. Those require the documented lab environments and their own evidence. A completed course also does not confer twenty years of operating experience or guarantee a failure-proof service.

## Operating notes

- Keep the course usable when optional cloud save is disabled or unavailable. Local progress and export remain the fallback.
- Export/import progress when changing from a local file, Pages address or custom domain; browser storage is scoped to its origin.
- Review current free-service limits before enabling optional integrations. Do not enable paid upgrades merely to preserve a convenience feature.
- Publish only the reviewed public output. Keep database credentials, authentication secrets, learner evidence and authoring caches out of downloadable artifacts.
- Record broad DNS resolution and end-to-end optional cloud-save validation when completed. Worker publication and anonymous authentication rejection passed; real signed-in save/load/delete, cross-account isolation and stale-revision behavior are not yet recorded as passed.
- Domain auto-renew is off. Retaining the custom domain beyond 20 October 2027 requires a separate renewal decision and its applicable charge; the free Pages address is independent of that renewal.
