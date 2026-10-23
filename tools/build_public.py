"""Produce an allowlisted Cloudflare Pages upload, never the entire workspace."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'public'
DEST.mkdir(exist_ok=True)
files = [ROOT / name for name in ['index.html', '_headers', 'robots.txt', 'sitemap.xml', 'sync-config.json', 'progress-template.csv']]
for folder, suffixes in [('assets', {'.css', '.svg', '.png', '.webp', '.jpg', '.mp4', '.woff2', '.json', '.txt'}), ('handbook', {'.md'}), ('templates', {'.md'}), ('research', {'.md'}), ('downloads', {'.zip'})]:
    files.extend(p for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix in suffixes)
uploads = [(p, p.relative_to(ROOT)) for p in files]
worker_dir = ROOT / 'deploy' / 'worker-build'
worker_names = ('_worker.js', '_routes.json')
worker_present = [(worker_dir / name).is_file() for name in worker_names]
assert all(worker_present) or not any(worker_present), 'Worker and routes must be built together before publication'
worker_included = all(worker_present)
if worker_included:
    routes = json.loads((worker_dir / '_routes.json').read_text(encoding='utf-8'))
    assert routes == {'version': 1, 'include': ['/api/progress'], 'exclude': []}, 'Only the progress API may invoke the worker'
    uploads.extend((worker_dir / name, Path(name)) for name in worker_names)
assert len(uploads) <= 1000, 'Cloudflare dashboard uploads allow at most 1,000 files'
for src, relative_path in uploads:
    assert src.stat().st_size < 25 * 1024 * 1024, src
    target = DEST / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, target)
expected = {relative_path.as_posix() for _, relative_path in uploads}
actual = {p.relative_to(DEST).as_posix() for p in DEST.rglob('*') if p.is_file()}
assert actual == expected, 'Unexpected files in public; review rather than publish them'
archive = ROOT / 'Dev-Oops-Pages.zip'
with ZipFile(archive, 'w', ZIP_DEFLATED, compresslevel=6) as z:
    for src, relative_path in sorted(uploads, key=lambda item: item[1].as_posix()):
        z.write(src, relative_path.as_posix())
with ZipFile(archive) as z:
    assert z.testzip() is None
report = {'files': len(uploads), 'bytes': sum(src.stat().st_size for src, _ in uploads), 'archive': str(archive), 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'cloudSyncEnabled': json.loads((ROOT/'sync-config.json').read_text())['enabled'], 'workerIncluded': worker_included}
(ROOT/'research/public-build.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
