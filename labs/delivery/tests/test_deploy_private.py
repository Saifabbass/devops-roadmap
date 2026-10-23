"""No Docker, network, Linux lock or cloud execution: these are control-flow tests.

Windows imports use a scoped fcntl stub. Subprocess and HTTP boundaries are
replaced explicitly; a passing result does not validate Docker/Compose/locking.
Run: python -m unittest discover -s labs/delivery/tests -v
"""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

HELPER = Path(__file__).resolve().parents[1] / 'deploy_private.py'
spec = importlib.util.spec_from_file_location('deploy_private', HELPER)
deploy = importlib.util.module_from_spec(spec)
if sys.platform == 'win32':
    with patch.dict(sys.modules, {'fcntl': types.SimpleNamespace(LOCK_EX=2, flock=lambda *_: None)}):
        spec.loader.exec_module(deploy)
else:
    spec.loader.exec_module(deploy)
REGISTRY = 'registry.example.invalid/course/taskboard'
A, B, C = (REGISTRY + '@sha256:' + letter * 64 for letter in 'abc')
COMMIT = '1' * 40


def model(image=A):
    return {'name': 'devopps-staging', 'services': {
        'app': {'image': image, 'build': {'context': '.'}, 'pull_policy': 'build',
            'command': ['python', '-m', 'uvicorn', 'reference.stage07:app'],
            'ports': [{'host_ip': '127.0.0.1', 'target': 8000, 'published': '8000', 'protocol': 'tcp'}],
            'networks': {'backend': None}},
        'migrate': {'image': image, 'command': ['python', '-m', 'reference.migrate'],
            'networks': {'backend': None}},
        'db': {'image': 'postgres:17', 'networks': {'backend': None}, 'volumes': [
            {'type': 'volume', 'source': 'taskboard-data', 'target': '/var/lib/postgresql/data'}]}},
        'networks': {'backend': {'name': 'devopps-staging_backend', 'internal': True}},
        'volumes': {'taskboard-data': {'name': 'devopps-staging_taskboard-data'}}}


class GuardTests(unittest.TestCase):
    def test_candidate_exact_digest_stale_and_substitution(self):
        watermark = {'pipeline_id': 10, 'image': A}
        for pipeline, image, registry in [(0,A,REGISTRY), (-1,A,REGISTRY),
                (True,A,REGISTRY), (10,REGISTRY + ':latest',REGISTRY),
                (10,A,'registry.example.invalid/another/project'),
                (9,A,REGISTRY), (10,B,REGISTRY), (10,A + '\n',REGISTRY)]:
            with self.subTest(pipeline=pipeline, image=image), self.assertRaises(ValueError):
                deploy.check_candidate(pipeline, image, registry, watermark)
        deploy.check_candidate(10,A,REGISTRY,watermark)
        deploy.check_candidate(11,B,REGISTRY,watermark)

    def test_rollback_uses_exact_pending_target_after_failure_or_interruption(self):
        good, previous, target = {'image': B}, {'image': A}, {'image': B}
        for status in ('failed', 'running'):
            with self.subTest(status=status):
                self.assertEqual(deploy.recovery_release(good,previous,{'mode':'deploy','status':status}),good)
                self.assertEqual(deploy.recovery_release(good,previous,{'mode':'rollback','status':status},target),target)
                with self.assertRaises(ValueError):
                    deploy.recovery_release(good,previous,{'mode':'rollback','status':status})
        self.assertEqual(deploy.recovery_release(good,previous,{'mode':'deploy','status':'passed'}),previous)
        self.assertEqual(deploy.recovery_release(good,previous,{'mode':'rollback','status':'passed'},target),good)
        with self.assertRaises(ValueError):
            deploy.recovery_release(None,None,{'mode':'deploy','status':'failed'})

    def test_compose_contract_and_build_removal(self):
        config = deploy.validate_compose(model(),A)
        self.assertNotIn('build',config['services']['app'])
        self.assertNotIn('pull_policy',config['services']['app'])

    def test_rejects_wrong_image_public_port_volume_or_stage(self):
        mutations = [
            lambda c: c['services']['app'].update(image=B),
            lambda c: c['services']['migrate'].update(image=B),
            lambda c: c['services']['app']['ports'][0].update(host_ip='0.0.0.0'),
            lambda c: c['services']['app']['ports'][0].update(published='8001'),
            lambda c: c['services']['app'].update(ports=[]),
            lambda c: c['services']['db'].update(ports=[{'published':'5432'}]),
            lambda c: c['services']['app'].update(command=['reference.stage06:app']),
            lambda c: c['services']['app'].update(volumes=[{'type':'bind','source':'/tmp','target':'/app'}]),
            lambda c: c['services']['app'].update(privileged=True),
            lambda c: c['networks']['backend'].update(internal=False),
            lambda c: c['services']['db']['volumes'][0].update(source='other-data'),
            lambda c: c['volumes']['taskboard-data'].update(name='otherproject_data'),
            lambda c: c['services']['app'].update(network_mode='host'),
        ]
        for i, mutate in enumerate(mutations):
            with self.subTest(case=i):
                config=model(); mutate(config)
                with self.assertRaises(ValueError): deploy.validate_compose(config,A)

    def test_running_image_identity_and_single_container(self):
        def runner(values):
            results=iter(values)
            return lambda *args, **kwargs: subprocess.CompletedProcess(args[0],0,stdout=next(results))
        image_id='sha256:'+'d'*64
        self.assertEqual(deploy.verify_running_image(runner(['a'*64,image_id,image_id]),['compose'],A),image_id)
        for values in [['a'*64,image_id,'sha256:'+'e'*64], ['',image_id,image_id],['a'*64+'\n'+'b'*64,image_id,image_id]]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                deploy.verify_running_image(runner(values),['compose'],A)

    def test_invalid_target_refused_before_external_operation(self):
        with patch.object(sys,'argv',['deploy_private.py','deploy','--target','/not-this-course']), patch.object(deploy.subprocess,'run') as run:
            with self.assertRaises(SystemExit): deploy.main()
            run.assert_not_called()


