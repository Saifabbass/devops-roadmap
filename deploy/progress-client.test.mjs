import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile} from 'node:fs/promises';
import {validateProgress} from '../functions/_lib/progress.mjs';

const source = await readFile(new URL('../teaching/progress-sync.js', import.meta.url), 'utf8');
const sample = () => ({schemaVersion: 1, edition: '2026-10-20', weeks: {'1': {status: 'Learning', note: 'My local evidence', updated: ''}}});
function fixture(fetchImpl) {
  const nodes = new Map();
  const calls = [], scripts = [];
  const context = vm.createContext({
    window: {Clerk: {loaded: true, user: {id: 'user_alice'}, session: {id: 'sess_alice', getToken: async () => 'signed-token'}}},
    document: {getElementById(id) {if (!nodes.has(id)) nodes.set(id, {events: {}, children: [], append(child) {this.children.push(child);}, addEventListener(type, handler) {this.events[type] = handler;}}); return nodes.get(id);},
      createElement() {return {dataset: {}, remove() {}};}, head: {append(script) {scripts.push(script);}}},
    location: {protocol: 'https:', origin: 'https://devoops.tech'}, URL, AbortSignal, setTimeout, clearTimeout, TextEncoder, validateProgress,
    progress: sample(), storageOK: true, save() {}, render() {}, confirm: () => true,
    fetch: async (...args) => {calls.push(args); return fetchImpl(...args);}
  });
  vm.runInContext(source, context);
  return {context, nodes, calls, scripts, run: code => vm.runInContext(code, context),
    async click(id) {vm.runInContext('bindProgressSync()', context); await nodes.get(id).events.click();}};
}
const response = (progress, revision, status = 200) => new Response(JSON.stringify({progress, revision, updatedAt: null}), {status});

test('loading the source does not load identity scripts or make network calls', () => {
  const f = fixture(() => {throw Error('Unexpected network');});
  f.run('progressSyncPanel(); bindProgressSync()');
  assert.equal(f.calls.length, 0);
  assert.equal(f.scripts.length, 0);
});

test('disabled accounts stop before loading Clerk or signing in', async () => {
  const f = fixture(() => new Response('{"enabled":false}'));
  await f.click('syncConnect');
  assert.equal(f.calls.length, 1);
  assert.equal(f.calls[0][0], '/sync-config.json');
  assert.equal(f.scripts.length, 0);
  assert.match(f.nodes.get('syncMessage').textContent, /not enabled/);
});

test('fallback and local hosts link to the canonical site without loading authentication or changing progress', async () => {
  const config = {enabled: true, siteOrigin: 'https://devoops.tech', clerkPublishableKey: 'pk_live_example', clerkFrontendApi: 'clerk.devoops.tech'};
  for (const origin of ['https://devoops.pages.dev', 'http://localhost:8080']) {
    const f = fixture(() => new Response(JSON.stringify(config)));
    f.context.location = {origin, protocol: new URL(origin).protocol};
    f.context.window.Clerk = undefined;
    await f.click('syncConnect');
    assert.equal(f.calls.length, 1);
    assert.equal(f.calls[0][0], '/sync-config.json');
    assert.equal(f.scripts.length, 0);
    assert.deepEqual(f.context.progress, sample());
    const message = f.nodes.get('syncMessage');
    assert.match(message.textContent, /Export a backup here, then import it/);
    assert.equal(message.children.length, 1);
    assert.equal(message.children[0].href, 'https://devoops.tech');
    assert.equal(message.children[0].rel, 'noopener noreferrer');
    assert.equal(f.nodes.get('syncLoad').hidden, true);
  }
});

test('canonical site configuration rejects unsafe URLs before loading authentication', async () => {
  for (const siteOrigin of ['javascript:alert(1)', 'http://devoops.tech', 'https://devoops.tech/path', 'https://user:password@devoops.tech', null]) {
    const f = fixture(() => new Response(JSON.stringify({enabled: true, siteOrigin})));
    await f.click('syncConnect');
    assert.equal(f.scripts.length, 0);
    assert.match(f.nodes.get('syncMessage').textContent, /not configured/);
    assert.deepEqual(f.context.progress, sample());
  }
});

test('JSONB property ordering does not create a false cloud conflict', async () => {
  const cloud = sample();
  cloud.weeks['1'] = {note: 'My local evidence', updated: '', status: 'Learning'};
  const f = fixture((url, options) => options.method === 'GET' ? response(cloud, 4) : response(sample(), 5));
  await f.click('syncSave');
  assert.deepEqual(f.calls.map(call => call[1].method), ['GET', 'PUT']);
  assert.equal(JSON.parse(f.calls[1][1].body).expectedRevision, 4);
  assert.equal(f.run('syncRevision'), 5);
  assert.match(f.nodes.get('syncMessage').textContent, /saved successfully/);
});

test('an account switch during a request cannot load the previous account data', async () => {
  let f;
  f = fixture(() => {
    f.context.window.Clerk.user = {id: 'user_bob'};
    f.context.window.Clerk.session = {id: 'sess_bob', getToken: async () => 'bob-token'};
    return response({...sample(), weeks: {}}, 8);
  });
  await f.click('syncLoad');
  assert.deepEqual(f.context.progress, sample());
  assert.equal(f.run('syncRevision'), null);
  assert.match(f.nodes.get('syncMessage').textContent, /account changed/);
});

test('conflicting and uncertain writes preserve local data and clear the revision', async () => {
  for (const fail of [() => response(null, 0, 409), () => {throw Error('Network lost after committing');}]) {
    const f = fixture(fail);
    f.run('syncRevision=7');
    await f.click('syncSave');
    assert.equal(f.run('syncRevision'), null);
    assert.deepEqual(f.context.progress, sample());
    assert.equal(f.run('syncBusy'), false);
  }
});

test('HTML fallback from a static host is not accepted as a cloud backup', async () => {
  const f = fixture(() => new Response('<!doctype html><h1>Course</h1>'));
  await f.click('syncLoad');
  assert.deepEqual(f.context.progress, sample());
  assert.equal(f.run('syncRevision'), null);
  assert.match(f.nodes.get('syncMessage').textContent, /not available on this deployment/);
});
