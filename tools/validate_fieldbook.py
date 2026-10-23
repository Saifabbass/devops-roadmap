"""Static coverage and local-link checks; does not execute learning assignments."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src") and value:
                self.links.append(value)


page = (ROOT / "index.html").read_text(encoding="utf-8")
data_text = re.search(r'<script id="fieldbook-data" type="application/json">([\s\S]*?)</script>', page)[1]
data = json.loads(data_text)
assert len(data["weeks"]) == 52
assert [w["week"] for w in data["weeks"]] == list(range(1, 53))
assert len({r["repo"] for r in data["repos"]}) == 30
assert sorted(r["rank"] for r in data["repos"]) == list(range(1, 31))
assert len({r["repo"] for r in data["learning"]}) == 10
assert len([w for w in data["weeks"] if w["title"].startswith("Gate ")]) == 13
assert len(data["templates"]) == 5
assert all(len(w["build"]) >= 2 and len(w["prove"]) >= 3 for w in data["weeks"])
assert all(s in data["sources"] for w in data["weeks"] for s in w["read"])
assert not re.search(r'<script[^>]+src="https?://', page)
assert not re.search(r'<link[^>]+rel="stylesheet"[^>]+href="https?://', page)

broken = []
for doc in data["docs"] + data["templates"]:
    parser = Links()
    parser.feed(doc["html"])
    for href in parser.links:
        if href.startswith(("#", "http:", "https:", "mailto:")):
            continue
        path = unquote(href.split("#")[0])
        if re.match(r"^[A-Za-z]:[\\/]", path) or Path(path).is_absolute() or not (ROOT / path).exists():
            broken.append({"document": doc["title"], "link": href})
assert not broken, broken

script = re.findall(r"<script(?: [^>]*)?>([\s\S]*?)</script>", page)[-1]
result = subprocess.run(["node", "--check"], input=script, text=True, encoding="utf-8", capture_output=True, timeout=15)
assert result.returncode == 0, result.stderr

report = {
    "checked": "2026-10-21",
    "weeks": 52,
    "assessmentGates": 13,
    "findarepoRepositories": 30,
    "learningRepositories": 10,
    "handbookAndResearchChapters": len(data["docs"]),
    "templates": len(data["templates"]),
    "primaryReferenceLinks": len(data["sources"]),
    "localDocumentLinks": "passed",
    "javascriptSyntax": "passed",
    "externalRuntimeDependencies": 0,
    "labExecution": "Viewer validation does not execute labs. See teaching/validation-taskboard.md for local application evidence and infrastructure limits."
}
(ROOT / "research/static-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report))