class LedgerFlowTests(unittest.TestCase):
    def setUp(self):
        self.sandbox=tempfile.TemporaryDirectory(prefix='deploy-audit-',dir=HELPER.parent)
        self.addCleanup(self.sandbox.cleanup)
        self.target=Path(self.sandbox.name)
        (self.target/'.env').write_text('LAB_ALICE_TOKEN='+'a'*32+'\nLAB_BOB_TOKEN='+'b'*32+'\n')
        self.candidate=self.target/'tested-digest.txt'
        self.compose_source=self.target/'candidate-compose.yaml'
        self.compose_source.write_text('reviewed source config\n')
        self.calls=[]
        self.fail_smoke=False
        self.wrong_image=False
        self.bad_config=False
        self.environment={'CI_PIPELINE_ID':'10','CI_REGISTRY_IMAGE':REGISTRY,'CI_COMMIT_SHA':COMMIT,
            'CI_REGISTRY':'registry.example.invalid','CI_REGISTRY_USER':'test-job','CI_REGISTRY_PASSWORD':'synthetic-not-a-real-secret',
            'SCHEMA_COMPATIBLE':'yes'}
        self.addCleanup(patch.stopall)
        patch.dict(os.environ,self.environment).start()
        real_path=Path
        def local_path(value):
            return self.target if str(value)=='/opt/devopps-staging' else real_path(value)
        patch.object(deploy,'Path',local_path).start()
        patch.object(deploy.subprocess,'run',side_effect=self.fake_docker).start()
        patch.object(deploy,'smoke',side_effect=self.smoke).start()
        patch('builtins.print').start()

    def fake_docker(self,command,**kwargs):
        self.calls.append((command,kwargs))
        stdout=''
        if command[-3:]==['config','--format','json']:
            config=model(kwargs['env']['TASKBOARD_IMAGE'])
            if self.bad_config: config['services']['app']['image']=B
            stdout=json.dumps(config)
        elif command[-3:]==['ps','-q','app']: stdout='c'*64
        elif command[:3]==['docker','image','inspect']: stdout='sha256:'+'d'*64
        elif command[:2]==['docker','inspect']: stdout='sha256:'+('e' if self.wrong_image else 'd')*64
        return subprocess.CompletedProcess(command,0,stdout=stdout,stderr='')

    def smoke(self,_):
        if self.fail_smoke: raise RuntimeError('synthetic smoke failure')
        return {'task_id':'synthetic-task','business_checks':'passed','version':{'git_sha':COMMIT}}

    def invoke(self,mode,image=A,pipeline=10):
        self.candidate.write_text(image+'\n')
        os.environ['CI_PIPELINE_ID']=str(pipeline)
        with patch.object(sys,'argv',['deploy_private.py',mode,'--image-file',str(self.candidate),'--compose',str(self.compose_source)]):
            deploy.main()

    def state(self):
        return json.loads((self.target/'state.json').read_text())

    def test_deploy_failure_rollback_failure_and_retry(self):
        self.invoke('deploy',A,10)
        self.fail_smoke=True
        with self.assertRaises(SystemExit): self.invoke('deploy',B,11)
        state=self.state()
        self.assertEqual(state['good']['image'],A)
        self.assertEqual(state['watermark']['pipeline_id'],11)
        self.assertIsNone(state['previous'])
        with self.assertRaises(SystemExit): self.invoke('rollback',pipeline=11)
        state=self.state()
        self.assertEqual(state['recovery']['image'],A)
        self.assertEqual(state['attempt']['mode'],'rollback')
        self.fail_smoke=False
        self.invoke('rollback',pipeline=11)
        self.assertEqual(self.state()['good']['image'],A)
        self.invoke('rollback',pipeline=11)
        self.assertEqual(self.state()['good']['image'],A)
        before=len(self.calls)
        with self.assertRaises(ValueError): self.invoke('deploy',A,10)
        self.assertEqual(len(self.calls),before)
        self.assertEqual(self.state()['watermark']['pipeline_id'],11)

    def test_successful_release_rollback_and_config_only_recovery(self):
        self.invoke('deploy',A,10)
        self.compose_source.write_text('second reviewed source config\n')
        self.invoke('deploy',A,11)
        self.assertEqual(self.state()['previous']['compose'],'reviewed source config\n')
        self.invoke('rollback',pipeline=11)
        self.assertEqual(self.state()['good']['compose'],'reviewed source config\n')
        self.invoke('deploy',C,12)
        self.assertEqual(self.state()['previous']['image'],A)
        self.invoke('rollback',pipeline=12)
        self.assertEqual(self.state()['good']['image'],A)

    def test_interrupted_deploy_uses_good_not_older_previous(self):
        self.invoke('deploy',A,10); self.invoke('deploy',B,11)
        state=self.state()
        state['attempt']={'mode':'deploy','status':'running','image':C,'pipeline_id':12}
        state['watermark']={'pipeline_id':12,'image':C}
        deploy.save_json(self.target/'state.json',state)
        self.invoke('rollback',pipeline=12)
        self.assertEqual(self.state()['good']['image'],B)
        self.assertEqual(self.state()['previous']['image'],A)

    def test_same_pipeline_image_substitution_and_stale_rollback(self):
        self.invoke('deploy',A,10)
        before=len(self.calls)
        with self.assertRaises(ValueError): self.invoke('deploy',B,10)
        with self.assertRaises(SystemExit): self.invoke('rollback',pipeline=9)
        self.assertEqual(len(self.calls),before)
        self.assertEqual(self.state()['good']['image'],A)

    def test_mismatch_does_not_mark_good_and_no_build_command_is_run(self):
        self.wrong_image=True
        with self.assertRaises(SystemExit): self.invoke('deploy',A,10)
        self.assertIsNone(self.state()['good'])
        self.assertEqual(self.state()['attempt']['status'],'failed')
        self.assertFalse(any('build' in cmd for cmd,_ in self.calls))
        self.assertFalse(any('rm' in cmd or 'down' in cmd for cmd,_ in self.calls))
        self.assertFalse(any(self.environment['CI_REGISTRY_PASSWORD'] in cmd for cmd,_ in self.calls))
        self.assertFalse(list(self.target.glob('.registry-*')))

    def test_bad_compose_fails_before_start_or_registry_login(self):
        self.bad_config=True
        with self.assertRaises(SystemExit): self.invoke('deploy',A,10)
        self.assertEqual(len(self.calls),1)
        self.assertEqual(self.state()['attempt']['status'],'failed')
        self.assertIsNone(self.state()['good'])

    def test_legacy_records_refused_instead_of_resetting_watermark(self):
        (self.target/'watermark.json').write_text('{"pipeline_id":100}')
        with self.assertRaises(SystemExit): self.invoke('deploy',A,10)
        self.assertEqual(self.calls,[])
        self.assertFalse((self.target/'state.json').exists())


class SmokeChecks(unittest.TestCase):
    def test_incorrect_completion_body_is_rejected_even_under_python_optimization(self):
        with tempfile.TemporaryDirectory(prefix='smoke-audit-',dir=HELPER.parent) as tmp:
            env=Path(tmp)/'.env'
            env.write_text('LAB_ALICE_TOKEN='+'a'*32+'\nLAB_BOB_TOKEN='+'b'*32+'\n')
            task={'id':'a-real-task-id','title':'replaced-on-create','completed':False}
            def fake_api(path,token=None,body=None,method=None,expected=200):
                if path=='/livez': return {'status':'ok'}
                if path=='/readyz': return {'status':'ready'}
                if expected in (401,404): return {'error':{'code':'expected-denial'}}
                if body:
                    task['title']=body['title']; return deepcopy(task)
                if path=='/tasks': return {'items':[]}
                if path.endswith('/complete'): return dict(task,completed=False,completed_at='2026-01-01T00:00:00Z')
                return deepcopy(task)
            with patch.object(deploy,'api',side_effect=fake_api), self.assertRaisesRegex(ValueError,'Completion body'):
                deploy.smoke(env)


if __name__=='__main__':
    unittest.main()
