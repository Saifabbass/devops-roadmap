# Optional cloud progress for Dev Oops!

The public course works without accounts, a database, email or this function. Browser progress and JSON export/import remain the fallback. As recorded on 21 October 2026, Neon Free schema/runtime permissions, the Cloudflare encrypted database secret and Clerk Hobby production DNS/public signing keys are configured. The complete public upload now includes the worker and client, with main-domain sync configuration enabled. The deployed anonymous API returns private/no-store JSON 401; public identity resources are reachable. **Real signed-in save/load/delete and cross-account checks remain unverified**, because the authoring machine's system DNS does not yet resolve the main domain. The Pages fallback was verified to offer the main-site link and export/import guidance without loading authentication. See [Deployment record](../DEPLOYMENT.md) for the evidence. Setting `PROGRESS_SYNC_ENABLED=false` disables the API while preserving public lessons and local progress.

## Services and spending

Use Cloudflare Pages/Workers **Free**, Neon **Free**, and Clerk **Hobby** only. Cloudflare Pages static requests are free and unlimited. The function shares the Workers Free allowance of 100,000 requests/day; Neon suspends compute at its Free quota. A quota outage may stop cloud save but must not stop learning. Do not enable paid plans or automatic overages.

Resend is deliberately inactive: the course has no necessary application email feature, and Clerk handles the selected authentication flow. R2 is deliberately inactive: it requires a billing subscription and charges above the free allowance. Cloudflare budget alerts do not cap spending. Current course assets fit Pages' 25 MiB individual-file limit. Keeping R2 disabled honors the owner's strict $0 running-cost requirement. Existing domain registration and renewal are separate from hosting.

Official limits checked 2026-10-21:

