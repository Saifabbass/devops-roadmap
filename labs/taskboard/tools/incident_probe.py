"""Diagnose a local client configuration without printing token values."""
import argparse,json
from pathlib import Path
from urllib.parse import urlparse
import httpx
p=argparse.ArgumentParser();p.add_argument('config');a=p.parse_args()
v=json.loads(Path(a.config).read_text())
url=v['base_url']
if urlparse(url).hostname not in {'127.0.0.1','localhost'}: raise SystemExit('Only local disposable endpoints allowed')
with httpx.Client(base_url=url,timeout=3) as client:
    for path,headers in [('/livez',{}),('/readyz',{}),('/tasks',{'Authorization':'Bearer '+v['token']})]:
        try:
            r=client.get(path,headers=headers)
            print(path,'HTTP',r.status_code,'request_id',r.headers.get('x-request-id','none'))
        except httpx.RequestError as e: print(path,type(e).__name__)
