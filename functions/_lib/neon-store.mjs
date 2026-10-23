import {neon} from '@neondatabase/serverless';

function envelope(row) {
  if (!row) return null;
  const revision = Number(row.revision);
  if (!Number.isSafeInteger(revision) || revision < 1) throw new Error('Invalid database revision');
  if (!row.updated_at) throw new Error('Invalid database timestamp');
  return {progress: row.progress, revision, updatedAt: new Date(row.updated_at).toISOString()};
}

export function createNeonStore(env) {
  const sql = neon(env.DATABASE_URL);
  const query = (text, params) => sql.query(text, params, {fetchOptions: {signal: AbortSignal.timeout(8_000)}});
  return {
    async get(userId) {
      const rows = await query('SELECT progress, revision, updated_at FROM public.learner_progress WHERE user_id = $1', [userId]);
      return envelope(rows[0]);
    },
    async save(userId, progress, expectedRevision) {
      // One statement provides compare-and-swap even when two devices save at once.
      // Revisions come from a sequence so delete/recreate cannot reuse an old revision.
      const rows = await query(`
        WITH changed AS (
          UPDATE public.learner_progress
          SET progress = $2::jsonb, revision = nextval('public.learner_progress_revision_seq'), updated_at = now()
          WHERE user_id = $1 AND revision = $3::bigint AND $3::bigint > 0
          RETURNING progress, revision, updated_at
        ), created AS (
          INSERT INTO public.learner_progress (user_id, progress)
          SELECT $1, $2::jsonb WHERE $3::bigint = 0
          ON CONFLICT (user_id) DO NOTHING
          RETURNING progress, revision, updated_at
        )
        SELECT * FROM changed UNION ALL SELECT * FROM created`, [userId, JSON.stringify(progress), expectedRevision]);
      return envelope(rows[0]);
    },
    async remove(userId, expectedRevision) {
      const rows = await query('DELETE FROM public.learner_progress WHERE user_id = $1 AND revision = $2::bigint RETURNING user_id', [userId, expectedRevision]);
      return rows.length ? {progress: null, revision: 0, updatedAt: null} : null;
    }
  };
}
