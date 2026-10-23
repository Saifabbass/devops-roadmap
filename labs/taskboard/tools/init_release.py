"""Create an explicitly incomplete release record; never synthesize a passing report."""
import json
from pathlib import Path
path=Path('reports/release');path.mkdir(parents=True,exist_ok=True)
manifest=path/'release.json'
if manifest.exists(): raise SystemExit('Existing release record preserved; edit/review it deliberately.')
data={'source_commit':'','artifact_kind':'registry-image','image_ref':'','api_contract':'1.0','schema_version':2,
      'checks':{name:{'status':'incomplete','evidence':'','sha256':''}
                for name in ('unit','integration','system','security','restore','cost','rollback')}}
manifest.write_text(json.dumps(data,indent=2),encoding='utf-8')
print('Created reports/release/release.json with every check incomplete.')
