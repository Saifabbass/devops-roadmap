# Browser validation — 20 October 2026

Production preview: http://127.0.0.1:8767. Isolated Edge profile on D:; user browser progress untouched.

Passed: all 52 lesson routes, 13 capstones, 40 repository patterns, command blocks and source badges. Document-width checks passed at 1440, 390 and 320 pixels. All 13 journey rows, 52 week links and 65 previews passed bounds/single-active checks at those widths; no montage links remain.

Passed: empty-evidence Proved guard; save and reload; actual JSON download and restore after changing the record; lesson answer disclosure; beforeprint opens all 31 sampled lesson details and afterprint restores their exact prior state; federation search includes week39. Zero page exceptions were observed by the CDP listener.

REA desktop evidence: ev_ef8d929cf110ceebfc6c0816b803f1aa58fe3642bb4415f9c2ea42196a00819a. REA mobile evidence: ev_55420ee8d5fdb2c3def1181dc9d97a7799d34e025d525d375c4be1f514392190. Attached REA captures include DOM/screenshot evidence but cannot recover pre-attach event history; the JSON report records this limitation.

Viewport screenshots: course-desktop.png and course-mobile.png. Full browser report: validation-browser.json. Lesson syntax report: validation-25-40.json (16 lessons;171 command blocks;170 Bash;12 embedded Python;19 YAML/config;1 HCL;zero errors).

No Docker, Kubernetes, live CI, cloud resource creation, performance, cost or provider reliability result was executed or claimed by these browser/syntax checks.
