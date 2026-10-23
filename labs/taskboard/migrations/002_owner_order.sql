-- Additive migration: stage 06 remains compatible. Never rewrite an applied migration.
CREATE INDEX tasks_owner_order ON tasks (owner_id, created_at, id);
