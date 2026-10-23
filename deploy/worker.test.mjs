import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile} from 'node:fs/promises';
import {webcrypto} from 'node:crypto';

// Evaluate the built artifact without Node globals or module resolution.
const source = await readFile(new URL('./worker-build/_worker.js', import.meta.url), 'utf8');
let networkHandler = () => {throw new Error('Unexpected external network request');};
const context = vm.createContext({
  crypto: webcrypto, TextEncoder, TextDecoder, URL, Request, Response, Headers,
  AbortController, AbortSignal, atob, btoa, console, setTimeout, clearTimeout,
  fetch(...args) {return networkHandler(...args);}
});
const module = new vm.SourceTextModule(source, {context});
await module.link(() => {throw new Error('Bundle contains an external import');});
await module.evaluate();
const worker = module.namespace.default;

test('the built module forwards public lessons/assets directly to ASSETS', async () => {
  const request = new Request('https://devoops.tech/handbook/start-here.md?view=plain');
  let received;
  const response = await worker.fetch(request, {ASSETS: {async fetch(value) {received = value; return new Response('public lesson');}}});
  assert.equal(received, request);
  assert.equal(await response.text(), 'public lesson');
});

test('the built module handles disabled API without forwarding to static HTML', async () => {
  const response = await worker.fetch(new Request('https://devoops.tech/api/progress'), {
    ASSETS: {fetch() {throw new Error('API must not fall back to an asset');}}
  });
  assert.equal(response.status, 503);
  assert.equal((await response.json()).error, 'sync_disabled');
});

test('enabled API still rejects anonymous requests inside the bundled artifact', async () => {
  const response = await worker.fetch(new Request('https://devoops.tech/api/progress'), {
    PROGRESS_SYNC_ENABLED: 'true', APP_ORIGINS: 'https://devoops.tech',
    CLERK_ISSUER: 'https://clerk.example.test', DATABASE_URL: 'not-used-before-authentication',
    ASSETS: {fetch() {throw new Error('API must not fall back to an asset');}}
  });
  assert.equal(response.status, 401);
  assert.equal((await response.json()).error, 'not_signed_in');
});

test('deployment routes invoke the function only for the progress endpoint', async () => {
  const routes = JSON.parse(await readFile(new URL('./worker-build/_routes.json', import.meta.url), 'utf8'));
  assert.deepEqual(routes, {version: 1, include: ['/api/progress'], exclude: []});
});

test('the self-contained bundle verifies a signed session and queries Neon without Node globals', async () => {
  const keys = await webcrypto.subtle.generateKey({name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048,
    publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256'}, true, ['sign', 'verify']);
  const jwk = {...await webcrypto.subtle.exportKey('jwk', keys.publicKey), kid: 'bundled-test', alg: 'RS256', use: 'sig'};
  const now = Math.floor(Date.now() / 1000);
  const encode = value => Buffer.from(JSON.stringify(value)).toString('base64url');
  const header = encode({alg: 'RS256', kid: 'bundled-test'});
  const payload = encode({iss: 'https://clerk.example.test', azp: 'https://devoops.tech', sub: 'user_bundled', sid: 'sess_bundled',
    iat: now - 10, nbf: now - 10, exp: now + 60});
  const signature = await webcrypto.subtle.sign('RSASSA-PKCS1-v1_5', keys.privateKey, new TextEncoder().encode(`${header}.${payload}`));
  const token = `${header}.${payload}.${Buffer.from(signature).toString('base64url')}`;
  const seen = [];
  networkHandler = async (url, options) => {
    seen.push(url);
    if (url === 'https://clerk.example.test/.well-known/jwks.json') return Response.json({keys: [jwk]});
    assert.equal(new URL(url).pathname, '/sql');
    const body = JSON.parse(options.body);
    assert.deepEqual(body.params, ['user_bundled']);
    assert.match(body.query, /WHERE user_id = \$1/);
    return Response.json({fields: [], rows: [], rowCount: 0, command: 'SELECT', rowAsArray: true});
  };
  const response = await worker.fetch(new Request('https://devoops.tech/api/progress', {headers: {Authorization: `Bearer ${token}`}}), {
    PROGRESS_SYNC_ENABLED: 'true', APP_ORIGINS: 'https://devoops.tech', CLERK_ISSUER: 'https://clerk.example.test',
    DATABASE_URL: 'postgresql://test:example@ep-test.us-east-2.aws.neon.tech/test?sslmode=require'
  });
  const result = await response.json();
  assert.equal(response.status, 200, JSON.stringify({result, seen}));
  assert.deepEqual(result, {progress: null, revision: 0, updatedAt: null});
  assert.equal(seen.length, 2);
});