- [Pages Functions and static requests](https://developers.cloudflare.com/pages/functions/pricing/)
- [Pages file/build limits](https://developers.cloudflare.com/pages/platform/limits/)
- [Neon Free quotas and suspension behavior](https://neon.com/docs/introduction/plans)
- [Clerk Hobby allowance and upgrade threshold](https://clerk.com/pricing)
- [Resend Free and paid overages](https://resend.com/pricing)
- [R2 pricing](https://developers.cloudflare.com/r2/pricing/) and [budget alerts are informational only](https://developers.cloudflare.com/billing/manage/budget-alerts/)

## Setup

1. Keep the course itself a public Pages project. Do not apply Cloudflare Access or a sign-in redirect to course routes. Associate `devoops.tech` through Pages custom domains; the apex requires a Cloudflare DNS zone in the same account and Cloudflare nameservers. See [custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/).
2. Create a Neon Free project. Run `deploy/progress-schema.sql` in its SQL editor. Prefer a dedicated database login with only the grants listed in the schema. Copy that login's connection string into a Cloudflare **encrypted secret** named `DATABASE_URL`. Do not put it in a public JSON file, browser script, repository, ZIP or screenshot.
3. Configure a Clerk production application for `devoops.tech`, complete its required DNS setup, enable personal accounts and only the desired free sign-in methods. The frontend publishable key is public; a Clerk secret key is not needed by this API. The server fetches the public signing keys from the configured Frontend API origin.
4. Set server environment variables using `progress-env.example`. `CLERK_ISSUER` is the exact Frontend API origin including `https://` and **no trailing slash**. `APP_ORIGINS` is a comma-separated exact origin allowlist, normally only `https://devoops.tech`. Do not wildcard `pages.dev` previews. `CLERK_AUDIENCE` is optional; leave it absent for standard Clerk sessions without an `aud` claim. The server always verifies `iss`, `azp`, signature, expiry, not-before, issuance time, session id and user id. It rejects missing `azp` for this browser-only application and pending sessions.
5. From the course source directory (the directory containing `index.html`, `functions` and `package.json`), install the small pinned backend dependency with `npm ci`. `package-lock.json` fixes the Neon driver version. No frontend application build is required for the static course.
6. For an existing dashboard Direct Upload project, build the single advanced-mode worker as described below. Cloudflare explicitly supports `_worker.js` in dashboard uploads even though it does **not compile a `functions` directory**. A Wrangler or Pages Git build is an alternative: run Wrangler with the course source as current directory against a separate curated public-output directory. Example: `npx wrangler pages deploy ../public-output --project-name YOUR_PROJECT`. Keep `functions`, `node_modules`, `.dev.vars`, schema and environment files out of public assets.
7. In the public-output directory, use the contents of `deploy/progress-routes.json` as `_routes.json`. It routes **only `/api/progress`** into the function, leaving all course files on the free static path. Keep Function failure behavior closed for the API: a quota failure must never bypass authentication into a backend.
8. Set `PROGRESS_SYNC_ENABLED=true` on the server only after schema and identity configuration are ready. Set the public `sync-config.json` fields to `{ "enabled": true, "clerkPublishableKey": "YOUR_PUBLIC_KEY", "clerkFrontendApi": "YOUR_FRONTEND_API_HOST" }`. No secret belongs in that file. The frontend should load Clerk only when the learner clicks Save across devices. Test before publishing the enabled config.

The current official [Clerk JavaScript quickstart](https://clerk.com/docs/js-frontend/getting-started/quickstart) uses the Frontend API host to load `/npm/@clerk/ui@1/dist/ui.browser.js`, then `/npm/@clerk/clerk-js@6/dist/clerk.browser.js` with `data-clerk-publishable-key`. Initialize with `Clerk.load({ui:{ClerkUI:window.__internal_ClerkUICtor}})`. Reading must not load these bundles.

## Dashboard deployment with a bundled worker

Cloudflare's [Direct Upload documentation](https://developers.cloudflare.com/pages/get-started/direct-upload/#functions) explicitly supports a `_worker.js` file for dashboard drag-and-drop, including ZIP uploads. [Advanced mode](https://developers.cloudflare.com/pages/functions/advanced-mode/) requires a module-worker default export and forwarding non-API requests to `env.ASSETS.fetch(request)`. `deploy/worker-entry.js` implements that contract and reuses the same verified progress API.

From the course source directory, after `npm ci`:

```text
npm run build:worker
npm run test:worker
```

The build writes **only** `deploy/worker-build/_worker.js`, `deploy/worker-build/_routes.json` and `deploy/worker-build-report.json`. It never reads `.env` files or copies credentials into JavaScript, and it does not modify the public site directory. The report records size, SHA-256 and the absence of external module imports. The pinned esbuild tool is a build dependency, not a hosted service.

After review, copy `_worker.js` and `_routes.json` into the root of a **complete, curated public site** directory beside `index.html`, then ZIP that whole directory's contents for Pages → Create a new deployment. Do not upload only the two worker files: a deployment replaces the site's asset set. Do not add the unbundled `functions` directory, database schema, `node_modules` or environment files to the ZIP. Keep the public account configuration disabled until server secrets/variables have been set and authenticated tests have passed. Set a current compatibility date in Pages Runtime settings; the bundle uses standard Web APIs and does not require `nodejs_compat`.

The supplied `_routes.json` invokes the function only for `/api/progress`, preserving the free static delivery path for course pages. The worker also forwards non-API requests to `ASSETS` if invoked by a future routing change. Dashboard Direct Upload permits 1,000 files and 25 MiB per file; count the full curated asset set before upload. After deployment, verify the unauthenticated API returns JSON 401 when enabled (503 when disabled), never the course's HTML fallback, and recheck that lessons still open anonymously. Bundle tests evaluate the actual output in an isolated Web-API context without Node globals and include a real signed session with a mocked Neon HTTP response; they do not replace deployed integration checks.

## Browser contract

All requests are same-origin and use `Authorization: Bearer <await Clerk.session.getToken()>`. Cookies alone are rejected. Cross-origin CORS is intentionally unavailable.

| Operation | Request | Successful response |
|---|---|---|
| Load | `GET /api/progress` | `{progress, revision, updatedAt}`; no record means `null, 0, null` |
| Save | `PUT /api/progress`, JSON `{progress, expectedRevision}` | `{progress, revision, updatedAt}` |
| Delete cloud copy | `DELETE /api/progress`, JSON `{expectedRevision}` | `{progress:null, revision:0, updatedAt:null}` |

Always load before the first save. Keep the returned revision; it is an opaque positive safe integer, **not necessarily consecutive**. Use zero only to create a record that does not exist. A 409 response means another save changed the cloud copy; preserve local data and ask the learner to load/compare rather than automatically overwriting. After any network error, reload before retrying because the original write may have succeeded. Deleting cloud progress does not delete the Clerk account or local browser data.

Progress matches the course's existing schema: `schemaVersion:1`, date-shaped edition string, and week keys `1` through `52`. Each week contains `status` (`Not started`, `Learning`, `Built`, `Proved`), `note` up to 20,000 characters, and optional `updated` string up to 40 characters. Proved requires a nonblank note. An export's optional `exportedAt` is accepted and discarded. Unknown fields are rejected. The whole request is limited to 2,000,000 UTF-8 bytes, including when no Content-Length header is sent.

401 means sign in again; 403 means origin configuration mismatch; 400/413/415 means invalid data; 409 means revision conflict; 503 means disabled, unconfigured, temporarily unavailable or a provider quota/outage. Every response is marked noncacheable. Provider exceptions, database credentials, tokens and learner notes are not logged or returned as errors.

## Validation and operational limits

Run `node --test --test-isolation=none deploy/progress.test.mjs` from the course source directory, with Node 22 or newer. The tests generate real RSA signatures and check invalid signatures, algorithms, issuer/authorized-party/audience mismatches, expired and pending sessions, origin restrictions, payload limits, schema violations, optimistic concurrency behavior, per-user isolation and provider failure handling. The pinned Neon driver is exercised with an isolated HTTP response to check parameter handling and result decoding. These tests do **not** establish that a live Clerk or Neon account is connected or that the schema has been applied.

Before enabling the public config, use two real test accounts: save as account A, verify B sees no A progress, verify two-tab stale revisions return 409, load after saving, delete only the test cloud record, sign out and verify anonymous API requests fail while all lessons still open. Repeat an API request with a modified/expired token and confirm rejection. Set `PROGRESS_SYNC_ENABLED=false` to test the fallback. Check actual deployed routes and responses; a static host may otherwise return the website HTML for a missing API route.

Revisions use a database sequence to prevent old revisions being accepted after delete/recreate. There is no cross-user endpoint or user id supplied by the browser. Authorization is enforced by the server function; the database login can access the whole progress table and must remain secret. Do not expose that table directly through a public Data API. Learner evidence is private account data: ask learners not to save credentials or sensitive production logs, and retain export/delete controls.

Session verification follows [Clerk's manual JWT guide](https://clerk.com/docs/guides/sessions/manual-jwt-verification). Neon calls use the pinned official [HTTP serverless driver](https://neon.com/docs/serverless/serverless-driver), parameterized SQL, and an eight-second timeout. Signing-key fetches have a five-second timeout and bounded cache. Like ordinary stateless JWT validation, a signed session token remains valid until its short expiry; revocation is not checked online on every save. Free service allowances can change, and cloud sync availability is bounded by them; the public static course and local export are the durable fallback.
