"""Check authored lesson coverage and syntax. Does not execute lab exercises."""
from pathlib import Path
import collections
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
counts = collections.Counter()
lessons = []

def check(ok, message):
    if not ok:
        errors.append(message)

def walk(value, path):
    if isinstance(value, dict):
        if 'code' in value:
            counts['commandBlocks'] += 1
            for key in ['code', 'explain', 'expected']:
                check(bool(value.get(key)), f'{path}: missing command {key}')
            code = value.get('code', '')
            shell = value.get('shell', 'Bash').lower()
            if bash and 'bash' in shell:
                result = subprocess.run([bash, '-n'], input=code+'\n', text=True, encoding='utf-8', capture_output=True, timeout=15)
                counts['bashSyntaxChecks'] += 1
                check(result.returncode == 0, f'{path}: Bash syntax: {result.stderr.strip()}')
            for match in re.finditer(r"(?:python(?:3)?|\.venv/bin/python)\s+-\s*<<\s*['\"]?(\w+)['\"]?[^\n]*\n([\s\S]*?)\n\1(?:\n|$)", code):
                counts['embeddedPythonChecks'] += 1
                try:
                    compile(match[2], path, 'exec')
                except SyntaxError as exc:
                    errors.append(f'{path}: Python syntax: {exc}')
        for key, child in value.items():
            walk(child, f'{path}.{key}')
    elif isinstance(value, list):
        for i, child in enumerate(value):
            walk(child, f'{path}[{i}]')
    elif isinstance(value, str):
        check(not any(x in value for x in ['\ufffd', '\u00e2\u20ac', '\u00c3\u00a2', '\u00c2', '\u00c3']), f'{path}: damaged UTF-8 text')

bash = shutil.which('bash')
if sys.platform == 'win32':
    candidate = Path(r'C:\Program Files\Git\bin\bash.exe')
    bash = str(candidate) if candidate.exists() else None
for week in range(1, 53):
    path = ROOT / f'teaching/lessons/week-{week:02d}.json'
    if not path.exists():
        errors.append(f'Missing week {week}')
        continue
    lesson = json.loads(path.read_text(encoding='utf-8-sig'))
    lessons.append(lesson)
    check(lesson.get('week') == week, f'{path.name}: wrong week')
    for key in ['introduction', 'prerequisites', 'concepts', 'steps', 'failure', 'exercise', 'questions', 'cleanup', 'references']:
        check(bool(lesson.get(key)), f'{path.name}: missing {key}')
    check(len(lesson.get('concepts', [])) >= 2, f'{path.name}: concepts too few')
    check(len(lesson.get('steps', [])) >= 3, f'{path.name}: steps too few')
    check(len(lesson.get('questions', [])) >= 3, f'{path.name}: recall questions too few')
    check(bool(lesson.get('capstone')) == (week % 4 == 0), f'{path.name}: capstone schedule mismatch')
    for step in lesson.get('steps', []):
        check(bool(step.get('purpose')) and bool(step.get('checkpoint')) and bool(step.get('commands')), f'{path.name}: incomplete build step')
    failure = lesson.get('failure', {})
    for key in ['boundary', 'inject', 'investigate', 'hints', 'answer']:
        check(bool(failure.get(key)), f'{path.name}: missing failure {key}')
    for ref in lesson.get('references', []):
        check(ref.get('url', '').startswith('https://') and ref.get('title') and ref.get('usedFor'), f'{path.name}: malformed reference')
    walk(lesson, path.name)

synthesis = json.loads((ROOT/'teaching/repository-synthesis.json').read_text(encoding='utf-8-sig'))['repositories']
check(len(synthesis) == 40 and len({p['repo'] for p in synthesis}) == 40, 'Need all40 unique repository syntheses')
check(set(w for p in synthesis for w in p['weeks']) == set(range(1,53)), 'Repository mapping must cover52weeks')
page = (ROOT/'index.html').read_text(encoding='utf-8')
payload = json.loads(re.search(r'<script id="fieldbook-data" type="application/json">([\s\S]*?)</script>',page)[1])
check(payload.get('lessons') == {str(p['week']):p for p in lessons}, 'Rebuild index: lesson payload differs from source')
check(payload.get('repoLessons') == synthesis, 'Rebuild index: repository teaching differs from source')
check('watch montage' not in page.lower(), 'Montage watch link still present')
report = {'lessons':len(lessons),'capstones':sum(bool(p.get('capstone')) for p in lessons),'repositorySyntheses':len(synthesis),**dict(counts),'bashAvailable':bool(bash),'errors':errors,'scope':'Coverage, required teaching fields, encoding, embedded payload identity and command syntax only. Does not execute infrastructure or prove teaching outcomes.'}
(ROOT/'teaching/validation-structure.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
sys.exit(bool(errors))
