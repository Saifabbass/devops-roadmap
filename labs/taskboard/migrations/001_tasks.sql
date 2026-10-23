CREATE TABLE tasks (
    id uuid PRIMARY KEY,
    owner_id text NOT NULL CHECK (char_length(owner_id) BETWEEN 1 AND 120),
    title text NOT NULL CHECK (char_length(title) BETWEEN 1 AND 120 AND title !~ '^[[:space:]]*$'),
    completed boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL,
    completed_at timestamptz,
    CONSTRAINT completion_consistent CHECK (
        (NOT completed AND completed_at IS NULL) OR
        (completed AND completed_at IS NOT NULL AND completed_at >= created_at)
    )
);
