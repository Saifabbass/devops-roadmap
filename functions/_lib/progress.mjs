// Server-only progress API. No course page or download requires this module.
export const MAX_BODY_BYTES = 2_000_000;
const MAX_TOKEN_LENGTH = 16_384;
const JWKS_TTL_MS = 5 * 60_000;
const UNKNOWN_KEY_COOLDOWN_MS = 30_000;
const STATUSES = new Set(['Not started', 'Learning', 'Built', 'Proved']);
const WEEK = /^(?:[1-9]|[1-4]\d|5[0-2])$/;
const encoder = new TextEncoder();

export class HttpProblem extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

function problem(status, code, message) {
  throw new HttpProblem(status, code, message);
}

function object(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function onlyKeys(value, allowed) {
  return Object.keys(value).every(key => allowed.includes(key));
}

export function validateProgress(value) {
  if (!object(value) || !onlyKeys(value, ['schemaVersion', 'edition', 'weeks', 'exportedAt']) ||
      value.schemaVersion !== 1 || typeof value.edition !== 'string' ||
      !/^\d{4}-\d{2}-\d{2}$/.test(value.edition) || !object(value.weeks) ||
      Object.keys(value.weeks).length > 52) {
    problem(400, 'invalid_progress', 'This is not a valid progress record.');
  }
  const clean = {schemaVersion: 1, edition: value.edition, weeks: {}};
  for (const [week, record] of Object.entries(value.weeks)) {
    if (!WEEK.test(week) || !object(record) || !onlyKeys(record, ['status', 'note', 'updated']) ||
        !STATUSES.has(record.status) || typeof record.note !== 'string' ||
        record.note.length > 20_000 || (record.status === 'Proved' && !record.note.trim()) ||
        (record.updated !== undefined && (typeof record.updated !== 'string' || record.updated.length > 40))) {
      problem(400, 'invalid_progress', 'A week contains invalid progress or evidence.');
    }
    clean.weeks[week] = {status: record.status, note: record.note, updated: record.updated || ''};
  }
  return clean;
}

function canonicalOrigin(value, allowLocal = false) {
  try {
    const url = new URL(value);
    const local = allowLocal && url.protocol === 'http:' && ['localhost', '127.0.0.1'].includes(url.hostname);
    if ((url.protocol !== 'https:' && !local) || url.origin !== value || url.username || url.password) return null;
    return url.origin;
  } catch { return null; }
}

export function readConfig(env) {
  if (env.PROGRESS_SYNC_ENABLED !== 'true') {
    problem(503, 'sync_disabled', 'Cloud save is not enabled. Your local progress is still available.');
  }
  const issuer = canonicalOrigin(env.CLERK_ISSUER);
  const origins = String(env.APP_ORIGINS || '').split(',').map(x => x.trim()).filter(Boolean);
  if (!issuer || !origins.length || origins.length > 8 ||
      origins.some(x => !canonicalOrigin(x, true)) || !env.DATABASE_URL) {
    problem(503, 'sync_unavailable', 'Cloud save has not been configured. Your local progress is still available.');
  }
  return {issuer, origins, audience: env.CLERK_AUDIENCE || null};
}

function decodeSegment(segment) {
  if (!/^[A-Za-z0-9_-]+$/.test(segment)) throw new Error('Invalid JWT encoding');
  const bytes = Uint8Array.from(atob(segment.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));
  return bytes;
}

async function limitedJSON(response, maxBytes, status, code, message) {
  const size = response.headers.get('content-length');
  if (size && (!/^\d+$/.test(size) || Number(size) > maxBytes)) problem(status, code, message);
  if (!response.body) problem(status, code, message);
  const reader = response.body.getReader();
  const chunks = [];
  let total = 0;
  try {
    for (;;) {
      const {done, value} = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > maxBytes) {
        await reader.cancel();
        problem(status, code, message);
      }
      chunks.push(value);
    }
    const bytes = new Uint8Array(total);
    let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
    try { return JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(bytes)); }
    catch { problem(status === 413 ? 400 : status, code, message); }
  } finally { reader.releaseLock(); }
}

