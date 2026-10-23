"""Small, explainable onboarding checks; names and actions, never secret values."""
import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys
parser=argparse.ArgumentParser()
parser.add_argument('--stage',choices=['03','06','07'],default='03')
parser.add_argument('--env-file',default='.env')
a=parser.parse_args()
errors=[]
if sys.version_info<(3,12): errors.append('Use Python 3.12+ and recreate the project .venv.')
for package in ('fastapi','uvicorn','psycopg','pytest','httpx'):
    try: print(package,version(package))
    except PackageNotFoundError: errors.append(f'{package}: install requirements-dev.lock in this .venv.')
if a.stage!='03':
    path=Path(a.env_file)
    if not path.is_file(): errors.append('Missing lab environment file: run python tools/init_lab.py once.')
    else:
        values=dict(line.split('=',1) for line in path.read_text().splitlines() if line and not line.startswith('#') and '=' in line)
        if not values.get('POSTGRES_PASSWORD'): errors.append('POSTGRES_PASSWORD is missing; restore your existing private lab configuration.')
        if a.stage=='07':
            for name in ('LAB_ALICE_TOKEN','LAB_BOB_TOKEN'):
                if len(values.get(name,''))<32: errors.append(name+': requires a generated token of at least 32 characters.')
            if values.get('LAB_ALICE_TOKEN')==values.get('LAB_BOB_TOKEN'): errors.append('Alice and Bob tokens must differ.')
if errors:
    for error in errors: print('ACTION:',error,file=sys.stderr)
    raise SystemExit(1)
print('Preflight passed. This checks configuration presence, not DB/network availability.')
