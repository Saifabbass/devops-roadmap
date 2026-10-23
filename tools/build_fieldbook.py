"""Build the offline fieldbook using only the Python standard library."""
from pathlib import Path
import csv
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ("free-learning", "Learn without a cloud bill", "handbook/free-learning.md"),
    ("senior-practice", "Build engineering judgment", "handbook/senior-practice.md"),
    ("lab-setup", "Set up your learning lab", "handbook/lab-setup.md"),
    ("start-here", "Start here", "handbook/start-here.md"),
    ("first-two-weeks", "First two weeks · daily sessions", "handbook/first-two-weeks.md"),
    ("project-spec", "Taskboard project specification", "handbook/project-spec.md"),
    ("engineering-handbook", "Engineering concepts", "handbook/engineering-handbook.md"),
    ("assessment-and-operations", "Assessment and operations", "handbook/assessment-and-operations.md"),
    ("resource-strategy", "How to use the learning sources", "handbook/resource-strategy.md"),
    ("glossary", "Glossary", "handbook/glossary.md"),
    ("roadmap-analysis", "Roadmap investigation", "research/roadmap-analysis.md"),
    ("repos-01-15", "Repository audit · 1–15", "research/repos-01-15.md"),
    ("repos-16-30", "Repository audit · 16–30", "research/repos-16-30.md"),
]
DOC_MAP = {str((ROOT / p).resolve()): slug for slug, _, p in DOCS}


