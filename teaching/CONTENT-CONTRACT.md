# Teaching content contract

The current objective is in C:/Users/abbas/.codex/attachments/b086590f-cf2f-495f-9fa3-397fafbadd24/goal-objective.md. Latest steering: no Imagegen; preserve the current look. Canonical project is D:/DevOps-Engineering-Fieldbook-2026-10-20. C is full. Author only your assigned files here.

Each lessons/week-NN.json is one fully authored learning block, not a generated template with substituted tool names. Retain the original week/phase/title/outcome sequencing. Explain terminology before requiring it. The website must contain the knowledge needed to do the core exercise; references support and extend it. Do not copy third-party tutorials or imply unexecuted cloud labs were tested.

## JSON shape

- week: integer 1..52
- introduction: 2–4 paragraphs in a string array: concrete situation, why it matters, what the learner will be able to explain, bounded lab vs production distinction.
- prerequisites: string array of exact prior capabilities, required tools and setup. Link local course routes as plain explanatory text only if useful; no undefined project path. Default shell Ubuntu 24.04 LTS Bash (WSL2 or disposable VM). Windows setup is a separate in-course guide.
- concepts: array of {title, paragraphs:[...], example, judgment}. Teach mechanics, a concrete example, and operational tradeoff/misconception. At least 2 substantive concepts per normal lesson.
- steps: ordered array of {title, purpose, commands:[command], checkpoint}. Each step should be a sensible chunk, not a command dump. Provide every required configuration/file, or point to an included local lab file and explain its contents.
- command: {code, explain:[...], expected, troubleshoot, shell?}. code must be executable Bash or clearly shell:"configuration" for a file example. Explain EVERY shell command and important flag/pipeline/redirection. Name the working directory and keep state obvious. Expected output must be specific; mark variable fields. troubleshooting describes the next observation, not simply retry. No unexplained placeholders; define environment variables before use. Use scoped, disposable lab paths/resources and include cleanup for anything created. Cloud commands must start with account/project/region verification and teach costs before creation. Never execute cloud creates while authoring.
- failure: {title, boundary, inject:[command], investigate:[command], hints:[...], answer:{explanation:[...], recover:[command], verification:command}}. One real bounded fault, observable symptoms, expandable hints and solution. The learner writes/understands recovery first. Do not sabotage a host, global DNS, existing accounts, or production resources.
- questions: array of {prompt, hint, answer}. Include at least 3 questions using the exact mechanics just taught. Answers explain reasoning and alternate evidence, not a keyword.
- exercise: {brief, constraints:[...], deliverables:[...], acceptance:[...], hints:[...], solution:[...]}. A small independent practice task each week, with a hidden reference approach.
- capstone: required in weeks4/8/.../52. {title, scenario, startingPoint, requirements:[...], acceptance:[...], runbook:[command], hints:[...], solution:[...], rubric:[{criterion, evidence, pass}], stretch:[...]}. A level-specific integration project with an independently measurable pass condition. Do not merely rename the weekly break drill. Teach then ask for independent application; don't require tools introduced later. Gate52 is cumulative production-readiness review, no claim of bulletproof reliability.
- cleanup: array of command objects, or a clear text command expected preserving deliberate assets for next week; avoid destructive broad patterns.
- references: array of {title,url,usedFor}. Primary docs + specific repo pages, verified current during authoring for version-sensitive claims. References render at END of lesson. Do not require following them to learn the core material.
- repoConnections: array of {repo,principle,application,url}. Integrate specific relevant insights from teaching/repository-synthesis.json within lesson prose/exercises; one sentence/link per repo is insufficient.
- notes: optional array of teaching/verification limitations (not generic warnings).

## Common lab conventions

Beginner workspace: ~/dev-opps-lab with notes/, app/, tests/, evidence/. First two weeks use a local Python standard-library HTTP server under a designated subfolder. Later Taskboard reference assets ship in labs/taskboard with staged implementations; coordinate exact paths with taskboard_labs agent before authoring dependent commands. Do not assume the static course's folder is the learner's Git worktree.

Costly/provider labs always have a local or design-only preparation route with a stated narrower proof, plus the real provider procedure. Do not quietly substitute a local simulation for the advertised cloud capability. Separate setup, execution, and teardown. Explain credentials, identity, network exposure, data persistence and recovery at the moment they matter.

No image generation. Keep the current design. Author original explanatory prose. Record command validation honestly in teaching/validation-notes.md; unexecuted provider labs need syntax/doc checks and explicit status. Do not fabricate credentials, account IDs, image digests, GitHub star counts, or test results.
