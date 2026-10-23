"""An evidence completeness gate, not proof that a report or signer is trustworthy."""
import argparse,hashlib,json,re
from pathlib import Path
import xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('manifest');a=p.parse_args()
path=Path(a.manifest).resolve();data=json.loads(path.read_text());errors=[]
if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}',data.get('source_commit','')): errors.append('Record an actual source commit.')
pattern = r'sha256:[0-9a-f]{64}' if data.get('artifact_kind') == 'local-image' else r'.+@sha256:[0-9a-f]{64}'
if not re.fullmatch(pattern,data.get('image_ref','')): errors.append('Record the tested immutable image identity and its artifact kind.')
if data.get('api_contract')!='1.0' or data.get('schema_version')!=2: errors.append('Review contract/schema compatibility (reference baseline: API1.0/schema2).')
for name in ('unit','integration','system','security','restore','cost','rollback'):
    item=data.get('checks',{}).get(name,{})
    if item.get('status')!='passed': errors.append(name+': not passed')
    relative=item.get('evidence','')
    file=(path.parent/relative).resolve()
    if not relative or not file.is_relative_to(path.parent) or not file.is_file():
        errors.append(name+': missing evidence inside release folder');continue
    if hashlib.sha256(file.read_bytes()).hexdigest()!=item.get('sha256'): errors.append(name+': evidence checksum mismatch')
    if name in ('unit','integration','system'):
        try:
            root=ET.parse(file).getroot();cases=list(root.iter('testcase'))
            if not cases or any(list(case.iter('failure')) or list(case.iter('error')) or list(case.iter('skipped')) for case in cases):
                errors.append(name+': tests absent, failed, errored or skipped')
        except ET.ParseError: errors.append(name+': not a JUnit report')
if errors:
    print('\n'.join('BLOCK: '+error for error in errors));raise SystemExit(1)
print('Evidence completeness gate passed. Review authenticity, scope and approval independently before deployment.')
