"""Bounded local-only sample. Defaults match the course workload; no SLO claim."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import statistics
import threading
import time
from urllib.parse import urlparse
import httpx

parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://127.0.0.1:8000')
parser.add_argument('--warmup', type=int, default=60)
parser.add_argument('--seconds', type=int, default=300)
parser.add_argument('--clients', type=int, default=10)
parser.add_argument('--tasks', type=int, default=1000)
parser.add_argument('--output', default='reports/load.json')
a = parser.parse_args()
if urlparse(a.url).hostname not in {'127.0.0.1', 'localhost', 'app'}:
    parser.error('Only the disposable local lab is allowed')
if not (0 <= a.warmup <= 300 and 1 <= a.seconds <= 600 and 1 <= a.clients <= 20 and 1 <= a.tasks <= 1000):
    parser.error('Bounds: warmup0–300s, measurement1–600s, clients1–20, tasks1–1000')
token = os.environ.get('LAB_ALICE_TOKEN')
if not token:
    parser.error('Export the local LAB_ALICE_TOKEN first; never put it on the command line')
headers = {'Authorization': 'Bearer ' + token}
with httpx.Client(base_url=a.url, headers=headers, timeout=5) as client:
    response = client.get('/tasks'); response.raise_for_status()
    tasks = response.json()['items']
    if len(tasks) > 1000:
        parser.error('Existing dataset exceeds the course limit; use a fresh disposable database')
    while len(tasks) < a.tasks:
        response = client.post('/tasks', json={'title': f'Load sample {len(tasks):04}'})
        response.raise_for_status(); tasks.append(response.json())
    tasks = tasks[:a.tasks]
ids = [t['id'] for t in tasks]
completed = {t['id'] for t in tasks if t['completed']}
lock = threading.Lock()

def phase(seconds):
    deadline = time.monotonic() + seconds
    latencies, errors, changed, repeated, reads = [], 0, 0, 0, 0
    def worker(seed):
        nonlocal errors, changed, repeated, reads
        rng = random.Random(seed)
        with httpx.Client(base_url=a.url, headers=headers, timeout=5) as client:
            while time.monotonic() < deadline:
                task_id = rng.choice(ids)
                completion = rng.random() < 0.1
                started = time.monotonic()
                try:
                    response = client.post(f'/tasks/{task_id}/complete') if completion else client.get(f'/tasks/{task_id}')
                    response.raise_for_status()
                    body = response.json()
                    assert body['id'] == task_id
                    if completion:
                        assert body['completed'] is True and body['completed_at']
                    with lock:
                        if completion:
                            if task_id in completed:
                                repeated += 1
                            else:
                                completed.add(task_id); changed += 1
                        else:
                            reads += 1
                except (httpx.HTTPError, ValueError, KeyError, AssertionError):
                    with lock:
                        errors += 1
                finally:
                    with lock:
                        latencies.append((time.monotonic() - started) * 1000)
    with ThreadPoolExecutor(max_workers=a.clients) as pool:
        list(pool.map(worker, range(a.clients)))
    ordered = sorted(latencies)
    def percentile(p):
        return round(ordered[min(len(ordered)-1, int((len(ordered)-1)*p))], 2) if ordered else None
    return dict(requests=len(ordered), errors=errors, successful_reads=reads,
                completions_changed=changed, completions_repeated=repeated,
                p50_ms=percentile(.5), p95_ms=percentile(.95), p99_ms=percentile(.99))

warmup = phase(a.warmup) if a.warmup else {}
started_at = datetime.now(timezone.utc).isoformat()
started = time.monotonic()
measurement = phase(a.seconds)
measurement['elapsed_seconds'] = round(time.monotonic()-started, 2)
measurement['requests_per_second'] = round(measurement['requests']/measurement['elapsed_seconds'], 2)
report = dict(started_at=started_at, clients=a.clients, tasks=len(ids), intended_read_ratio=.9,
              warmup=warmup, measured=measurement, note='Closed-loop local sample; no monthly SLO or open-loop capacity proof.')
path = Path(a.output); path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
