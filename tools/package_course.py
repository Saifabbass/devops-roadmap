"""Create clean downloadable labs, static site and editable offline source archives."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={'.venv','.tmp','.pytest_cache','__pycache__','.git','.ruff_cache','reports','node_modules','browser-profile','qa-profile','validation-lib','validation-tmp','qa-edge','qa-edge-cache','browser-qa'}
FORBIDDEN={'.env','private.env','credentials','id_rsa','id_ed25519'}

def collect(folder, suffixes=None):
    result=[]
    for p in (ROOT/folder).rglob('*'):
        rel=p.relative_to(ROOT)
        if not p.is_file() or any(part in EXCLUDE or part.startswith('pytest-cache-files-') for part in rel.parts):
            continue
        if p.name in FORBIDDEN or (p.name.startswith('.env.') and p.name != '.env.example') or p.name.endswith('.sql.gz') or p.suffix in {'.pyc','.dump','.sql.gz','.log','.pem','.key'}:
            continue
        if suffixes is not None and p.suffix not in suffixes:
            continue
        result.append(p)
    return result

def archive(target, paths, prefix=''):
    with ZipFile(target,'w',ZIP_DEFLATED,compresslevel=7) as z:
        for p in sorted(set(paths)):
            z.write(p, prefix+p.relative_to(ROOT).as_posix())
    with ZipFile(target) as z:
        assert z.testzip() is None
        assert not any(any(part in EXCLUDE or part in FORBIDDEN for part in Path(n).parts) for n in z.namelist())
    return {'file':target.name,'files':len(set(paths)),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}

(ROOT/'downloads').mkdir(exist_ok=True)
labs=collect('labs')
lab_archive=ROOT/'downloads/dev-opps-labs.zip'
reports=[archive(lab_archive,labs)]
site=[ROOT/'index.html',ROOT/'README.md',ROOT/'CONTENTS.md',ROOT/'VALIDATION.md',ROOT/'REDESIGN.md',ROOT/'DEPLOYMENT.md',ROOT/'teaching/product-intent-review.md',ROOT/'deploy/PROGRESS-SYNC.md',lab_archive]
site+=collect('assets')+collect('handbook',{'.md'})+collect('templates',{'.md'})+collect('research',{'.md'})
site+=[p for p in (ROOT/'teaching').glob('validation*.md')]+[p for p in (ROOT/'teaching').glob('validation*.json')]+[ROOT/'teaching/requirements-audit.md',ROOT/'teaching/course-desktop.png',ROOT/'teaching/course-mobile.png']
site += [ROOT/'progress-template.csv',ROOT/'sync-config.json',ROOT/'_headers',ROOT/'robots.txt',ROOT/'sitemap.xml']
reports.append(archive(ROOT/'Dev-Opps-Public-Site.zip',site,'site/'))
source=site+labs+[ROOT/'curriculum.json',ROOT/'sources.json',ROOT/'progress-template.csv']
source+=[p for p in (ROOT/'teaching').iterdir() if p.is_file() and (p.suffix=='.json' or p.name in {'lesson-view.js','lesson-view.css','progress-sync.js','CONTENT-CONTRACT.md','product-intent-review.md'})]+collect('teaching/lessons',{'.json'})+collect('tools',{'.py','.html'})
source+=collect('redesign-source',{'.js','.css'})+[ROOT/'redesign-source/prepare_redesign.py']+collect('research',{'.json'})
source=[p for p in source if p.name!='ui-progress-export.json']
source += collect('functions',{'.js','.mjs'}) + collect('deploy',{'.md','.json','.sql','.mjs','.js'})
source += [ROOT/name for name in ['package.json','package-lock.json','deploy/progress-env.example'] if (ROOT/name).exists()]
all_files=sorted(set(source))
(ROOT/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in all_files),encoding='utf-8')
source.append(ROOT/'MANIFEST.sha256')
reports.append(archive(ROOT/'Dev-Opps-Complete-Course.zip',source,'Dev-Opps/'))
(ROOT/'PACKAGE-MANIFEST.json').write_text(json.dumps(reports,indent=2)+'\n',encoding='utf-8')
print(json.dumps(reports))