export function createTokenVerifier({fetchImpl = fetch, now = Date.now, cryptoImpl = crypto} = {}) {
  const cache = new Map();
  async function keysFor(issuer, kid) {
    let entry = cache.get(issuer);
    const time = now();
    const found = entry?.keys.find(key => key.kid === kid);
    if (entry && entry.until > time && (found || time - entry.fetched < UNKNOWN_KEY_COOLDOWN_MS)) return entry.keys;
    if (entry?.pending) return entry.pending;
    entry ||= {keys: [], fetched: 0, until: 0};
    const pending = (async () => {
      try {
        const response = await fetchImpl(`${issuer}/.well-known/jwks.json`, {
          headers: {Accept: 'application/json'}, redirect: 'error', signal: AbortSignal.timeout(5_000)
        });
        if (!response.ok) throw new Error('JWKS unavailable');
        const data = await limitedJSON(response, 65_536, 503, 'auth_unavailable', 'Sign-in verification is temporarily unavailable.');
        if (!object(data) || !Array.isArray(data.keys) || data.keys.length > 20) throw new Error('Invalid JWKS');
        entry.keys = data.keys;
        entry.fetched = now();
        entry.until = now() + JWKS_TTL_MS;
        return entry.keys;
      } catch {
        problem(503, 'auth_unavailable', 'Sign-in verification is temporarily unavailable.');
      } finally { entry.pending = null; }
    })();
    entry.pending = pending;
    if (!cache.has(issuer) && cache.size >= 4) cache.delete(cache.keys().next().value);
    cache.set(issuer, entry);
    return pending;
  }

  return async function verify(request, config) {
    const authorization = request.headers.get('authorization') || '';
    if (!authorization.startsWith('Bearer ') || authorization.length > MAX_TOKEN_LENGTH) {
      problem(401, 'not_signed_in', 'Sign in to save progress across devices.');
    }
    try {
      const token = authorization.slice(7);
      const parts = token.split('.');
      if (parts.length !== 3) throw new Error('Malformed JWT');
      const header = JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(decodeSegment(parts[0])));
      const claims = JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(decodeSegment(parts[1])));
      if (!object(header) || header.alg !== 'RS256' || (header.typ !== undefined && header.typ !== 'JWT') ||
          header.crit !== undefined || typeof header.kid !== 'string' || header.kid.length > 200 ||
          !object(claims)) throw new Error('Unsupported JWT');
      const seconds = Math.floor(now() / 1_000);
      if (claims.iss !== config.issuer || !config.origins.includes(claims.azp) ||
          !Number.isSafeInteger(claims.exp) || !Number.isSafeInteger(claims.nbf) ||
          !Number.isSafeInteger(claims.iat) || claims.exp <= seconds - 5 || claims.nbf > seconds + 5 ||
          claims.iat > seconds + 5 || claims.exp <= claims.iat ||
          typeof claims.sub !== 'string' || !/^user_[A-Za-z0-9_-]{1,128}$/.test(claims.sub) ||
          typeof claims.sid !== 'string' || !/^sess_[A-Za-z0-9_-]{1,128}$/.test(claims.sid) ||
          (claims.sts !== undefined && claims.sts !== 'active')) throw new Error('Invalid session claims');
      if (config.audience && !(Array.isArray(claims.aud) ? claims.aud.includes(config.audience) : claims.aud === config.audience)) {
        throw new Error('Wrong audience');
      }
      const keys = await keysFor(config.issuer, header.kid);
      const matches = keys.filter(key => key.kid === header.kid && key.kty === 'RSA' &&
        (key.alg === undefined || key.alg === 'RS256') && (key.use === undefined || key.use === 'sig'));
      if (matches.length !== 1) throw new Error('Unknown signing key');
      const key = await cryptoImpl.subtle.importKey('jwk', matches[0], {name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256'}, false, ['verify']);
      if (!await cryptoImpl.subtle.verify('RSASSA-PKCS1-v1_5', key, decodeSegment(parts[2]), encoder.encode(`${parts[0]}.${parts[1]}`))) {
        throw new Error('Bad signature');
      }
      return claims.sub;
    } catch (error) {
      if (error instanceof HttpProblem) throw error;
      problem(401, 'invalid_session', 'Your sign-in could not be verified. Please sign in again.');
    }
  };
}

function json(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {status, headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store, private',
    'CDN-Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    Vary: 'Authorization, Origin',
    ...extraHeaders
  }});
}

export function createProgressHandler({createStore, verify = createTokenVerifier()} = {}) {
  return async function handle({request, env}) {
    try {
      if (!['GET', 'PUT', 'DELETE'].includes(request.method)) {
        return json({error: 'method_not_allowed', message: 'Use GET, PUT or DELETE.'}, 405, {Allow: 'GET, PUT, DELETE'});
      }
      const config = readConfig(env);
      const origin = new URL(request.url).origin;
      if (!config.origins.includes(origin) ||
          (request.headers.has('origin') && request.headers.get('origin') !== origin) ||
          request.headers.get('sec-fetch-site') === 'cross-site') {
        problem(403, 'origin_not_allowed', 'This origin cannot access cloud progress.');
      }
      const userId = await verify(request, config);
      let payload;
      if (request.method !== 'GET') {
        if (request.headers.get('content-type')?.split(';')[0].trim().toLowerCase() !== 'application/json') {
          problem(415, 'json_required', 'Send progress as application/json.');
        }
        if (request.headers.has('content-encoding')) problem(415, 'encoding_not_supported', 'Compressed request bodies are not accepted.');
        payload = await limitedJSON(request, MAX_BODY_BYTES, 413, 'invalid_body', 'The progress data is invalid or exceeds 2 MB.');
        const keys = request.method === 'PUT' ? ['progress', 'expectedRevision'] : ['expectedRevision'];
        if (!object(payload) || !onlyKeys(payload, keys) || !Number.isSafeInteger(payload.expectedRevision) || payload.expectedRevision < 0) {
          problem(400, 'invalid_revision', 'Load your cloud progress before saving.');
        }
        if (request.method === 'PUT') payload.progress = validateProgress(payload.progress);
      }
      const store = createStore(env);
      if (request.method === 'GET') {
        const record = await store.get(userId);
        return json(record || {progress: null, revision: 0, updatedAt: null});
      }
      const result = request.method === 'PUT'
        ? await store.save(userId, payload.progress, payload.expectedRevision)
        : await store.remove(userId, payload.expectedRevision);
      if (!result) problem(409, 'revision_conflict', 'Cloud progress changed. Load it before saving again. Your local progress has not been changed.');
      return json(result);
    } catch (error) {
      if (error instanceof HttpProblem) return json({error: error.code, message: error.message}, error.status);
      // Never return provider errors: they may include SQL or connection credentials.
      return json({error: 'sync_unavailable', message: 'Cloud save is temporarily unavailable. Keep your local progress or export a backup.'}, 503);
    }
  };
}
