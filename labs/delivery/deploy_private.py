"""Private single-host teaching deployment. Linux, stdlib, Docker Compose v2.

Only the bundled private Compose layout is supported. Schema compatibility still
requires human review: image rollback cannot reverse incompatible migrations.
"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from uuid import uuid4


def read_json(path, default=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def save_text(path, value):
    pending = path.with_suffix(path.suffix + '.pending')
    pending.write_text(value, encoding='utf-8')
    os.replace(pending, path)


def save_json(path, value):
    save_text(path, json.dumps(value, indent=2) + '\n')


def require(condition, message):
    # Operational checks must also run with python -O; do not use assert here.
    if not condition:
        raise ValueError(message)


def check_identity(pipeline_id, image, registry):
    require(type(pipeline_id) is int and pipeline_id > 0,
            'A positive real GitLab pipeline ID is required')
    require(bool(registry) and bool(re.fullmatch(re.escape(registry) + r'@sha256:[0-9a-f]{64}', image)),
            'Image must be this project registry followed by an exact sha256 digest')


def check_candidate(pipeline_id, image, registry, watermark):
    check_identity(pipeline_id, image, registry)
    if watermark:
        require(pipeline_id >= watermark['pipeline_id'],
                'Rejected stale pipeline: a newer pipeline was already approved')
        require(pipeline_id != watermark['pipeline_id'] or image == watermark['image'],
                'Same pipeline cannot substitute another image')


def recovery_release(good, previous, attempt, recovery=None):
    # A deploy may have replaced app before failing, or been killed before it
    # could record failure. In both cases good is the recovery destination.
    # A failed/interrupted rollback retries its already-recorded destination.
    if attempt and attempt.get('mode') == 'rollback':
        # Retain the actual recovery destination through repeated failures or
        # process termination. Repeated successful rollback is also idempotent.
        release = good if attempt.get('status') == 'passed' else recovery
    elif attempt and attempt.get('status') in {'running', 'failed'}:
        release = good
    else:
        release = previous
    require(bool(release), 'No recorded compatible known-good release is available')
    return release


def validate_compose(config, image):
    services = config.get('services', {})
    for name in ('app', 'migrate'):
        require(services.get(name, {}).get('image') == image,
                'Both app and migrate must select the exact tested image')
        require(not services[name].get('volumes'), 'Runtime source mounts are not supported')
        require(not services[name].get('privileged'), 'Privileged application services are not supported')
    app, db = services['app'], services.get('db', {})
    ports = app.get('ports', [])
    require(len(ports) == 1 and isinstance(ports[0], dict), 'Exactly one private app publication is required')
    port = ports[0]
    require(port.get('host_ip') == '127.0.0.1' and str(port.get('published')) == '8000'
            and str(port.get('target')) == '8000' and port.get('protocol', 'tcp') == 'tcp',
            'App must publish only 127.0.0.1:8000 to container TCP 8000')
    require(not db.get('ports'), 'The database must not publish host ports')
    require('reference.stage07:app' in app.get('command', []), 'Private staging requires the two-user stage07')
    require(services['migrate'].get('command') == ['python', '-m', 'reference.migrate'],
            'Use the explicit bundled migration entrypoint')
    require(config.get('networks', {}).get('backend', {}).get('internal') is True,
            'The backend network must remain internal')
    for name in ('app', 'migrate', 'db'):
        service = services.get(name, {})
        require(set(service.get('networks', {})) == {'backend'} and not service.get('network_mode'),
                'Runtime services must use only the private backend network')
    volumes = db.get('volumes', [])
    require(len(volumes) == 1 and volumes[0].get('type') == 'volume'
            and volumes[0].get('source') == 'taskboard-data'
            and volumes[0].get('target') == '/var/lib/postgresql/data',
            'Keep the dedicated database volume and mount unchanged')
    volume = config.get('volumes', {}).get('taskboard-data', {})
    require(volume.get('name') == 'devopps-staging_taskboard-data' and not volume.get('external'),
            'Only this staging project database volume is supported')
    # Do not leave an implicit build path in the effective deployment model.
    for service in services.values():
        service.pop('build', None)
        service.pop('pull_policy', None)
    return config


def verify_running_image(run, compose, image):
    def output(command):
        return run(command, capture_output=True, text=True).stdout.strip()
    container = output(compose + ['ps', '-q', 'app'])
    require(bool(re.fullmatch(r'[0-9a-f]{12,64}', container)), 'Expected exactly one running app container')
    expected = output(['docker', 'image', 'inspect', image, '--format', '{{.Id}}'])
    actual = output(['docker', 'inspect', container, '--format', '{{.Image}}'])
    require(bool(re.fullmatch(r'sha256:[0-9a-f]{64}', expected)) and actual == expected,
            'Running app image differs from the pulled tested digest')
    return actual


def api(path, token=None, body=None, method=None, expected=200):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    request = urllib.request.Request('http://127.0.0.1:8000' + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers=headers, method=method)
    try:
        response = urllib.request.urlopen(request, timeout=5)
    except urllib.error.HTTPError as response:
        status, data = response.code, response.read()
    else:
        with response:
            status, data = response.status, response.read()
    if status != expected:
        raise RuntimeError(f'Smoke check {method or "GET"} {path} returned {status}, expected {expected}')
    return json.loads(data)


def smoke(env_file):
    # Read generated key=value data; never execute it as shell code.
    values = dict(line.split('=', 1) for line in env_file.read_text(encoding='utf-8').splitlines()
                  if line and not line.startswith('#') and '=' in line)
    alice, bob = values['LAB_ALICE_TOKEN'], values['LAB_BOB_TOKEN']
    require(len(alice) >= 32 and len(bob) >= 32 and alice != bob, 'Use distinct generated lab tokens')
    deadline = time.monotonic() + 60
    while True:
        try:
            require(api('/livez') == {'status': 'ok'}, 'Unexpected liveness body')
            require(api('/readyz') == {'status': 'ready'}, 'Unexpected readiness body')
            break
        except (OSError, RuntimeError, ValueError):
            if time.monotonic() >= deadline:
                raise RuntimeError('Staging did not become ready within the readiness window')
            time.sleep(1)
    api('/tasks', expected=401)
    api('/tasks', 'deliberately-invalid-token', expected=401)
    title = 'Release smoke ' + uuid4().hex
    task = api('/tasks', alice, {'title': title}, expected=201)
    require(task['title'] == title and task['completed'] is False, 'Create returned an incorrect task')
    path = '/tasks/' + task['id']
    require(api(path, alice) == task, 'Owner read did not match creation')
    api(path, bob, expected=404)
    api(path + '/complete', bob, method='POST', expected=404)
    require(all(item['id'] != task['id'] for item in api('/tasks', bob)['items']), 'Cross-owner list leaked a task')
    require(api(path, alice) == task, 'Rejected cross-owner update changed the task')
    done = api(path + '/complete', alice, method='POST')
    require(done['completed'] is True and bool(done['completed_at']), 'Completion body is incorrect')
    require(api(path + '/complete', alice, method='POST') == done, 'Completion is not idempotent')
    require(api(path, alice) == done, 'Completion was not stored')
    require(done in api('/tasks', alice)['items'], 'Owner list did not contain the completed task')
    return {'task_id': task['id'], 'business_checks': 'passed', 'version': api('/version')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['deploy', 'rollback'])
    parser.add_argument('--target', default='/opt/devopps-staging')
    parser.add_argument('--image-file', default='tested-digest.txt')
    parser.add_argument('--compose', default='compose.yaml')
    args = parser.parse_args()
    target = Path(args.target).resolve()
    if target != Path('/opt/devopps-staging'):
        raise SystemExit('This teaching helper only operates /opt/devopps-staging')
    if not (target / '.env').is_file():
        raise SystemExit('Prepare the target and its private .env before deployment')
    if os.environ.get('SCHEMA_COMPATIBLE') != 'yes':
        raise SystemExit('Review current/previous schema compatibility, then set SCHEMA_COMPATIBLE=yes for this manual job')
    try:
        pipeline_id = int(os.environ['CI_PIPELINE_ID'])
        registry = os.environ['CI_REGISTRY_IMAGE']
        require(pipeline_id > 0 and bool(registry), 'Missing pipeline identity')
        for name in ('CI_REGISTRY', 'CI_REGISTRY_USER', 'CI_REGISTRY_PASSWORD'):
            require(bool(os.environ.get(name)), 'Missing registry job credential')
    except (KeyError, ValueError):
        raise SystemExit('Run this helper from the configured protected GitLab job with its registry credentials')
    reports = target / 'reports'
    reports.mkdir(exist_ok=True)
    with (target / '.deployment.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state_file = target / 'state.json'
        if not state_file.exists() and any((target / name).exists() for name in
                ('watermark.json', 'good.json', 'previous.json', 'attempt.json')):
            raise SystemExit('Legacy deployment records exist: inspect and migrate them before using this ledger. Do not erase stale-job protection.')
        state = read_json(state_file, {'watermark': None, 'good': None,
            'previous': None, 'attempt': None, 'recovery': None})
        watermark, good, previous, attempt = (state[name] for name in
            ('watermark', 'good', 'previous', 'attempt'))
        if args.mode == 'deploy':
            image = Path(args.image_file).read_text(encoding='utf-8').strip()
            check_candidate(pipeline_id, image, registry, watermark)
            commit = os.environ.get('CI_COMMIT_SHA', '')
            require(bool(re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', commit)), 'A full source commit is required')
            release = {'image': image, 'commit': commit,
                       'compose': Path(args.compose).read_text(encoding='utf-8'), 'pipeline_id': pipeline_id}
            state['watermark'] = {'pipeline_id': pipeline_id, 'image': image}
        else:
            if watermark and pipeline_id < watermark['pipeline_id']:
                raise SystemExit('An older pipeline cannot roll back a newer approved release')
            release = recovery_release(good, previous, attempt, state.get('recovery'))
            state['recovery'] = release
            image = release['image']
            check_identity(pipeline_id, image, registry)
            if not watermark or pipeline_id > watermark['pipeline_id']:
                state['watermark'] = {'pipeline_id': pipeline_id, 'image': image}
        state['attempt'] = {'pipeline_id': pipeline_id, 'image': image, 'mode': args.mode, 'status': 'running'}
        save_json(state_file, state)
        started = time.monotonic()
        # The temporary directory is private and removed on exit. The resolved
        # Compose model contains credentials and must never be printed or archived.
        with tempfile.TemporaryDirectory(prefix='.registry-', dir=target) as credentials:
            env = dict(os.environ, TASKBOARD_IMAGE=image, DOCKER_CONFIG=credentials)
            def run(command, **kwargs):
                kwargs.setdefault('timeout', 600)
                return subprocess.run(command, cwd=target, env=env, check=True, **kwargs)
            compose = ['docker', 'compose', '--project-name', 'devopps-staging', '--env-file', str(target / '.env'), '--file', str(target / 'compose.yaml')]
            try:
                save_text(target / 'compose.yaml', release['compose'])
                config = json.loads(run(compose + ['config', '--format', 'json'], capture_output=True, text=True).stdout)
                effective = Path(credentials) / 'effective-compose.json'
                save_json(effective, validate_compose(config, image))
                compose[-1] = str(effective)
                run(['docker', 'login', os.environ['CI_REGISTRY'], '-u', os.environ['CI_REGISTRY_USER'], '--password-stdin'], input=os.environ['CI_REGISTRY_PASSWORD'].encode(), stdout=subprocess.DEVNULL)
                run(['docker', 'pull', image])
                run(compose + ['up', '-d', '--no-build', 'db'])
                deadline = time.monotonic() + 60
                while subprocess.run(compose + ['exec', '-T', 'db', 'pg_isready', '-U', 'taskboard', '-d', 'taskboard'], cwd=target, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10).returncode:
                    if time.monotonic() >= deadline:
                        raise RuntimeError('Database did not become ready within the readiness window')
                    time.sleep(1)
                if args.mode == 'deploy':
                    run(compose + ['run', '--rm', '--no-deps', '--pull', 'never', 'migrate'])
                run(compose + ['up', '-d', '--no-deps', '--no-build', '--pull', 'never', '--force-recreate', 'app'])
                running_image_id = verify_running_image(run, compose, image)
                result = smoke(target / '.env')
                require(result['version'].get('git_sha') == release['commit'],
                        'Running version does not match the recorded release commit')
                if args.mode == 'deploy' and good and any(good[key] != release[key]
                        for key in ('image', 'commit', 'compose')):
                    state['previous'] = good
                state['good'] = release
                status = {'pipeline_id': pipeline_id, 'image': image, 'running_image_id': running_image_id, 'mode': args.mode, 'status': 'passed', 'elapsed_seconds': round(time.monotonic() - started, 2), **result}
                state['attempt'] = status
                # One replacement commits good/previous/attempt together, so
                # interruption cannot make recovery choose a half-updated pair.
                save_json(state_file, state)

            except Exception as error:
                status = {'pipeline_id': pipeline_id, 'image': image, 'mode': args.mode, 'status': 'failed', 'error_type': type(error).__name__, 'elapsed_seconds': round(time.monotonic() - started, 2)}
                state['attempt'] = status
                save_json(state_file, state)
                save_json(reports / f'{pipeline_id}-{args.mode}.json', status)
                raise SystemExit('Deployment failed. Inspect the private target and sanitized report; use the recorded compatible rollback procedure. No data was restored or deleted.')
            save_json(reports / f'{pipeline_id}-{args.mode}.json', status)
            print(json.dumps(status))


if __name__ == '__main__':
    main()
