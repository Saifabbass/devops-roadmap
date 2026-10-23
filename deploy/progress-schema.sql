-- Run once in the intended Neon Free project using the SQL editor as owner.
-- No real learner data or credentials are embedded in this file.
BEGIN;

CREATE SEQUENCE IF NOT EXISTS public.learner_progress_revision_seq
  AS bigint MAXVALUE 9007199254740991 NO CYCLE;

CREATE TABLE IF NOT EXISTS public.learner_progress (
  user_id text PRIMARY KEY CHECK (user_id ~ '^user_[A-Za-z0-9_-]{1,128}$'),
  progress jsonb NOT NULL CHECK (
    jsonb_typeof(progress) = 'object'
    AND progress ?& ARRAY['schemaVersion', 'edition', 'weeks']
    AND progress ->> 'schemaVersion' = '1'
    AND jsonb_typeof(progress -> 'weeks') = 'object'
    AND octet_length(progress::text) <= 2100000
  ),
  revision bigint NOT NULL DEFAULT nextval('public.learner_progress_revision_seq'),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT learner_progress_safe_revision CHECK (revision BETWEEN 1 AND 9007199254740991)
);

REVOKE ALL ON public.learner_progress FROM PUBLIC;
REVOKE ALL ON public.learner_progress_revision_seq FROM PUBLIC;

COMMIT;

-- Recommended: create a separate login role in Neon for this function, then run
-- these grants with its actual role name (replace progress_app if different):
-- GRANT USAGE ON SCHEMA public TO progress_app;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON public.learner_progress TO progress_app;
-- GRANT USAGE ON SEQUENCE public.learner_progress_revision_seq TO progress_app;
-- Store only that role's DATABASE_URL as a Cloudflare encrypted secret.
-- Do not expose this table through a public Data API. Authorization belongs to
-- the server function, which derives user_id exclusively from the verified JWT.
