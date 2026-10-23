# Dev Opps validation

This report distinguishes the course viewer, authored exercises and actual lab execution. The public packages are static course material; the website does not run commands, authenticate to providers or deploy a service.

## Teaching coverage

The expanded edition retains the 52-week sequence and adds a guided lesson for each week, with concepts, prerequisites, explained commands, expected results, troubleshooting, a controlled fault, diagnosis and recovery answers, independent practice, recall questions, cleanup and primary references. Every fourth week includes a capstone with a brief, acceptance checks, hints, reference approach and evidence rubric.

All 30 findarepo projects and ten DevOps Daily repositories have original teaching synthesis and exercises inside the relevant lessons and catalog entries. The roadmap investigation and source inspection evidence remain included. Source links are attribution and deeper reference after the teaching.

The repeatable `tools/validate_teaching.py` checks the required fields, capstone schedule, repository coverage, encoding, embedded lesson identity and available Bash/Python syntax. Its generated detail is `teaching/validation-structure.json`. These structural checks do not measure teaching effectiveness or prove that commands succeed on every environment.

## Application evidence

The original supplied Taskboard implementation has 38 passing local unit/adapter checks, 10 passing real HTTP checks for the in-memory prototype with one intentional authentication skip, and 11 passing authenticated real HTTP checks using the shared adapter with an explicitly injected memory store. Lint and dependency checks passed. A short bounded load-helper smoke validated its mechanics; it is not the formal five-minute workload or a production performance claim.

Fourteen deployment-helper control-flow/guard tests pass normally and with Python optimization enabled. Those tests replace Docker/HTTP and stub the unavailable Windows fcntl import; they do not prove a Linux deployment. Executed negative-input checks also verify that malformed restore names and UUIDs stop before database operations. See `teaching/validation-taskboard.md` and `teaching/validation-deployment-audit.md` for exact versions, commands, scope and limitations. PostgreSQL integration, Linux container builds, Compose lifecycle/restore, GitLab delivery, Kubernetes and AWS/GCP exercises were not executed in this Windows authoring environment. They remain explicit learner gates requiring their own evidence. No paid resources were created.

## Viewer and interaction checks

The original weeks, repository and learning catalogs, templates and source registry match the pre-teaching backup exactly; new teaching is added alongside them. The original viewer validator checks the 52 weeks, 13 gates, 30+10 catalog identities, five templates, local document links, JavaScript syntax and lack of external runtime dependencies. The expanded browser check exercises the production viewer, including lesson routes, source badges, expandable answers, responsive layouts and preserved progress behavior. The production check passed all 52 routes, 13 capstones and source badges, all 13 journey rows and 65 previews at 1440/390/320-pixel widths, evidence-required progress, save/reload, an actual export/import round trip, search, answer disclosures and print-state restoration. No page exceptions or document-width overflow were observed. See `teaching/validation-browser.md` and `.json` for scope and REA capture limitations.

Printing opens lesson answers for the printed copy and restores their prior on-screen state afterward. Existing local progress keeps its original storage key/schema. Proved still requires an evidence note; export/import remains the backup mechanism.

## Sources and public packages

The availability check records HTTP response status and redirects for the authored primary references in `teaching/validation-source-links.json`. It checks reachability, not factual accuracy. Ansible documentation rate-limited some automated HEAD requests; this is recorded separately from a missing page.

`tools/package_course.py` creates a small lab download, a static hosting archive and a complete editable offline archive. Packages exclude virtual environments, caches, temporary authoring scripts, reports, learner progress exports, credentials and database dumps. ZIP integrity and prohibited-path checks run during packaging. Package checksums are in `PACKAGE-MANIFEST.json` and file checksums in `MANIFEST.sha256`.

The course has not been published to an external hosting account. Upload the contents of the public archive's `site` folder when a destination is selected. The complete course archive contains the editable sources as well as the viewer and labs.
