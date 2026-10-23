import test from 'node:test';
import assert from 'node:assert/strict';
import {webcrypto} from 'node:crypto';
import {createProgressHandler, createTokenVerifier, MAX_BODY_BYTES, validateProgress} from '../functions/_lib/progress.mjs';
import {createNeonStore} from '../functions/_lib/neon-store.mjs';
import {neonConfig} from '@neondatabase/serverless';

const origin = 'https://devoops.tech';
const issuer = 'https://clerk.example.test';
const now = Date.now();
const seconds = Math.floor(now / 1000);
const keyPair = await webcrypto.subtle.generateKey({name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048,
  publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256'}, true, ['sign', 'verify']);
const publicKey = {...await webcrypto.subtle.exportKey('jwk', keyPair.publicKey), kid: 'test-key', use: 'sig', alg: 'RS256'};
const baseClaims = {iss: issuer, azp: origin, sub: 'user_alice', sid: 'sess_alice', iat: seconds - 10, nbf: seconds - 10, exp: seconds + 60};
const env = {PROGRESS_SYNC_ENABLED: 'true', APP_ORIGINS: origin, CLERK_ISSUER: issuer, DATABASE_URL: 'server-secret'};
const sample = () => ({schemaVersion: 1, edition: '2026-10-20', weeks: {'1': {status: 'Proved', note: 'Restored the test data and checked all five records.', updated: '2026-10-21T12:00:00Z'}}});
const encoded = value => Buffer.from(typeof value === 'string' ? value : JSON.stringify(value)).toString('base64url');
async function token(changes = {}, headerChanges = {}) {
  const header = encoded({alg: 'RS256', typ: 'JWT', kid: 'test-key', ...headerChanges});
  const payload = encoded({...baseClaims, ...changes});
  const signature = await webcrypto.subtle.sign('RSASSA-PKCS1-v1_5', keyPair.privateKey, new TextEncoder().encode(`${header}.${payload}`));
  return `${header}.${payload}.${Buffer.from(signature).toString('base64url')}`;
}
function request(method, jwt, body, headers = {}, url = `${origin}/api/progress`) {
  return new Request(url, {method, headers: {'Authorization': `Bearer ${jwt}`, ...(body !== undefined ? {'Content-Type': 'application/json'} : {}), ...headers},
    ...(body !== undefined ? {body: typeof body === 'string' ? body : JSON.stringify(body)} : {})});
}
function fixture({jwksStatus = 200} = {}) {
  const rows = new Map();
  let sequence = 0, queries = 0, jwksFetches = 0;
  const verify = createTokenVerifier({now: () => now, cryptoImpl: webcrypto, fetchImpl: async (url, options) => {
    jwksFetches++;
    assert.equal(url, `${issuer}/.well-known/jwks.json`);
    assert.equal(options.redirect, 'error');
    return new Response(JSON.stringify({keys: [publicKey]}), {status: jwksStatus});
  }});
  const handle = createProgressHandler({verify, createStore: () => ({
    async get(user) { queries++; return rows.get(user) || null; },
    async save(user, progress, expectedRevision) {
      queries++;
      if ((rows.get(user)?.revision || 0) !== expectedRevision) return null;
      const result = {progress, revision: ++sequence, updatedAt: new Date(now).toISOString()};
      rows.set(user, result);
      return result;
    },
    async remove(user, expectedRevision) {
      queries++;
      if (!rows.has(user) || rows.get(user).revision !== expectedRevision) return null;
      rows.delete(user);
      return {progress: null, revision: 0, updatedAt: null};
    }
  })});
  return {handle: (req, config = env) => handle({request: req, env: config}), rows,
    queries: () => queries, jwksFetches: () => jwksFetches};
}

test('disabled sync does not contact identity or database providers', async () => {
  const f = fixture();
  const response = await f.handle(request('GET', ''), {...env, PROGRESS_SYNC_ENABLED: 'false'});
  assert.equal(response.status, 503);
  assert.equal((await response.json()).error, 'sync_disabled');
  assert.equal(f.jwksFetches(), 0);
  assert.equal(f.queries(), 0);
});

test('configuration rejects an insecure or path-bearing issuer and invalid application origins', async () => {
  for (const change of [{CLERK_ISSUER: 'http://clerk.example.test'}, {CLERK_ISSUER: `${issuer}/path`}, {APP_ORIGINS: `${origin}/path`}, {DATABASE_URL: ''}]) {
    const f = fixture();
    assert.equal((await f.handle(request('GET', ''), {...env, ...change})).status, 503);
    assert.equal(f.jwksFetches(), 0);
  }
});

test('missing bearer token and cookie-only authentication are rejected', async () => {
  const f = fixture();
  const req = new Request(`${origin}/api/progress`, {headers: {Cookie: `__session=${await token()}`}});
  assert.equal((await f.handle(req)).status, 401);
  assert.equal(f.queries(), 0);
});

test('valid signed session can create, read, compare-and-swap and delete only its own progress', async () => {
  const f = fixture();
  const alice = await token();
  const bob = await token({sub: 'user_bob', sid: 'sess_bob'});
  assert.deepEqual(await (await f.handle(request('GET', alice))).json(), {progress: null, revision: 0, updatedAt: null});
  const created = await f.handle(request('PUT', alice, {progress: sample(), expectedRevision: 0}));
  assert.equal(created.status, 200);
  const first = await created.json();
  assert.equal(first.revision, 1);
  assert.equal((await (await f.handle(request('GET', bob))).json()).progress, null);
  assert.equal((await f.handle(request('PUT', alice, {progress: sample(), expectedRevision: 0}))).status, 409);
  assert.equal((await f.handle(request('DELETE', bob, {expectedRevision: first.revision}))).status, 409);
  const changed = sample(); changed.weeks['1'].note = 'Updated evidence';
  const second = await (await f.handle(request('PUT', alice, {progress: changed, expectedRevision: first.revision}))).json();
  assert.equal(second.revision, 2);
  assert.equal((await f.handle(request('DELETE', alice, {expectedRevision: first.revision}))).status, 409);
  assert.equal((await f.handle(request('DELETE', alice, {expectedRevision: second.revision}))).status, 200);
  const recreated = await (await f.handle(request('PUT', alice, {progress: sample(), expectedRevision: 0}))).json();
  assert.ok(recreated.revision > second.revision);
  assert.equal(f.jwksFetches(), 1, 'signing keys are cached');
  assert.equal(created.headers.get('cache-control'), 'no-store, private');
  assert.equal(created.headers.get('access-control-allow-origin'), null);
});

test('rejects expired, future, wrong issuer, wrong party, wrong audience and pending sessions', async () => {
  const cases = [
    {exp: seconds - 30}, {nbf: seconds + 60}, {iat: seconds + 60},
    {iss: 'https://attacker.test'}, {azp: 'https://attacker.test'}, {azp: undefined},
    {sub: 'user_alice OR 1=1'}, {sid: undefined}, {sts: 'pending'}, {exp: '9999999999'}
  ];
  for (const claims of cases) {
    const f = fixture();
    assert.equal((await f.handle(request('GET', await token(claims)))).status, 401, JSON.stringify(claims));
    assert.equal(f.queries(), 0);
  }
  const f = fixture();
  assert.equal((await f.handle(request('GET', await token({aud: 'other'})), {...env, CLERK_AUDIENCE: 'progress'})).status, 401);
  assert.equal((await f.handle(request('GET', await token({aud: ['progress']})), {...env, CLERK_AUDIENCE: 'progress'})).status, 200);
});

test('rejects tampering, unsigned algorithms, unknown key ids and critical JWT extensions', async () => {
  const valid = await token();
  const pieces = valid.split('.');
  pieces[1] = encoded({...baseClaims, sub: 'user_victim'});
  const tokens = [pieces.join('.'), await token({}, {alg: 'none'}), await token({}, {kid: 'unknown'}), await token({}, {crit: ['b64']}), 'bad.token'];
  for (const jwt of tokens) {
    const f = fixture();
    assert.equal((await f.handle(request('GET', jwt))).status, 401);
    assert.equal(f.queries(), 0);
  }
});

test('JWKS failure is unavailable, never a bypass or a database query', async () => {
  const f = fixture({jwksStatus: 503});
  assert.equal((await f.handle(request('GET', await token()))).status, 503);
  assert.equal(f.queries(), 0);
});

test('cross-origin and unknown-host requests are rejected before authentication', async () => {
  const jwt = await token();
  for (const req of [request('PUT', jwt, {}, {Origin: 'https://attacker.test'}), request('GET', jwt, undefined, {'Sec-Fetch-Site': 'cross-site'}), request('GET', jwt, undefined, {}, 'https://preview.pages.dev/api/progress')]) {
    const f = fixture();
    assert.equal((await f.handle(req)).status, 403);
    assert.equal(f.jwksFetches(), 0);
    assert.equal(f.queries(), 0);
  }
});

test('schema rejects invalid weeks, missing proved evidence, oversized notes and forged row owners', async () => {
  const invalid = [
    {schemaVersion: 2, edition: '2026-10-20', weeks: {}},
    {schemaVersion: 1, edition: '2026-10-20', weeks: {'53': {status: 'Learning', note: ''}}},
    {schemaVersion: 1, edition: '2026-10-20', weeks: {'1': {status: 'Proved', note: '   '}}},
    {schemaVersion: 1, edition: '2026-10-20', weeks: {'1': {status: 'Learning', note: 'a'.repeat(20001)}}},
    {...sample(), user_id: 'user_victim'},
    JSON.parse('{"schemaVersion":1,"edition":"2026-10-20","weeks":{"__proto__":{}}}')
  ];
  const jwt = await token();
  for (const progress of invalid) {
    const f = fixture();
    assert.equal((await f.handle(request('PUT', jwt, {progress, expectedRevision: 0}))).status, 400);
    assert.equal(f.queries(), 0);
  }
  assert.deepEqual(validateProgress({...sample(), exportedAt: '2026-10-21T12:00:00Z'}), sample());
});

test('requires JSON, rejects negative or missing revisions and unknown request properties', async () => {
  const f = fixture();
  const jwt = await token();
  assert.equal((await f.handle(request('PUT', jwt, '{}', {'Content-Type': 'text/plain'}))).status, 415);
  assert.equal((await f.handle(request('PUT', jwt, '{}', {'Content-Encoding': 'gzip'}))).status, 415);
  for (const body of [{progress: sample()}, {progress: sample(), expectedRevision: -1}, {progress: sample(), expectedRevision: 0, userId: 'user_victim'}]) {
    assert.equal((await f.handle(request('PUT', jwt, body))).status, 400);
  }
  assert.equal((await f.handle(request('PUT', jwt, '{broken'))).status, 400);
  assert.equal(f.queries(), 0);
});

test('enforces the byte limit even when Content-Length is absent', async () => {
  const f = fixture();
  const response = await f.handle(request('PUT', await token(), ' '.repeat(MAX_BODY_BYTES + 1)));
  assert.equal(response.status, 413);
  assert.equal(f.queries(), 0);
});

test('provider errors never leak credentials or SQL to a browser', async () => {
  const handle = createProgressHandler({verify: async () => 'user_alice', createStore: () => ({get() {throw new Error('postgresql://secret:password@db SELECT *');}})});
  const response = await handle({request: request('GET', 'test'), env});
  assert.equal(response.status, 503);
  assert.doesNotMatch(await response.text(), /password|postgresql|SELECT/);
});

test('other methods never contact providers', async () => {
  const f = fixture();
  const response = await f.handle(new Request(`${origin}/api/progress`, {method: 'OPTIONS'}));
  assert.equal(response.status, 405);
  assert.equal(response.headers.get('allow'), 'GET, PUT, DELETE');
  assert.equal(f.queries(), 0);
});

test('the pinned Neon HTTP driver keeps owner and evidence in parameters and decodes the database envelope', async () => {
  const originalFetch = neonConfig.fetchFunction;
  const calls = [];
  neonConfig.fetchFunction = async (url, options) => {
    assert.equal(new URL(url).protocol, 'https:');
    assert.equal(new URL(url).pathname, '/sql');
    assert.ok(options.signal instanceof AbortSignal);
    calls.push(JSON.parse(options.body));
    return new Response(JSON.stringify({
      fields: [{name: 'progress', dataTypeID: 3802}, {name: 'revision', dataTypeID: 20}, {name: 'updated_at', dataTypeID: 1184}],
      rows: [[JSON.stringify(sample()), '42', '2026-10-21 12:00:00+00']], rowCount: 1, command: 'SELECT', rowAsArray: true
    }), {status: 200});
  };
  try {
    const store = createNeonStore({DATABASE_URL: 'postgresql://test:example@ep-test.us-east-2.aws.neon.tech/test?sslmode=require'});
    const progress = sample(); progress.weeks['1'].note = "'; DROP TABLE learner_progress; --";
    const saved = await store.save('user_alice', progress, 7);
    assert.equal(saved.revision, 42);
    assert.equal(saved.updatedAt, '2026-10-21T12:00:00.000Z');
    assert.deepEqual(calls[0].params, ['user_alice', JSON.stringify(progress), '7']);
    assert.doesNotMatch(calls[0].query, /user_alice|DROP TABLE/);
    await store.get('user_alice');
    assert.deepEqual(calls[1].params, ['user_alice']);
    assert.match(calls[1].query, /WHERE user_id = \$1/);
  } finally { neonConfig.fetchFunction = originalFetch; }
});

test('the Neon adapter maps empty compare-and-swap results to conflicts', async () => {
  const originalFetch = neonConfig.fetchFunction;
  neonConfig.fetchFunction = async () => new Response(JSON.stringify({fields: [], rows: [], rowCount: 0, command: 'SELECT', rowAsArray: true}), {status: 200});
  try {
    const store = createNeonStore({DATABASE_URL: 'postgresql://test:example@ep-test.us-east-2.aws.neon.tech/test?sslmode=require'});
    assert.equal(await store.get('user_alice'), null);
    assert.equal(await store.save('user_alice', sample(), 7), null);
    assert.equal(await store.remove('user_alice', 7), null);
  } finally { neonConfig.fetchFunction = originalFetch; }
});
