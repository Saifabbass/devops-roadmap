// Cloudflare Pages advanced mode: a single module deployable via dashboard ZIP.
// Keep _routes.json alongside the bundle so only this API invokes a function.
import {onRequest} from '../functions/api/progress.js';

export default {
  async fetch(request, env, context) {
    if (new URL(request.url).pathname === '/api/progress') {
      return onRequest({request, env, waitUntil: context?.waitUntil?.bind(context)});
    }
    return env.ASSETS.fetch(request);
  }
};