def inline(text, source):
    tokens = []

    def stash(value):
        tokens.append(value)
        return f"\x00{len(tokens)-1}\x00"

    text = re.sub(r"`([^`]+)`", lambda m: stash("<code>" + html.escape(m[1]) + "</code>"), text)

    def link(m):
        target = m[2].strip("<>")
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) and not target.startswith("#"):
            part, _, fragment = target.partition("#")
            resolved = (source.parent / part).resolve()
            if str(resolved) in DOC_MAP:
                target = "#read-" + DOC_MAP[str(resolved)]
            else:
                try:
                    target = resolved.relative_to(ROOT).as_posix() + (("#" + fragment) if fragment else "")
                except ValueError:
                    pass
        if target.lower().startswith(("javascript:", "data:", "vbscript:")):
            return html.escape(m[1])
        attrs = ' target="_blank" rel="noopener noreferrer"' if target.startswith("https://") else ""
        return stash(f'<a href="{html.escape(target, quote=True)}"{attrs}>{html.escape(m[1])}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m[1])], text)


def markdown(text, source):
    """Render the small, explicit Markdown subset used by these local documents."""
    lines = text.splitlines()
    output, para = [], []
    list_type = None

    def flush():
        if para:
            output.append("<p>" + inline(" ".join(para), source) + "</p>")
            para.clear()

    def close_list():
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            close_list()
            lang = line[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            if lang == "mermaid" and any("sequenceDiagram" in b for b in block):
                output.append('<div class="flow" aria-label="Request path"><span>Client</span><b>→</b><span>HTTPS endpoint</span><b>→</b><span>Taskboard API</span><b>→</b><span>PostgreSQL</span></div><p class="caption">The API validates identity, ownership and input before committing a transaction. The result returns through the same path.</p>')
            else:
                label = f'<span class="code-label">{html.escape(lang or "example")}</span>'
                output.append(label + "<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
        elif re.match(r"^#{1,6} ", line):
            flush()
            close_list()
            level = len(line.split(" ", 1)[0])
            output.append(f"<h{level}>" + inline(line[level+1:], source) + f"</h{level}>")
        elif line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|\-]+\|$", lines[i+1]):
            flush()
            close_list()
            headers = line.strip().strip("|").split("|")
            output.append('<div class="table-wrap"><table><thead><tr>' + "".join("<th>" + inline(c.strip(), source) + "</th>" for c in headers) + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                cells = lines[i].strip().strip("|").split("|")
                output.append("<tr>" + "".join("<td>" + inline(c.strip(), source) + "</td>" for c in cells) + "</tr>")
                i += 1
            output.append("</tbody></table></div>")
            continue
        elif re.match(r"^\s*(?:[-*] |\d+\. )", line):
            flush()
            kind = "ol" if re.match(r"^\s*\d+\.", line) else "ul"
            if list_type != kind:
                close_list()
                output.append(f"<{kind}>")
                list_type = kind
            item = re.sub(r"^\s*(?:[-*] |\d+\. )", "", line)
            output.append("<li>" + inline(item, source) + "</li>")
        elif not line.strip():
            flush()
            close_list()
        elif line.startswith("> "):
            flush()
            close_list()
            output.append("<blockquote>" + inline(line[2:], source) + "</blockquote>")
        elif re.match(r"^-{3,}$", line):
            flush()
            close_list()
            output.append("<hr>")
        else:
            close_list()
            para.append(line.strip())
        i += 1
    flush()
    close_list()
    return "\n".join(output)


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def build():
    curriculum = read_json("curriculum.json")
    sources = read_json("sources.json")
    repos = read_json("research/repos-01-15.json") + read_json("research/repos-16-30.json")
    learning = read_json("research/learning-repos.json")["repositories"]
    assert [w["week"] for w in curriculum["weeks"]] == list(range(1, 53))
    assert len({r["repo"] for r in repos}) == 30
    assert len({r["repo"] for r in learning}) == 10
    for w in curriculum["weeks"]:
        assert all(k in w for k in ("outcome", "concept", "build", "break", "prove", "deliverable", "question", "cost"))
        assert all(k in sources for k in w["read"]), w["week"]

    docs = []
    for slug, title, path in DOCS:
        source = ROOT / path
        text = source.read_text(encoding="utf-8-sig")
        docs.append({"id": slug, "title": title, "path": path, "html": markdown(text, source), "text": text})
    templates = []
    for source in sorted((ROOT / "templates").glob("*.md")):
        text = source.read_text(encoding="utf-8-sig")
        templates.append({"id": source.stem, "title": source.stem.replace("-", " ").title(), "path": source.relative_to(ROOT).as_posix(), "text": text, "html": markdown(text, source)})

    plan = [
        "# 52-week DevOps study plan",
        "",
        "Edition 2026-10-20 · Beginner to operational practice · two hours/day · 728 scheduled hours.",
        "",
        "Read [Start here](start-here.md) first. Weeks are relative learning units; repeat a gate when evidence is insufficient. Core readings are linked below. Read only the relevant sections in each week's Focus.",
        "",
        "Each week: day 1 understand; days 2–3 build; day 4 verify; day 5 inject a controlled failure; day 6 reproduce; day 7 review and catch up. Optional repository exercises replace a related lab, never automatically add to the 14-hour budget.",
    ]
    for w in curriculum["weeks"]:
        plan += ["", f"## Week {w['week']}: {w['title']}", "", f"**Phase:** {w['phase']} · **Execution:** {w['cost']}", "", w["outcome"], "", f"**Concept:** {w['concept']}", "", f"**Focus:** {w['focus']}", "", "**Read:** " + " · ".join(f"[{sources[s][0]}]({sources[s][1]})" for s in w["read"]), "", "### Build", ""]
        plan += [f"{i+1}. {t}" for i, t in enumerate(w["build"])]
        plan += ["", "**Controlled failure:** " + w["break"], "", "### Prove before advancing", ""]
        plan += ["- " + p for p in w["prove"]]
        plan += ["", "**Deliverable:** " + w["deliverable"], "", "**Mentor question:** " + w["question"]]
    (ROOT / "handbook/52-week-plan.md").write_text("\n".join(plan) + "\n", encoding="utf-8")

    with (ROOT / "progress-template.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Week", "Phase", "Title", "Status", "Evidence", "Review date"])
        for w in curriculum["weeks"]:
            writer.writerow([w["week"], w["phase"], w["title"], "Not started", "", ""])

    lessons = {str(item["week"]): item for item in (read_json(p.relative_to(ROOT)) for p in sorted((ROOT / "teaching/lessons").glob("week-*.json")))}
    payload = {"repoLessons": read_json("teaching/repository-synthesis.json")["repositories"], "lessons": lessons, **curriculum, "sources": sources, "repos": repos, "learning": learning, "docs": docs, "templates": templates}
    encoded = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = (ROOT / "tools/fieldbook.template.html").read_text(encoding="utf-8")
    def joined(directory, names):
        return "\n".join((ROOT / directory / name).read_text(encoding="utf-8-sig") for name in names if (ROOT / directory / name).exists())
    redesign_css = (ROOT / "assets/reference-variables.css").read_text(encoding="utf-8-sig") + "\n" + joined("redesign-source", ["shell.css", "map.css", "journey.css", "badges.css"])
    replacements = {
        "__REDESIGN_CSS__": redesign_css,
        "__REDESIGN_JS__": joined("redesign-source", ["map.js", "journey.js", "badges.js", "home.js"]),
        "__TEACHING_CSS__": joined("teaching", ["lesson-view.css"]),
        "__TEACHING_JS__": joined("teaching", ["lesson-view.js"]),
        "__SYNC_JS__": joined("teaching", ["progress-sync.js"]),
    }
    for marker, replacement in replacements.items():
        assert template.count(marker) == 1, marker
        template = template.replace(marker, replacement)
    assert template.count("__PAYLOAD__") == 1
    (ROOT / "index.html").write_text(template.replace("__PAYLOAD__", encoded), encoding="utf-8")
    print(json.dumps({"weeks": len(curriculum["weeks"]), "guided_lessons": len(lessons), "repos": len(repos), "learning_repos": len(learning), "documents": len(docs), "templates": len(templates), "sources": len(sources), "output": str(ROOT / "index.html")}))


if __name__ == "__main__":
    build()
